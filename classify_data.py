"""Script to classify a list of audio samples"""
import sys
import matplotlib.pyplot as plt
import pandas as pd
import stroke_cleaning
import itertools

def show_features_from_list(audio_list):
    """
    """
    fig = plt.figure()
    features_dict = {}
    colors = itertools.cycle(["r", "b", "g"])
    for iaudiofile in audio_list:
        iaudio = stroke_cleaning.audio_sample(iaudiofile)
        iaudio.isolate_strokes()
        ifeatures = iaudio.get_features()
        del(iaudio)
        plt.scatter(ifeatures[:, 0], ifeatures[:, 1],color=next(colors), s=70)
    fig.show()
    raw_input('press enter when finished...')
    

def main():
    """
    goes through a list of audio sample files
    Reduce into features
    Train a classifier with good or bad labels
    """
    testaudio = stroke_cleaning.audio_sample('/Users/jean-francoisrajotte/myaudio/marina.m4a')
    testaudio.isolate_strokes()
    features = testaudio.get_features()
    fig = plt.figure()
    plt.scatter(features[:, 0], features[:, 1], c='b',s=70)
    fig.show()
    raw_input('press entre when finished ...')

if __name__ == '__main__':
    #sys.exit(main())
    recording_list = (
        '/Users/jean-francoisrajotte/myaudio/marina.m4a',
        '/Users/jean-francoisrajotte/myaudio/jfraj.m4a',
        )
    show_features_from_list(recording_list)
