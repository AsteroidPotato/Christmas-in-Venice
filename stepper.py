import numpy as np
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pins = [17, 27, 22, 23] #the pins that control the coils


GPIO.setup(pins, GPIO.OUT)

lor = -1 #clockwise or anticlockwise
nsteps = 400 #total number of steps per trial
rest = .01 #rest time between steps

initial_time = time.time()
#full step
for i in range(nsteps): #loop through the number of steps int nsteps
	GPIO.output(pins, GPIO.LOW) #reset all of our pins in list pins
	GPIO.output(pins[0], GPIO.HIGH) #raise two pins
	GPIO.output(pins[3], GPIO.HIGH)
	pins = np.roll(pins, lor).tolist() #rotate the list in the direction of lor = +/- 1
	time.sleep(rest) #wait rest time between steps
total_time = time.time()-initial_time #how we find the period
nrevs = nsteps/200 #we calculate how many revolutions there are

#print all the output stuff (full step)
print("\nfull step report:\n")
print(f"total number of steps: {nsteps}")
print(f"number of revolutions: {nrevs}")
print(f"total time: {total_time}")
print(f"period: {total_time/nrevs}")
print(f"frequency: {nrevs/total_time}")
print("turning degrees per step: 1.8")


#half step
initial_time = time.time()

for i in range(nsteps):
	GPIO.output(pins, GPIO.LOW)
	GPIO.output(pins[0], GPIO.HIGH)
	time.sleep(rest/2) # add a rest between the pin raising
	GPIO.output(pins[1], GPIO.HIGH)
	pins = np.roll(pins, lor).tolist()
	time.sleep(rest/2)
total_time = time.time()-initial_time
nrevs = nsteps/200

#print all the output stuff (half step)
print("\nhalf step report:\n")
print(f"total number of steps: {2*nsteps}")
print(f"number of revolutions: {nrevs}")
print(f"total time: {total_time}")
print(f"period: {total_time/nrevs}")
print(f"frequency: {nrevs/total_time}")
print("turning degrees per step: 0.9")
