import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import itertools
import pandas as pd
import numpy as np
from datetime import datetime

# This project
import stroke_cleaning

colors = itertools.cycle(["r", "b", "g", "k", "c", "m", "y"])

def plot_features_from_audio(audio):
    """Plot the features from the audio sample object"""
    feature_dic = audio.get_features()
    features = feature_dic['feature_table']
    # Plot
    plt.scatter(features[:, 0], features[:, 1],
                color=next(colors), s=70, alpha=0.5)
    plt.xlabel(feature_dic['feature_names'][0])
    plt.ylabel(feature_dic['feature_names'][1])
    plt.grid()

def plot_features_from_list(audio_list, label_list=None, good_range_list=None, **kwargs):
    """Plot features for audio signal in the given list."""
    if good_range_list is None:
        good_range_list = [None]*len(audio_list)
    if label_list is None:
        label_list = [os.path.basename(x) for x in audio_list]
    fake_stroke_onset = kwargs.get("fake_stroke_onset", False)
    print('Fake stroke is {}'.format(fake_stroke_onset))
    for iaudiofile, ilabel, igood_range in zip(
            audio_list, label_list, good_range_list):
        iaudio = stroke_cleaning.audio_sample(iaudiofile, igood_range)

        # Strokes are either searched or just regular samples
        if fake_stroke_onset is not False:
            print('Using fake stroke')
            iaudio.set_fake_regular_offsets(fake_stroke_onset)
        else:
            iaudio.isolate_strokes()

        # Features
        ifeature_dic = iaudio.get_features()
        ifeatures = ifeature_dic['feature_table']
        print('features shape: {}'.format(ifeatures.shape))
        del(iaudio)

        # Plot
        plt.scatter(ifeatures[:, 0], ifeatures[:, 1],
                    color=next(colors), s=70, label=ilabel, alpha=0.5)
        plt.xlabel(ifeature_dic['feature_names'][0])
        plt.ylabel(ifeature_dic['feature_names'][1])
    plt.grid()
    plt.legend(loc='best')


def show_features_from_list(audio_list, label_list=None, good_range_list=None, **kwargs):
    """Plot features for audio signal in the given list."""
    fig = plt.figure()
    plot_features_from_list(audio_list, label_list, good_range_list, **kwargs)
    fig.show()
    raw_input('press enter when finished...')

def get_features_from_path_list(path_list, goodrange_list, **kwargs):
    """Return feature dict from path list"""
    fake_stroke_onset = kwargs.get('fake_stroke_onset', False)
    feature_dic = {}
    for iaudiofile, igood_range in zip(path_list, goodrange_list):
        iaudio = stroke_cleaning.audio_sample(iaudiofile, igood_range)

        # Strokes are either searched or just regular samples
        if fake_stroke_onset is not False:
            print('Using fake stroke')
            iaudio.set_fake_regular_offsets(fake_stroke_onset)
        else:
            iaudio.isolate_strokes()
        ifeature_dic = iaudio.get_features()
        if not feature_dic.has_key('feature_names'):
            feature_dic.update(ifeature_dic)
        else:
            feature_dic['feature_table'] =\
                np.vstack((feature_dic['feature_table'],
                          ifeature_dic['feature_table']))
    return feature_dic


def show_grouped_features(group_dict):
    """Plot the features from the group"""
    fig = plt.figure()
    for igroup in group_dict.keys():
        ifeature_dic =\
            get_features_from_path_list(group_dict[igroup]['paths'],
                                        group_dict[igroup]['goodranges'])
        ifeatures = ifeature_dic['feature_table']
        print('features shape: {}'.format(ifeatures.shape))

        # Plot
        plt.scatter(ifeatures[:, 0], ifeatures[:, 1],
                    color=next(colors), s=70, label=igroup, alpha=0.5)
        plt.xlabel(ifeature_dic['feature_names'][0])
        plt.ylabel(ifeature_dic['feature_names'][1])
    plt.grid()
    plt.legend(loc='best')
    fig.show()
    raw_input('press enter when finished...')


def show_features_from_dic(audio_dic, **kwargs):
    """Plot features for audio signal in the given dict."""
    recording_list = []
    good_range_list = []
    label_list = []
    for ilabel, idic in audio_dic.items():
        label_list.append(ilabel)
        recording_list.append(idic['audio_file'])
        good_range_list.append(idic['good_range'])
    show_features_from_list(recording_list, label_list, good_range_list, **kwargs)

