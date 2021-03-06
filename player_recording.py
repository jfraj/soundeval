import os
import time

#  This project
import recorder
import check_signal


def record_playing(**kwargs):
    """Record audio signal and save it."""
    save_dir = kwargs.get('save_dir', 'test/')
    show_audio = kwargs.get('show_audio', False)
    countdown = kwargs.get('countdown', 3)
    max_length = kwargs.get('max_length', 60)
    basename = kwargs.get('basename', None)
    if basename is None:
        basename = raw_input('Type a name for the file? ')
    save_name = '{}_{}.wav'.format(basename, time.strftime("%Y%m%d"))
    save_name = os.path.join(save_dir, save_name)
    wait4enter = kwargs.get('wait4enter', True)
    if wait4enter:
        raw_input('Press enter when ready to start...')
    rec = recorder.AudioRecorder(max_length=max_length, countdown=countdown)
    rec.start_record(savename=save_name)
    if show_audio:
        check_signal.audio_report(save_name)
    return save_name


def multi_recording(**kwargs):
    """Record multiple audio signal and save them."""
    file_list = []
    while True:
        if raw_input('Another one?') not in ('y', 'Y', 'yes', 'Yes', 'YES'):
            break
        file_list.append(record_playing())
    check_signal.show_multiaudio(file_list)

if __name__ == "__main__":
    #record_playing(show_audio=True)
    multi_recording()
