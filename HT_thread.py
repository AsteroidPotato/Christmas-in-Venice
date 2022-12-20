import threading
import time
import numpy as np
import RPi.GPIO as GPIO

"""Class to run the high-torque servo that rocks the gondola"""
class HT(threading.Thread):
    
"""center is the duty cycle value for the servo's center mark
pin is the GPIO pin for the servo"""
    def __init__(self, center, pin, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

        self.center = # centered duty cycle calibrated to each servo
        self.pin = pin # GPIO pin for servo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.center)

        self.range = .5 # range of motion for the servo (in duty cycle)
        self.period = [-1, 3, 2, 1, .5] # period presets
        self.index = 0 # start at 0 speed


"""The inherited run method from threading.Thread. This runs on
thread.start() call

This loops through the rocking motion"""      
    def run(self):
        try:
            # rock the boat back and forth unless self.index = 0
            while True:
                if self.index != 0:
                    for i in np.linspace(0, 2*np.pi, 100):
                        try:
                            self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i)) # rock with steps defined via sinusoidal function
                            time.sleep(self.period[self.index]/100)
                        # if self.index == 0 during the loop, catch ValueError, and slowly return boat to initial position
                        except ValueError:
                            self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i))
                            time.sleep(self.period[1]/100)
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
        if pm == 1 and self.index < 5:
            self.index += 1
        elif pm == 0 and self.index >1:
            self.index -= 1

"""return self.index"""
    def getIndex(self):
        return self.index

"""set self.index"""
    def setIndex(self, ind):
        self.index = ind
