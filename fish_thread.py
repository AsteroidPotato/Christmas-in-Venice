import threading
import time
import numpy as np
import RPi.GPIO as GPIO


class Fish(threading.Thread):
	def __init__(self, center, ranger, pin, *args, **kwargs):
		threading.Thread.__init__(self)
		self._args = args
		self._kwargs = kwargs
		self._lock = kwargs.get("lock", None)
		self.center = center


		self.pin = pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pin, 50)

		self.pwm.start(self.center)

		self.range = ranger
		self.period = .5
		self.runvar = 0
	def run(self):
		try:
			while True:
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
	
