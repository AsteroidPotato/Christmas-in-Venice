from picovoice import Picovoice
import pyaudio

def wake_word_callback():
    # wake word detected
    pass

def inference_callback(inference):
   if inference.is_understood:
      intent = inference.intent
      slots = inference.slots
      # take action based on intent and slot values
   else:
      # unsupported command
      pass

handle = Picovoice(
     access_key= "WnYuSEJ+OsuCObjZ3C8rBJ6kkKoH+Z2qTgLh3YFCehiUGlEQzGT32Q==",
     keyword_path= "alexa_mac.ppn",
     wake_word_callback=wake_word_callback,
     context_path="smart_lighting_mac.rhn",
     inference_callback=inference_callback)

def get_next_audio_frame():
    pass #replace with audio collection

while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)

