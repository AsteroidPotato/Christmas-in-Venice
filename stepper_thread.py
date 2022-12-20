import threading
import time
import numpy as np
import RPi.GPIO as GPIO


class Stepper(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

        self.pins = [17, 27, 22, 23] #the pins that control the coils
        self.lor = 1 #clockwise or anticlockwise
        self.rest = [-1, .1, .05, .01, .001] #predefined speeds
        self.index = 0 # initiate the stepper at 0 speed
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT)
"""The inherited run method from threading.Thread. This runs on
thread.start() call

This method runs the stepper rotation loop"""  
    def run(self):
        # run the loop until a keyboard interrupt.
        try:
            while True:
                if self.rest[self.index] != -1:
                    time.sleep(self.rest[self.index]) #wait rest time between steps
                    GPIO.output(self.pins, GPIO.LOW) #reset all of our pins in list pins
                    GPIO.output(self.pins[0], GPIO.HIGH) #raise two pins
                    GPIO.output(self.pins[3], GPIO.HIGH)
                    self.pins = np.roll(self.pins, self.lor).tolist() #rotate the list in the direction of lor = +/- 1
        except ValueError:
            GPIO.cleanup()
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("stepper interrupted")
            raise KeyboardInterrupt
"""update the index for the self.rest list. This dictates which speed
preset the stepper will rotate

pm is either +1 for increase speed or 0 for decrease speed"""
    def updateSpeed(self, pm):
        if pm == 1 and self.index < 5:
            self.index += 1
        elif pm == 0 and self.index >0:
            self.index -= 1
"""return self.index"""
    def getIndex(self):
        return self.index
"""set self.index"""
    def setIndex(self, ind):
        self.index = ind
