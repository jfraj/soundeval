from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import os

# Audio information retrieval
import essentia.standard as ess
from essentia.standard import MonoLoader
from essentia.standard import Centroid, Spectrum, Windowing

# Classifier and feature processing
from sklearn import preprocessing
from sklearn.cluster import KMeans


class audio_sample():
    """Contain an audio data and methods to clean it and extract feature.

    Attributes
    ----------
    sampling_rate : frequency of the recording

    stroke_length : length of a stroke to determin onsets

    audio_fname : path of the audio file

    audio : numpy array of the audio signal
    """

    def __init__(self, audio_fname, good_range=None, **kwargs):
        """
        Load the audio file and determin the features
        """
        # Some parameters
        self.sampling_rate = 44100  # This is essentia's default
        self.stroke_length = kwargs.get('stroke_length', 0.5)  # In seconds
        self.clip_start = kwargs.get('clip_start', True)  # In seconds
        self.clip_end = kwargs.get('clip_end', True)  # In seconds

        # Getting the audio signal
        self.audio_fname = audio_fname
        # Following is an audio signal sampled in 44100Hz (essentia default)
        self.audio = MonoLoader(filename=audio_fname)()

        # Cleaning edges
        try:
            self.audio = self.audio[good_range[0]:good_range[1]]
        except:
            pass

        # clipping
        self.audio_thd = 0.05
        self.beginning_buffer = 1 # in seconds
        if self.clip_start:
            clipped_start = np.argmax(self.audio>self.audio_thd) - self.beginning_buffer*self.sampling_rate
            clipped_start = max(0, clipped_start)
            self.audio = self.audio[clipped_start:-1]

        if self.clip_end:
            reversed_audio = self.audio[::-1]
            clipped_end = len(reversed_audio) - np.argmax(reversed_audio>self.audio_thd) - 1 + self.beginning_buffer*self.sampling_rate
            self.audio = self.audio[:clipped_end]

        # Some parameter that will be defined by signal processing
        self.onset_times = False  # In seconds
        self.onset_samples = False  # As sample number in the audio sampling
        self.strokes = False
        self.stroke_df = False
        self.feature_table = False

    def set_fake_regular_offsets(self, win_wd, win_gap=0):
        """Fill offsets with regular times.

        Parameters
        ----------
        win_wd : window width (unit seconds)

        win_gap : gap length between windows (unit seconds)

        """
        sample_onset = int((win_wd + win_gap)*self.sampling_rate)
        self.onset_samples = range(0, len(self.audio), sample_onset)
        # excluding windows that are too close to the beginning
        self.onset_samples = [x for x in self.onset_samples if x > self.beginning_buffer]
        self.onset_times = [x/self.sampling_rate for x in self.onset_samples]

    def find_onsets(self):
        """Find and save stroke beginning"""
        get_onsets = ess.OnsetRate()
        # onset_times is np array
        self.onset_times, onset_rate = get_onsets(self.audio)
        # Onset as sample number in the audio signal
        index2delete = []
        previous_time = -9999999
        for index, itime in enumerate(self.onset_times):
            if (itime - previous_time) < 2*self.stroke_length:
                index2delete.append(index)
            else:
                previous_time = itime
        self.onset_times = np.delete(self.onset_times, index2delete)
        self.onset_samples = [int(self.sampling_rate*i) for i in self.onset_times]

    def isolate_strokes(self):
        """Fill self.strokes dictionary of signal strokes."""
        if self.onset_times is False:
            self.find_onsets()
        # Defining the frame to contain the strokes
        frame_sz = int(self.stroke_length*self.sampling_rate)
        self.strokes = np.array(
            [self.audio[i:i+frame_sz] for i in self.onset_samples])

    def isGoodFrame(self, frame):
        """True if frame passes some quality test."""
        if max(frame)<0.1:
            return False
        return True

    def extract_features_from_frame(self, frame):
        """ Return dictionary of features for the given frame."""
        centroid = Centroid(range=22050)
        hamming_window = Windowing(type='hamming')
        zcr = ess.ZeroCrossingRate()
        spectrum = ess.Spectrum()
        # Spectrum can only compute FFT of array of even size (don't know why)
        if len(frame) % 2 == 1:
            frame = frame[:-1]
        spectral_magnitude = spectrum(hamming_window(frame))
        return {'zrc':zcr(frame), 'centroid':centroid(spectral_magnitude)}

    def get_features(self):
        """Return a feature table from the strokes."""
        if self.strokes is False:
            print('Isolating strokes')
            self.isolate_strokes()
        feature_names = ('zrc', 'centroid')
        features_list = []
        for istroke in self.strokes:
            if not self.isGoodFrame(istroke):
                continue
            ifeature_dic = self.extract_features_from_frame(istroke)
            ifeature_list = []
            for ifeature in feature_names:
                ifeature_list.append(ifeature_dic[ifeature])
            features_list.append(ifeature_list)
        return {'feature_names': feature_names,
                'feature_table': np.array(features_list)}

    def plot_signal(self, **kwargs):
        """plot audio signal."""
        label = kwargs.get('label', None)
        # Calculate strokes if requested
        with_strokes = kwargs.get("with_strokes", False)
        x_axis_type = kwargs.get("x_axis_type", 'time')
        if with_strokes and self.onset_samples is False:
            self.isolate_strokes()

        # Plot signal
        nsamples = len(self.audio)
        print nsamples
        x_axis = np.arange(0, nsamples)
        if x_axis_type == 'time':
            x_axis = x_axis/self.sampling_rate
        plt.plot(x_axis, self.audio, color='b')
        plt.xlabel(x_axis_type)

        # Add strokes if availables
        if self.onset_samples is not False:
            print('Plotting strokes')
            onsets = self.onset_samples
            if x_axis_type == 'time':
                onsets = self.onset_times
            for istroke_start, istroke in zip(onsets, self.strokes):
                if not self.isGoodFrame(istroke):
                    continue
                plt.axvline(istroke_start, color='r', alpha=0.2)

    def show_strokes(self):
        """
        plots the isolated stroke signal
        """
        assert(self.strokes is not False)
        fig = plt.figure()
        for istroke in range(self.strokes.shape[0]):
            plt.subplot(self.strokes.shape[0] + 1, 1, istroke + 1)
            plt.plot(self.strokes[istroke])
        fig.show()
        raw_input('press enter when finished...')

if __name__=='__main__':
    audio_dir = "/Users/jean-francoisrajotte/myaudio/alto_recordings/"
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/marina.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/jfraj.m4a',(95000, -400000))
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_ON.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_ON.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/sustainedG_shoulder_rest_ON.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/sustainedG_shoulder_rest_OFF.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/marina_20150507_test.m4a')
    fname = os.path.join(audio_dir, 'jfraj_marcmalobowtest2_20150610b.m4a')
    testaudio = audio_sample(fname, stroke_length=0.5)

    #testaudio.show_signal()
    #testaudio.isolate_strokes()
    #testaudio.set_fake_regular_offsets(2)
    fig = plt.figure()
    testaudio.plot_signal(x_axis_type='sample')
    fig.show()
    raw_input('ok...')
    #testaudio.show_strokes()
    #print testaudio.get_features()
