// Main Arduino code for a 6-dof Stewart platform.
// Written for the Ruggeduino Controller. Arduino Mega.
// Schematic and PCB Designs are also included in the repository. An online version is available at https://easyeda.com/editor#id=b51efcbcc5cc493f94a94739c4155136

#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h>
#include "SparkFun_BNO080_Arduino_Library.h"

BNO080 myIMU;

// Direction pins
#define DIR_A1_PIN 43
#define DIR_A2_PIN 45
#define DIR_A3_PIN 30
#define DIR_A4_PIN 28
#define DIR_A5_PIN 31
#define DIR_A6_PIN 33

#define DIR_B1_PIN 41
#define DIR_B2_PIN 35
#define DIR_B3_PIN 32
#define DIR_B4_PIN 38
#define DIR_B5_PIN 29
#define DIR_B6_PIN 23

// PWM pins
#define PWM_PIN_1 13
#define PWM_PIN_2 12
#define PWM_PIN_3 11
#define PWM_PIN_4 10
#define PWM_PIN_5 9
#define PWM_PIN_6 8

// PA-14P potentiometer pins
#define POT_PIN_1 A13
#define POT_PIN_2 A12
#define POT_PIN_3 A3
#define POT_PIN_4 A0
#define POT_PIN_5 A7
#define POT_PIN_6 A4

// Enable for all motors (grouped as such due to different H-bridge controllers)
#define EN_PIN_1 A15
#define EN_PIN_2 A14
#define EN_PIN_3 A2
#define EN_PIN_4 A1
#define EN_PIN_5 A10
#define EN_PIN_6 A11

// Platform parameters
#define NUM_MOTORS 6

// Actuator value bounds
#define MIN_POS 0
#define MAX_POS 50
#define MIN_PWM 0
#define MAX_PWM 255
#define MAX_MOVE_TIME 3500
#define MIN_MOVE_TIME 0

#define IDLE 0
#define EXTEND 1
#define RETRACT 2

// Default platform calibration settings (average analog values at extrema for each actuator)
unsigned long move_times[NUM_MOTORS];
unsigned long previousMillis[NUM_MOTORS];
unsigned long currentMillis = 0;

// Pin group arrays
const uint8_t DIR_A_PINS[NUM_MOTORS] = { DIR_A1_PIN, DIR_A2_PIN, DIR_A3_PIN, DIR_A4_PIN, DIR_A5_PIN, DIR_A6_PIN };
const uint8_t DIR_B_PINS[NUM_MOTORS] = { DIR_B1_PIN, DIR_B2_PIN, DIR_B3_PIN, DIR_B4_PIN, DIR_B5_PIN, DIR_B6_PIN };
const uint8_t PWM_PINS[NUM_MOTORS]   = { PWM_PIN_1, PWM_PIN_2, PWM_PIN_3, PWM_PIN_4, PWM_PIN_5, PWM_PIN_6 };
const uint8_t POT_PINS[NUM_MOTORS]   = { POT_PIN_1, POT_PIN_2, POT_PIN_3, POT_PIN_4, POT_PIN_5, POT_PIN_6 };
const uint8_t EN_PINS[NUM_MOTORS]    = { EN_PIN_1, EN_PIN_2, EN_PIN_3, EN_PIN_4, EN_PIN_5, EN_PIN_6 };

// Serial configuration parameters
#define BAUD_RATE 115200  // baud rate for serial port (also needs to be set on host side)

// Serial input parameters
#define INPUT_TRIGGER 11   // at minimum, 6 numbers + 5 spaces

// Actuator variables
uint8_t pwm[NUM_MOTORS];            // current PWM for each actuator

// Position variables
long pos[NUM_MOTORS];            // current position (measured by analog read) of each actuator
long pos_converted[NUM_MOTORS];
int16_t pos_buffer[NUM_MOTORS];
int16_t input[NUM_MOTORS];          // intermediate input retrieved from the serial buffer
long desired_pos[NUM_MOTORS];   // desired (user-inputted and validated) position of each actuator
long total_diff[NUM_MOTORS];     // cumulative position difference for each actuator; for integral gain
int16_t actuator_state[NUM_MOTORS];
const int16_t rate_of_pos_change = 2;

