#include <Servo.h>

// Pin initializations
int panServoPin = 9;

// Servos
Servo panServo;

// Serial Variables
char positioning[7];
byte flag;
char fire;
char pan_byte[4];
char tilt_byte[4];
int pan = 0;
int tilt = 0;


void setup() {
  
  // Initialize Serial communication
  Serial.begin(9600);
  Serial.println("Ready");
  
  // Initialize Servo pins
  panServo.attach(panServoPin);
}

void loop() {
  
  // Check to make sure that there is a full message
  if (Serial.available() >= 8) 
  {
    // Make sure that this is a firing command
    flag = Serial.read();
    if (flag == 'f')
    {
      // Step through all elements in the byte stream that are in an incident window
      pan = Serial.read();
      tilt = Serial.read();
      
      fire = Serial.read();
        
      // Print Pan integer
      Serial.print(pan); 
      Serial.println(' ');
    }
  }
  
  panServo.write(pan);
  
  delay(100);
}
