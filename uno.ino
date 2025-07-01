#include <Servo.h>
#include "secret.h"

Servo servo;  // create servo object to control a servo
bool shouldDispense = false; 

void setup() {
  servo.attach(9);  // attaches the servo on pin 9 to the servo objectư
  servo.write(180);   // rotate slowly servo to 90 degrees immediately
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      shouldDispense = true;
      Serial.println("shouldDispense set to true");
    }
  }

  if (shouldDispense) {
    servo.write(90);   // move servo
    delay(10000);       // hold position
    servo.write(180);    // return servo
    shouldDispense = false;  // reset flag
    Serial.println("Servo action completed");
  }
}
