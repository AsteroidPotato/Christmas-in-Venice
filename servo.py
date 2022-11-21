import numpy as np
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 50)

pwm.start(1.4)
time.sleep(1)

"""Collect data for fit"""
for i in np.linspace(1.4, 12.4, 12): #increment i by 1 between 1.4 and 12.4
	pwm.ChangeDutyCycle(i) #change the duty cycle 
	time.sleep(5) #give me enough time to record the angle
	print(i)

t=input("what angle? ") #user inputs angle in degrees
pwm.ChangeDutyCycle(1.5+float(t)/17.8) #sets the duty cycle according to equation (1)
time.sleep(5)
pwm.ChangeDutyCycle(1.4)
time.sleep(1)

pwm.stop()
GPIO.cleanup()

