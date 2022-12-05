import threading
import time
import numpy as np
import RPi.GPIO as GPIO

class Servo(threading.Thread):
    def __init__(self, center, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)
        self.center = center


        self.pin = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)

        self.pwm.start(self.center)

        self.range = 2
        self.period = [-1, 3, 2, 1, .5]
        self.index = 0
        
    def run(self):
        try:
            while True:
                if self.index != 0:
                    self.cycle()
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
    def updateRange(self, ranger):
        self.range = ranger
    def cycle(self):
        for i in np.linspace(0, 2*np.pi, 1000):
            try:
                self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i))
                time.sleep(self.period[self.index]/1000)
            except ValueError:
                self.pwm.ChangeDutyCycle(self.center - self.range*np.sin(i))
                time.sleep(self.period[1]/1000)
                #print("negative sleep")
