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
        self.rest = [-1, .2, .05, .01, .001, .0001]
        self.index = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT)
         
    def run(self):
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
    def updateSpeed(self, pm):
        if pm == 1 and self.index < 5:
            self.index += 1
        elif pm == 0 and self.index >0:
            self.index -= 1
    def getIndex(self):
        return self.index
    def setIndex(self, ind):
        self.index = ind