// Time variables (for printing)
unsigned long current_time;         // current time (in millis); used to measure difference from previous_time
unsigned long previous_time;        // last recorded time (in millis); measured from execution start or last print

// Iterator/sum variables
uint8_t motor;                      // used to iterate through actuators by their indexing (0 to NUM_MOTORS - 1)

//IMU Variables
float roll       = 0.0;
float roll_corr  = 0.0;
float roll_val   = 0.0;
float pitch      = 0.0;
float pitch_corr = 0.0;
float pitch_val  = 0.0;
float yaw        = 0.0;
float yaw_corr   = 0.0;
float yaw_val    = 0.0;
float X; 
float Y;
float Z;
byte linAccuracy;


void setup() //Runs once at initialization; set up input and output pins and variables.
{ 
  // Initialize pins
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      // We ae setting up the motor direction pins as output and then setting them as LOW
      pinMode(DIR_A_PINS[motor], OUTPUT);
      digitalWrite(DIR_A_PINS[motor], LOW);

      pinMode(DIR_B_PINS[motor], OUTPUT);
      digitalWrite(DIR_B_PINS[motor], LOW);

      // We are setting up the Speed control of the motors as Output and Setting the value to LOW
      pinMode(PWM_PINS[motor], OUTPUT);
      analogWrite(PWM_PINS[motor], 0);

      // We are setting up all the motor/actuator enable pins as output and setting it to the Value LOW
      pinMode(EN_PINS[motor], OUTPUT);

      // We are setting up the potentiometer pins as input
      pinMode(POT_PINS[motor], INPUT);
    }

    
    for (motor = 0; motor < NUM_MOTORS; ++motor) // For safety, set initial actuator settings and speed to 0
    {
        total_diff[motor] = 0;
        desired_pos[motor] = 0;
        pos[motor] = 0;
        pwm[motor] = MIN_PWM;
    }

    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      digitalWrite(EN_PINS[motor], HIGH);
    }

    startup(motor);

    // Initialize serial communication
    Serial.begin(BAUD_RATE);
    
    Wire.begin();
    if (myIMU.begin() == false)
    {
    Serial.println("BNO080 not detected at default I2C address. Check your jumpers and the hookup guide. Freezing...");
    while (1);
    }
    Wire.setClock(400000); //Increase I2C data rate to 400kHz
    myIMU.enableRotationVector(50); //Send data update every 50ms
    myIMU.enableLinearAccelerometer(50);
 }


void loop()   // Main loop. Run tasks in an infinite loop.
{  

  //If there is an incoming data packet from the computer, call the readEthernet function
  EthernetClient client = Serial.available();
  if ( Serial.available())
  {
    readSerial();
  }
  
  //Look for reports from the IMU
  if (myIMU.dataAvailable() == true)
  {
    X = myIMU.getLinAccelX();
    Y = myIMU.getLinAccelY();
    Z = myIMU.getLinAccelZ();
    linAccuracy = myIMU.getLinAccelAccuracy();

    pitch = (myIMU.getRoll()) * 180.0 / PI; // Convert roll to degre
    pitch_val = pitch - pitch_corr;
    roll = (myIMU.getPitch()) * 180.0 / PI; // Convert pitch to degrees
    roll_val = roll - roll_corr;
    yaw = (myIMU.getYaw()) * 180.0 / PI; // Convert yaw / heading to degrees
    yaw_val = yaw - yaw_corr;


  }  

  // For each actuator, set movement parameters (direction, PWM) and execute motion
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    move(motor);
  }

  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    pos[motor] = map(pos_converted[motor], 0, 3500, 0, 50);
  }

}


inline void disableallactuators()
{
    for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(EN_PINS[motor], LOW);
  }
}

