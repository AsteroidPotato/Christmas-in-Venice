import pyaudio
import speech_recognition as sr
import time

import commands

keyword = "Santa"

rec = sr.Recognizer()
mic = sr.Microphone()




def keyword_check(recognizer, audio):
    #TEST:
    print("callback")
    try:
        val = recognizer.recognize_google(audio)
        #TEST:
        print(val)
        if keyword in val:
            commands.find(val)
    except sr.UnknownValueError:
        print("UnknownValueError caught")

with mic as source:
    rec.adjust_for_ambient_noise(source)

stop_thread = rec.listen_in_background(mic, keyword_check)

time.sleep(200)
