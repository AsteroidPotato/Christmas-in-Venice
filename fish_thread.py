import threading
import time
import numpy as np
import RPi.GPIO as GPIO

"""Class to rotate the fish servo back and forth"""
class Fish(threading.Thread):
        """center is the duty cycle value for the servo's center mark
        pin is the GPIO pin for the servo
        ranger is the range of motion"""
	def __init__(self, center, ranger, pin, *args, **kwargs):
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

		self.range = ranger # range of motion for the servo (in duty cycle)
		self.period = .5 # speed of servo
		self.runvar = 0 # start with no rotation

"""The inherited run method from threading.Thread. This runs on
thread.start() call

This loops through the rocking motion"""
	def run(self):
		try:
			while True:
                                # while the self.runvar == 1, rock back and forth
				while self.runvar:
					for i in np.linspace(0, 1, 10):
						try:
							self.pwm.ChangeDutyCycle(self.center - self.range*i)
							time.sleep(self.period/10)
						except KeyboardInterrupt:
							self.pwm.stop()
							GPIO.cleanup()
							raise KeyboardInterrupt
					for i in np.linspace(1, 0, 10):
						try:
							self.pwm.ChangeDutyCycle(self.center - self.range*i)
							time.sleep(self.period/10)
					
						except KeyboardInterrupt:
							self.pwm.stop()
							GPIO.cleanup()
							raise KeyboardInterrupt

				while self.runvar == 0:
					continue
		except KeyboardInterrupt:
			print("fish interrupted")
			self.pwm.stop()
			GPIO.cleanup()
			raise KeyboardInterrupt
	
