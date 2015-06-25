import os
import time

#  This project
import recorder
import check_signal

def record_playing(**kwargs):
    """Record audio signal and save it."""
    save_dir = kwargs.get('save_dir', 'test/')
    show_audio = kwargs.get('show_audio', False)
    basename = raw_input('Type a name for the file? ')
    save_name = '{}_{}.wav'.format(basename, time.strftime("%Y%m%d"))
    save_name = os.path.join(save_dir, save_name)
    raw_input('Press enter when ready to start...')
    rec = recorder.AudioRecorder(max_length=60)
    rec.start_record(savename=save_name)
    if show_audio:
        check_signal.audio_report(save_name)


if __name__ == "__main__":
    record_playing(show_audio=True)
