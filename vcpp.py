import struct
import pyaudio
import pvporcupine
import speech_recognition as sr

import commands

porcupine = None
pa = None
audio_stream = None

porcupine = pvporcupine.create(keywords=["computer", "jarvis"], access_key= "WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==")

pa = pyaudio.PyAudio()

audio_stream = pa.open(rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        print("Hotword Detected")
        print(keyword_index)
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)



