import threading
import time
import numpy as np
import RPi.GPIO as GPIO


class Arm(threading.Thread):
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

        self.range = 4
        self.period = [-1, 1, .5, .2, .1]
        self.index = 0
        
    def run(self):
        try:
            while True:
                if self.index != 0:
                    for i in np.linspace(0, 1, 10):
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[self.index]/10)
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[1]/10)
                        except KeyboardInterrupt:
                            self.pwm.stop()
                            GPIO.cleanup()
                            raise KeyboardInterrupt
                    for i in np.linspace(1, 0, 10):
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[self.index]/10)
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[1]/10)
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
        elif pm == 0 and self.index >0:
            self.index -= 1
    def getIndex(self):
        return self.index
    def setIndex(self, ind):
        self.index = ind
