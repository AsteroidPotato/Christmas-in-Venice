import numpy as np
import time
from servo_thread import Servo
import RPi.GPIO as GPIO

test = Servo(7)

test.start()
try:
    while True:
        test.index = int(input("index:"))
except:
    test.pwm.stop()
    GPIO.cleanup()
