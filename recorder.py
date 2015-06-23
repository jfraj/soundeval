"""audio recorder"""

import pyaudio
import wave
import time

from baseaudio import BaseAudio


class AudioRecorder(BaseAudio):
    """Tools to record audio data."""

    def __init__(self, **kwargs):
        """Initializing for recording"""
        super(AudioRecorder, self).__init__(**kwargs)
        self.frames_perbuff = kwargs.get('chunk', 2048)
        self.channels = kwargs.get('channels', 1)
        self.format = pyaudio.paInt16  # paInt8
        # if recording is longer than max_length, it stops
        self.max_length = kwargs.get('max_length', 60)  # in seconds

    def start_record(self, **kwargs):
        countdown = kwargs.get('countdown', 3)
        savename = kwargs.get('savename', None)
        # Countdown before recording
        for isec_left in reversed(range(countdown)):
            print(isec_left + 1)
            time.sleep(0.8)
        # Record
        print('start recording')
        audio_api = pyaudio.PyAudio()
        stream = audio_api.open(format=self.format,
                                channels=self.channels,
                                rate=self.sampling_rate,
                                input=True,
                                frames_per_buffer=self.frames_perbuff)
        frames = []
        nchunks = int(self.max_length *
                      self.sampling_rate / self.frames_perbuff)
        try:
            for i in range(0, nchunks):
                data = stream.read(self.frames_perbuff)
                frames.append(data)
            print('max length ({}sec) reached...stop!'.format(self.max_length))
        except KeyboardInterrupt:
            print('\nStopped by user')
        print("* done recording")
        stream.stop_stream()
        stream.close()
        audio_api.terminate()
        if savename is not None:
            print('saving as {}'.format(savename))
            wf = wave.open(savename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio_api.get_sample_size(self.format))
            wf.setframerate(self.sampling_rate)
            wf.writeframes(b''.join(frames))
            wf.close()

if __name__ == "__main__":
    rec = AudioRecorder(max_length=20)
    rec.start_record(savename='test.wav')
    #print(rec)
