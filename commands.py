import numpy as np
import time
import subprocess,os
from subprocess import call
from stepper_thread import Stepper
from servo_thread import Arm
from HT_thread import HT
from fish_thread import Fish
import RPi.GPIO as GPIO

speed_dict = {"faster": 1, "rockier" : 1, "slower": 0, "calmer": 0}
pin = 26
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

motor = GPIO.PWM(pin, 50)
stepper = Stepper()
stepper.start()
fish = Fish(11, 10, 5)
fish.start()
ht = HT(5.7, 13)
ht.start()
oar = Arm(7, 19)
oar.start()

def changeRowSpeed(update):
    if update["com"] == "Santa":
        stepper.updateSpeed(speed_dict[update["speed"]])
        oar.updateSpeed(speed_dict[update["speed"]])
    if ht.getIndex() == 0 and stepper.getIndex() != 0:
        ht.setIndex(1)
    if stepper.getIndex() == 0 and ht.getIndex() != 0:
        ht.setIndex(0)
 
def changeFishState(update):
    if update["com"] == "fish":
        if speed_dict[update["swim"]] == 1:
            fish.runvar = 1
        else:
            fish.runvar = 0

def changeWaterState(update):
    if update["com"] == "Santa":
        ht.updateSpeed(speed_dict[update["rock"]])
    if stepper.getIndex() == 0:
        ht.setIndex(0)
        
def sayHI(update):
    os.system('mpg321 SantaHoHoHo.mp3 &')
