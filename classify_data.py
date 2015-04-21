"""Script to classify a list of audio samples"""
import sys
import pandas as pd
import stroke_cleaning

def get_features_from_file(audio_file):
    audio = stroke_cleaning.audio_sample(audio_file)
    return pd.DataFrame(audio.get_features())


def get_df_from_list(audio_files):
    """
    Will return a data frame
    filled with the features from audio files from the list
    """
    frames = [get_features_from_file(f) for f in audio_files]
    return pd.concat(frames)


def main():
    """
    goes through a list of audio sample files
    Reduce into features
    Train a classifier with good or bad labels
    """
    #testaudio = stroke_cleaning.audio_sample('/Users/jean-francoisrajotte/myaudio/marina.m4a')
    #df = pd.DataFrame(testaudio.get_features())
    #df['player'] = 1
    #print df
    list1 = ['/Users/jean-francoisrajotte/myaudio/marina.m4a',
             '/Users/jean-francoisrajotte/myaudio/marina.m4a',
             ]
    list2 = ['/Users/jean-francoisrajotte/myaudio/jfraj.m4a',
             '/Users/jean-francoisrajotte/myaudio/jfraj.m4a',
             ]
    df1 = get_df_from_list(list1)
    df1['player'] = 1
    print df1
    df2 = get_df_from_list(list2)
    df2['player'] = 2
    print df2
    df = pd.concat([df1,df2])

    print df

if __name__ == '__main__':
    sys.exit(main())