inline void enableallactuators()
{
    for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(EN_PINS[motor], HIGH);
  }
}

inline void levelplatform()
{
 
}

void currentPosition()
{

}

inline void readSerial()  //Read serial input and set desired positions.
{ 
  EthernetClient client = Serial.available();
  char incomingByte = Serial.read();
  
  if (incomingByte == 'A')
  {
      // Parse ints from serial
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      input[motor] = Serial.parseInt();
    }
    // Check that inputs are valid
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      if (input[motor] > MAX_POS)
      {
        return;
      }
      else if (input[motor] < MIN_POS)
      {
        return;
      }
    }

    // Set the input as the desired positions
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      desired_pos[motor] = input[motor];
      previousMillis[motor] = millis();    
    }
  }

  else if (incomingByte == 'Q')
  {
    disableallactuators();
    return;
  }
  else if (incomingByte == 'E')
  {
    calibrateIMU();
    return;
  }
  else if (incomingByte == 'I')
  {
    levelplatform();
    return;
  }
  else if (incomingByte == 'F')
  {
    basePosition(client);
    return;
  }
  else if (incomingByte == 'H')
  {
    enableallactuators();
    return;
  }
}

inline void calibrateIMU()
{
  pitch_corr = 0.0;
  roll_corr = 0.0;
  yaw_corr = 0.0;
  pitch_corr = pitch_corr + pitch;
  roll_corr = roll_corr + roll;
  yaw_corr = yaw_corr + yaw;
}

void basePosition(EthernetClient client)
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    desired_pos[motor] = 0;
  }
}

inline void startup(uint8_t motor)
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(DIR_A_PINS[motor], HIGH);
    digitalWrite(DIR_B_PINS[motor], LOW);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
  delay(1000);
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(DIR_A_PINS[motor], LOW);
    digitalWrite(DIR_B_PINS[motor], LOW);
    analogWrite(PWM_PINS[motor], MIN_PWM);
  }
}


inline void move(uint8_t motor)
{


    if (pos[motor] > desired_pos[motor])
    {
      actuator_state[motor] = RETRACT;
    }
    else if (pos[motor] < desired_pos[motor])
    {
      actuator_state[motor] = EXTEND;
    }
    else
    {
      actuator_state[motor] = IDLE;
    }

    total_diff[motor] = abs(desired_pos[motor] = pos[motor]);
    pos_converted[motor] = map(pos[motor], MIN_POS, MAX_POS, MIN_MOVE_TIME, MAX_MOVE_TIME);


    switch (actuator_state[motor]) 
    {
      case 0:
        // Idle state
        digitalWrite(DIR_A_PINS[motor], LOW);
        digitalWrite(DIR_B_PINS[motor], LOW);
        analogWrite(PWM_PINS[motor], 0);
        break;
      case 1:
        // Extend
        digitalWrite(DIR_A_PINS[motor], LOW);
        digitalWrite(DIR_B_PINS[motor], HIGH);
        analogWrite(PWM_PINS[motor], MAX_PWM);
      case 2:
        // Retract
        digitalWrite(DIR_A_PINS[motor], HIGH);
        digitalWrite(DIR_B_PINS[motor], LOW);
        analogWrite(PWM_PINS[motor], MAX_PWM);
    }

  

    move_times[motor] = map(total_diff[motor], MIN_POS, MAX_POS, MIN_MOVE_TIME, MAX_MOVE_TIME);
  
  
    currentMillis = millis();


    if (total_diff[motor] == 0)
    {
      return;
    }
    else
    {
      if(currentMillis - previousMillis[motor] < move_times[motor])
      {
        if(pos[motor] > desired_pos[motor])
        {
          pos_converted[motor] = pos_converted[motor] - rate_of_pos_change;
        }
        else if (pos[motor] < desired_pos[motor])
        {
          pos_converted[motor] = pos_converted[motor] + rate_of_pos_change;
        }
      }
    }
  
}