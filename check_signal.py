import matplotlib.pyplot as plt
import itertools

import stroke_cleaning


def show_features_from_list(audio_list, label_list=None, good_range_list=None):
    """
    """
    if good_range_list is None:
        good_range_list = [None]*len(audio_list)
    if label_list is None:
        label_list = [None]*len(label_list)
    fig = plt.figure()
    colors = itertools.cycle(["r", "b", "g", "k"])
    for iaudiofile, ilabel, igood_range in zip(
            audio_list, label_list, good_range_list):
        iaudio = stroke_cleaning.audio_sample(iaudiofile, igood_range)
        iaudio.isolate_strokes()
        ifeatures = iaudio.get_features()
        del(iaudio)
        plt.scatter(ifeatures[:, 0], ifeatures[:, 1],
                    color=next(colors), s=70, label=ilabel)
    plt.grid()
    plt.legend(loc='best')
    fig.show()
    raw_input('press enter when finished...')

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
    recording_list = []
    good_range_list = []
    label_list = []
    for ilabel, idic in recording_dic.items():
        label_list.append(ilabel)
        recording_list.append(idic['audio_file'])
        good_range_list.append(idic['good_range'])
    show_features_from_list(recording_list, label_list, good_range_list)
