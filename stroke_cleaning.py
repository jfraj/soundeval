import matplotlib.pyplot as plt
import numpy as np

## Audio information retrieval
import essentia.standard as ess
from essentia.standard import MonoLoader
from essentia.standard import Centroid, Spectrum, Windowing

## Classifier and feature processing
from sklearn import preprocessing
from sklearn.cluster import KMeans


class audio_sample():
    """
    Contain an audio data and methods to clean it and extract feature 
    """
    def __init__(self, audio_fname):
        """
        Loads the audio file and make the features
        """
        self.audio_fname = audio_fname
        ## The following is an audio signal sampled in 44100Hz (essentia default)
        self.audio = MonoLoader(filename=audio_fname)()

        
    def show_signal(self):
        """
        plots the audio signal
        """
        fig = plt.figure()
        plt.plot(self.audio)
        fig.show()
        raw_input('press enter when finished...')

if __name__=='__main__':
    testaudio = audio_sample('/Users/jean-francoisrajotte/myaudio/marina.m4a')
    testaudio.show_signal()
