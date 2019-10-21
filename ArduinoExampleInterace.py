from arduino import Arduino
import time
import logging
import threading

b = Arduino('/dev/ttyUSB0')
pin = 9

#declare output pins as a list/tuple
b.output([pin])

for xrange(10):
    b.setHigh(pin)
    time.sleep(1)
    print b.getState(pin)
    b.setLow(pin)
    print b.getState(pin)
    time.sleep(1)

b.close()


class MotorController():
    __init__(self):
        self.leftEyeTheta = 0
        self.leftEyePhi = 0
        self.rightEyeTheta = 0
        self.rightEyePhi = 0
        self.maxDegree = 180



#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  myservo.write(val);                  // sets the servo position according to the scaled value
  delay(15);                           // waits for the servo to get there
}
