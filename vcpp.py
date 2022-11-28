import struct
import pyaudio
import pvporcupine
import pvrhino
import speech_recognition as sr
import time

import commands

porcupine = None
pa = None
audio_stream = None

kws = ["computer", "jarvis"]
porcupine = pvporcupine.create(keywords=kws, access_key= "WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==")

rhino = pvrhino.create(
   access_key="WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==",
   context_path= "Christmas-in-Venice_en_mac_v2_1_0.rhn")

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
    print(keyword_index)
    isTrue = rhino.process(pcm)
    if isTrue:
        inference = rhino.get_inference()
        if inference.is_understood:
            intent = inference.intent
            slots = inference.slots
            print(kws[keyword_index])
            print(intent)
            print(slots)
        else:
            print("not understood")
        


