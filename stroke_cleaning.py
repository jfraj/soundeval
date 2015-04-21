from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

# Audio information retrieval
import essentia.standard as ess
from essentia.standard import MonoLoader
from essentia.standard import Centroid, Spectrum, Windowing
#get_onsets = ess.OnsetRate()
#centroid = Centroid(range=22050)
#hamming_window = Windowing(type='hamming')
#zcr = ess.ZeroCrossingRate()
#spectrum = ess.Spectrum()

# Classifier and feature processing
from sklearn import preprocessing
from sklearn.cluster import KMeans


class audio_sample():
    """
    Contain an audio data and methods to clean it and extract feature
    """
    def __init__(self, audio_fname, good_range=None):
        """
        Loads the audio file and make the features
        """
        # Some parameters
        self.sampling_rate = 44100  # This is essentia's default
        self.stroke_length = 0.5  # In seconds

        # Getting the audio signal
        self.audio_fname = audio_fname
        # Following is an audio signal sampled in 44100Hz (essentia default)
        self.audio = MonoLoader(filename=audio_fname)()

        # Cleaning edges
        if good_range is None:
            good_range = (0, len(self.audio))
        self.audio = self.audio[good_range[0]:good_range[1]]

        # Some parameter that will be defined by signal processing
        self.onset_times = False  # In seconds
        self.onset_samples = False  # As sample number in the audio sampling
        self.strokes = False
        self.stroke_df = False
        self.feature_table = False

    def find_onsets(self):
        """
        Get the starting of each strokes
        """
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
        """
        Fills self.strokes dictionary of signal strokes
        """
        self.find_onsets()
        # Defining the frame to contain the strokes
        frame_sz = int(self.stroke_length*self.sampling_rate)
        self.strokes = np.array(
            [self.audio[i:i+frame_sz] for i in self.onset_samples])

    def extract_features_from_frame(self, frame):
        centroid = Centroid(range=22050)
        hamming_window = Windowing(type='hamming')
        zcr = ess.ZeroCrossingRate()
        spectrum = ess.Spectrum()
        # Spectrum can only compute FFT of array of even size (don't know why)
        if len(frame) % 2 == 1:
            frame = frame[:-1]
        spectral_magnitude = spectrum(hamming_window(frame))
        #return [zcr(frame), centroid(spectral_magnitude)]
        return {'zrc':zcr(frame), 'centroid':centroid(spectral_magnitude)}

    def get_features(self):
        """
        Returns a feature table from the strokes
        """
        if self.strokes is False:
            self.isolate_strokes()
        #feature_table = np.array(
        #    [self.extract_features_from_frame(stroke) for stroke in self.strokes])
        feature_names = ('zrc', 'centroid')
        features_list = []
        for istroke in self.strokes:
            ifeature_dic = self.extract_features_from_frame(istroke)
            ifeature_list = []
            for ifeature in feature_names:
                ifeature_list.append(ifeature_dic[ifeature])
            features_list.append(ifeature_list)
        return {'feature_names': feature_names,
                'feature_table': np.array(features_list)}

    def show_signal(self):
        """
        plots the audio signal
        """
        # Make signal as time

        nsamples = len(self.audio)
        print nsamples
        times = np.arange(0, nsamples)/self.sampling_rate
        fig = plt.figure()
        #plt.plot(self.audio)
        plt.plot(times, self.audio)
        if self.onset_samples is not False:
            #for istroke_start in self.onset_samples:
            for istroke_start in self.onset_times:
                plt.axvline(istroke_start, color='r')
        fig.show()
        raw_input('press enter when finished...')

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
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/marina.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/jfraj.m4a',(95000, -400000))
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_ON.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_ON.m4a')
    #testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/sustainedG_shoulder_rest_ON.m4a')
    testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/sustainedG_shoulder_rest_OFF.m4a')

    #testaudio.show_signal()
    #testaudio.isolate_strokes()
    #testaudio.show_signal()
    #testaudio.show_strokes()
    print testaudio.get_features()
