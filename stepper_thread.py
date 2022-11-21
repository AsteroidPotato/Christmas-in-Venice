import threading
import time
import numpy as np
#import RPi.GPIO as GPIO


class Stepper(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

        self.pins = [17, 27, 22, 23] #the pins that control the coils
        self.lor = 1 #clockwise or anticlockwise
        self.rest = 1

        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.pins, GPIO.OUT)
         
    def run(self):
        while True:
            #GPIO.output(self.pins, GPIO.LOW) #reset all of our pins in list pins
            #GPIO.output(self.pins[0], GPIO.HIGH) #raise two pins
            #GPIO.output(self.pins[3], GPIO.HIGH)
            self.pins = np.roll(self.pins, self.lor).tolist() #rotate the list in the direction of lor = +/- 1
            time.sleep(self.rest) #wait rest time between steps
            print(self.pins)
