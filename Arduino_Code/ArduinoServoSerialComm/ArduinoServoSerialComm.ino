/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.
 
 modified 8 Nov 2022
 by Amaan
 http://www.arduino.cc/en/Tutorial/Sweep
*/
 
#include <Servo.h>

int x;
 
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
 
int pos = 0;    // variable to store the servo position
int tmp = -1;
 
void setup() 
{
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  Serial.setTimeout(1);
}
 
void loop() 
{
  while (!Serial.available());
  x = Serial.readString().toInt();

  if (x != tmp)
  {
    tmp = x;

    myservo.write(x);
    delay(20);
  }
  
}
