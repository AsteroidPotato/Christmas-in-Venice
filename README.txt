### RUNNING THE CODE ###

vcpp.py is the main python file. This manages all the other files and classes. Run it to run the whole code.

vcpp.py prints some debug messages to the terminal. These will print either on system interrupt, or when the pi hears speech that it understands as a command. In this second case, it will print the update dictionary that it passes to the intent function.

### NON-STANDARD DEPENDENCIES ###

Requires RPi.GPIO
Requires pvrhino
Requires pyaudio

Requires mpg321


### DESIGN CHOICES ###

I initially had all the servo objects distinct instances of the same class. I ran into a bug. In the process of debugging the bug, I separated each of these iterations into separate classes. This is a little less clean, and ultimately it wasn't the source of the bug (which was due to there being no rest time in the holding while loop for the servos). I fixed the bug, but since I had already separated them into three different classes, I decided not to recombine them. 

### DEVICE CLASSES ###

Each device class (Stepper, Arm, HT, Fish) are subclasses of the threading class. This allowed me to implement multithreading, and run each of these actions in parallel. When the thread is started by a call to foo.start(), the foo.run() method is called. Each of these threads run continuously, until a KeyboardInterrupt is thrown.

### VOICE COMMAND LOGIC ###

changeRowState will be called on "Santa go/row (the boat/the gondola) faster/slower" with the dictionary {"com":"Santa", "speed":"faster/slower"} passed as the update

changeWaterState will be called on "Santa rock (the boat/the gondola) faster/slower" or "Santa rockier/calmer" with the dictionary {"com":"Santa", "rock":"faster/slower"} passed as the update

changeFishState will be called on "Fish swim/jump faster/slower" with the dictionary {"com":"fish", "swim":"faster/slower"} passed as the update

sayHi will be called on "Santa say/speak (hi/hello/hey)" with the dictionary {"com":"Santa"} passed as the update



