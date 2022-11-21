import numpy as np
import time
from stepper_thread import Stepper

test = Stepper()

test.start()

while True:
    test.rest = float(input("rest step:"))