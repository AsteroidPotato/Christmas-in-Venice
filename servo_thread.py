import threading
import time
import numpy as np
import RPi.GPIO as GPIO

"""Class to run the arm/oar servo on Santa"""



class Arm(threading.Thread):

"""center is the duty cycle value for the servo's center mark
pin is the GPIO pin for the servo"""
    def __init__(self, center, pin, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

        self.center = center # centered duty cycle calibrated to each servo
        self.pin = pin # GPIO pin for servo
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.center)

        self.range = 4 # range of motion for the servo (in duty cycle)
        self.period = [-1, 1, .5, .2, .1] # period presets
        self.index = 0 # start at 0 speed

"""The inherited run method from threading.Thread. This runs on
thread.start() call

This loops through the oar motion"""
    def run(self):
        # move the oar back and forth unless self.index = 0
        try:
            while True:
                if self.index != 0:
                    # forward motion
                    for i in np.linspace(0, 1, 10):
                        # leave loop if self.index changes to 0, but complete loop
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[self.index]/10)
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[1]/10) # complete loop at slowest speed after ValueError
                        except KeyboardInterrupt:
                            self.pwm.stop()
                            GPIO.cleanup()
                            raise KeyboardInterrupt
                    # backward motion
                    for i in np.linspace(1, 0, 10):
                        # leave loop if self.index changes to 0, but complete loop
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[self.index]/10)
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*i)
                            time.sleep(self.period[1]/10) # complete loop at slowest speed after ValueError
                        except KeyboardInterrupt:
                            self.pwm.stop()
                            GPIO.cleanup()
                            raise KeyboardInterrupt

                        
                else:
                    time.sleep(.1)
                    self.pwm.ChangeDutyCycle(self.center)
            
        except KeyboardInterrupt:
            print("servo interrupted")
            self.pwm.stop()
            GPIO.cleanup()
            raise KeyboardInterrupt
"""update the index for the self.rest list. This dictates which speed
preset the stepper will rotate

pm is either +1 for increase speed or 0 for decrease speed"""
    def updateSpeed(self, pm):
        if pm == 1 and self.index < 4:
            self.index += 1
        elif pm == 0 and self.index >0:
            self.index -= 1

"""return self.index"""
    def getIndex(self):
        return self.index

"""set self.index"""
    def setIndex(self, ind):
        self.index = ind
