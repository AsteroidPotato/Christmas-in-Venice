import numpy as np
import time
import subprocess,os
from subprocess import call
import RPi.GPIO as GPIO

### IMPORT ALL DEVICE CLASSES ###
from stepper_thread import Stepper
from servo_thread import Arm
from HT_thread import HT
from fish_thread import Fish

speed_dict = {"faster": 1, "rockier" : 1, "slower": 0, "calmer": 0} # this dictionary takes speed phrases and converts them to 1 or 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

### INITIALIZE AND START ALL THREADS ###
stepper = Stepper()
stepper.start()

fish = Fish(11, 10, 5) # center, range, pin
fish.start()

ht = HT(5.7, 13) # center, pin
ht.start()

oar = Arm(7, 19) # center, pin
oar.start()

""" Change translational speed and oar speed """
def changeRowSpeed(update):
    if update["com"] == "Santa":
        stepper.updateSpeed(speed_dict[update["speed"]])
        oar.updateSpeed(speed_dict[update["speed"]])

    # This makes it so that the high-torque rocking and the stepper/oar must be on or off at the same time. Speed can be changed thereafter
    if ht.getIndex() == 0 and stepper.getIndex() != 0:
        ht.setIndex(1)
    if stepper.getIndex() == 0 and ht.getIndex() != 0:
        ht.setIndex(0)
 
""" Turn on or off fish """
def changeFishState(update):
    if update["com"] == "fish":
        if speed_dict[update["swim"]] == 1:
            fish.runvar = 1
        else:
            fish.runvar = 0

""" Make the high-torque servo rock the boat faster or slower """
def changeWaterState(update):
    if update["com"] == "Santa":
        ht.updateSpeed(speed_dict[update["rock"]])

    # This makes it so that the high-torque rocking and the stepper/oar must be on or off at the same time. Speed can be changed thereafter
    if stepper.getIndex() == 0:
        ht.setIndex(0)

""" Play audio recording of Santa """       
def sayHI(update):
    if update["com"] == "Santa":
        os.system('mpg321 SantaHoHoHo.mp3 &') # run the audio file with mpg321
