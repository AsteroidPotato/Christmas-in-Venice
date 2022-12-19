import threading
import time
import numpy as np
import RPi.GPIO as GPIO


class HT(threading.Thread):
    def __init__(self, center, pin, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)
        self.center = center

        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)

        self.pwm.start(self.center)

        self.range = .5
        self.period = [-1, 3, 2, 1, .5]
        self.index = 0
        
    def run(self):
        try:
            while True:
                if self.index != 0:
                    for i in np.linspace(0, 2*np.pi, 100):
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i))
                            time.sleep(self.period[self.index]/100)
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i))
                            time.sleep(self.period[1]/100)
                        except KeyboardInterrupt:
                            self.pwm.stop()
                            GPIO.cleanup()
                            raise KeyboardInterrupt
                        
                else:
                    self.pwm.ChangeDutyCycle(self.center)
            
                        
        except KeyboardInterrupt:
            print("servo interrupted")
            self.pwm.stop()
            GPIO.cleanup()
            raise KeyboardInterrupt
    def updateSpeed(self, pm):
        if pm == 1 and self.index < 5:
            self.index += 1
        elif pm == 0 and self.index >1:
            self.index -= 1
    def getIndex(self):
        return self.index
    def setIndex(self, ind):
        self.index = ind
