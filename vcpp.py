import struct
import pyaudio
import pvrhino
import time
import commands
import RPi.GPIO as GPIO

"""This is the primary file that runs everything else"""

pa = None
audio_stream = None

# create rhino speech-to-intent object using my access key and speech-to-intent tree (context_path)
rhino = pvrhino.create(
   access_key="WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==",
   context_path= "Christmas-in-Venice_en_raspberry-pi_v2_1_0.rhn")

# start a pyaudio object to record audio
pa = pyaudio.PyAudio()

# open the audio stream using pa
audio_stream = pa.open(rate=rhino.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=rhino.frame_length)
try:
    # listen for key phrases
    while True:
        pcm = audio_stream.read(rhino.frame_length)
        pcm = struct.unpack_from("h" * rhino.frame_length, pcm)

        isTrue = rhino.process(pcm) # did the pi hear something?
        if isTrue:
            inference = rhino.get_inference() # extract inference from speech-to-intent tree
            # if the inference is one of the ones I defined, continue
            if inference.is_understood:
                intent = inference.intent # which function does the inference think the pi should run?
                slots = inference.slots # what are the inputs to that function?
                print(slots)
                func = getattr(commands, intent) # extract the appropriate function from the commands file
                func(slots) # run that function with the inputs extracted from the inference
            else:
                pass

except KeyboardInterrupt:
    print("vcpp interrupted")
    GPIO.cleanup()

    
    
        


