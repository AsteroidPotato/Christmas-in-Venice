import numpy as np
import time
from stepper_thread import Stepper
from servo_thread import Servo
import RPi.GPIO as GPIO

speed_dict = {"faster": 1, "rockier" : 1, "slower": 0, "calmer": 0}
pin = 26
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

motor = GPIO.PWM(pin, 50)
stepper = Stepper()
stepper.start()
ht = Servo(7)
ht.start()


def changeRowSpeed(update):
    print("changeRowSpeed called")
    if update["com"] == "Santa":
        stepper.updateSpeed(speed_dict[update["speed"]])
def changeFishState(update):
    motor.ChangeDutyCycle(30)

def changeWaterState(update):
    print("changeWaterState called")
    if update["com"] == "Santa":
        #print("correct commander")
        ht.updateSpeed(speed_dict[update["rock"]])
def sayHI(update):
    pass
