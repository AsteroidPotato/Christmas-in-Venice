import speech_recognition as sr
import time

def into(wake):
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)

    stop_thread = rec.listen_in_background(mic, parse_phrase)
    time.sleep(5)
    stop_thread(wait_for_stop=True)
    

def parse_phrase(recognizer, audio):
    print("callback")
    try:
        val = recognizer.recognize_google(audio)
        print(val)
        for key, value in command_dictionary1:
            if key in val:
                value()
    except sr.UnknownValueError:
        print("UnknownValueError caught")
        
def test_comm():
    print("the test was successful")

command_dictionary1 = {'test' : test_comm }
command_dictionary2 = {}

def find(string):
    #TEST: print("searching dictionary")
    for key in command_dictionary.keys():
        if key in string:
            command_dictionary[key]()
