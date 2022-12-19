import struct
import pyaudio
import pvrhino
import time
import commands
import RPi.GPIO as GPIO

pa = None
audio_stream = None


rhino = pvrhino.create(
   access_key="WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==",
   context_path= "Christmas-in-Venice_en_raspberry-pi_v2_1_0.rhn")

pa = pyaudio.PyAudio()

audio_stream = pa.open(rate=rhino.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=rhino.frame_length)
try:
    while True:
        pcm = audio_stream.read(rhino.frame_length)
        pcm = struct.unpack_from("h" * rhino.frame_length, pcm)

        isTrue = rhino.process(pcm)
        if isTrue:
            inference = rhino.get_inference()
            if inference.is_understood:
                intent = inference.intent
                slots = inference.slots
                print(slots)
                func = getattr(commands, intent)
                func(slots)
            else:
                pass

except KeyboardInterrupt:
    print("vcpp interrupted")
    GPIO.cleanup()

    
    
        