def show_players_features():
    """Plot the features grouped by file selection"""
    df_data = pd.read_csv('datainfo.csv', sep=' ', na_values='None')
    print(df_data.head())
    grouping_dict = {}
    for iplayer in df_data.player.unique():
        ipathlist = df_data[df_data.player==iplayer]['path'].tolist()
        igoodrangelist = df_data[df_data.player==iplayer]['goodrange'].tolist()
        grouping_dict[iplayer] = {'paths': ipathlist,
                                  'goodranges': igoodrangelist}
    show_grouped_features(grouping_dict)

def audio_report(fname):
    """Plot summary of the given audio file."""
    audio = stroke_cleaning.audio_sample(fname)
    audio.set_fake_regular_offsets(1)
    fig_sig = plt.figure()
    audio.plot_signal(x_axis_type='sample')
    fig_sig.show()

    fig_feat = plt.figure()
    plot_features_from_audio(audio)
    plt.grid()
    fig_feat.show()
    raw_input('press enter when finished...')

def show_multiaudio(fnames, good_ranges = None):
    """Show summary of all the audio files in the given list."""

    if good_ranges is None:
        good_ranges = [None]*len(fnames)
    fig_feat = plt.figure(1)
    fig_raw = plt.figure(2)

    for idx, (iaudiofile, igood_range) in enumerate(zip(fnames, good_ranges)):
        print(igood_range)
        try:
            igood_range = igood_range.split('-')
            igood_range = (int(igood_range[0]), int(igood_range[1]))
        except AttributeError:
            igood_range = None
        print(igood_range)
        iaudio = stroke_cleaning.audio_sample(iaudiofile, igood_range)
        ilabel = os.path.basename(iaudiofile)
        iaudio.set_fake_regular_offsets(0.5)
        # Features
        ifeature_dic = iaudio.get_features()
        plt.figure(2)
        iax = fig_raw.add_subplot(len(fnames),1,idx)
        iaudio.plot_signal(label=os.path.basename(iaudiofile).split('.')[0])
        iax.text(0.05, 0.95, ilabel,
                 verticalalignment='top', horizontalalignment='left',
                 transform=iax.transAxes, fontsize=15)

        ifeatures = ifeature_dic['feature_table']
        plt.figure(1)
        plt.scatter(ifeatures[:, 0], ifeatures[:, 1],
                    color=next(colors), s=70, label=ilabel, alpha=0.5)
        plt.xlabel(ifeature_dic['feature_names'][0])
        plt.ylabel(ifeature_dic['feature_names'][1])
        plt.legend(loc='best')

    fig_feat.show()
    fig_raw.show()
    raw_input('press enter when finished...')

def show_day(daystr):
    """Show summary of all the audiofile from a given day."""
    df_data = pd.read_csv('datainfo.csv', sep=' ', na_values='None',
                          dtype={'date': datetime})
    fnames = df_data[df_data.date==daystr].path.tolist()
    good_ranges = df_data[df_data.date==daystr].goodrange.tolist()

    show_multiaudio(fnames, good_ranges)

if __name__ == '__main__':
    #recording_list = (
    #    '/Users/jean-francoisrajotte/myaudio/marina.m4a',
    #    '/Users/jean-francoisrajotte/myaudio/jfraj.m4a',
    #    )
    #show_features_from_list(recording_list)
    recording_dic = {}
    recording_dic['marina'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/marina.m4a',
        'good_range': None}
    recording_dic['jfraj'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/jfraj.m4a',
        'good_range': (95000, -400000)}
    recording_dic['marina_srON'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_ON.m4a',
        'good_range': None}
    recording_dic['marina_srOFF'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/astring_shoulder_rest_OFF.m4a',
        'good_range': None}
    recording_dic['marina_srON'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/marina_20150507.m4a',
        'good_range': None}
    recording_dic['marina_srOFF'] = {
        'audio_file': '/Users/jean-francoisrajotte/myaudio/marina_20150507_test.m4a',
        'good_range': None}
    #show_features_from_dic(recording_dic)
    #show_players_features()
    #audio_dir = "/Users/jean-francoisrajotte/myaudio/alto_recordings/"
    #audioname = os.path.join(audio_dir, 'marina_20150513_halfbow_testbow1.m4a')
    #audio_report(audioname)
    show_day('20150623')
