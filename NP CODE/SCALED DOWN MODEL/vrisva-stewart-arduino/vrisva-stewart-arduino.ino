// Main Arduino code for a 6-dof Stewart platform.
// Written for the Ruggeduino Controller. Arduino Mega.
// Schematic and PCB Designs are also included in the repository. An online version is available at https://easyeda.com/editor#id=b51efcbcc5cc493f94a94739c4155136

#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h>
#include "SparkFun_BNO080_Arduino_Library.h"
#include <math.h>
#include <stdlib.h>

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
#define INPUT_TRIGGER 11

// Assuming a maximum of 6 joints and 4 coordinates (x, y, z, w)
#define MAX_JOINTS 6
#define COORDINATES 4

#define PI 3.14159265358979323846

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
float roll_imu       = 0.0;
float roll_corr  = 0.0;
float roll_val   = 0.0;
float pitch_imu      = 0.0;
float pitch_corr = 0.0;
float pitch_val  = 0.0;
float yaw_imu        = 0.0;
float yaw_corr   = 0.0;
float yaw_val    = 0.0;
float X; 
float Y;
float Z;
byte linAccuracy;

// Assuming definitions for platform_joints and base_joints as global arrays
float yaw_current_value, pitch_current_value, roll_current_value;
float heave_current_value, sway_current_value, surge_current_value;
//int int_actuator_lengths[NUM_MOTORS]; // Assuming there are 6 actuators
float rotation_matrix[3][3];

float base_joints[MAX_JOINTS][COORDINATES] = {
    {407,  -80,  0, 1},
    {-135, -393, 0, 1},
    {-273, -313, 0, 1},
    {-273,  313, 0, 1},
    {-135,  393, 0, 1},
    {407,   80,  0, 1}
};

float platform_joints[MAX_JOINTS][COORDINATES] = 
    {{152,  -166, 0, 1},
     {68,   -215, 0, 1},
     {-220, -49,  0, 1},
     {-220,  49,  0, 1},
     {68,    215, 0, 1},
     {152,   166, 0, 1}};

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
  //readSerial();
      // Parse new serial input if enough is in the buffer (also sets desired position if input is valid)
  if (Serial.available() >= INPUT_TRIGGER)
  {
    readSerial();
  }
  update_platform();
  
  //Look for reports from the IMU
  if (myIMU.dataAvailable() == true)
  {
    X = myIMU.getLinAccelX();
    Y = myIMU.getLinAccelY();
    Z = myIMU.getLinAccelZ();
    linAccuracy = myIMU.getLinAccelAccuracy();

    pitch_imu = (myIMU.getRoll()) * 180.0 / PI; // Convert roll to degre
    pitch_val = pitch_imu - pitch_corr;
    roll_imu = (myIMU.getPitch()) * 180.0 / PI; // Convert pitch to degrees
    roll_val = roll_imu - roll_corr;
    yaw_imu = (myIMU.getYaw()) * 180.0 / PI; // Convert yaw / heading to degrees
    yaw_val = yaw_imu - yaw_corr;

    Serial.print(pitch_val);
    Serial.print("   ");
    Serial.print(roll_val);
    Serial.print("   ");
    Serial.print(yaw_val);
    Serial.print("   ");
    Serial.println();

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

inline void readSerial()  //Read serial input and set desired positions.
{ 
      // Parse ints from serial
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
        input[motor] = Serial.parseInt();
    }
 
    // Check that inputs are valid
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
        if (input[motor] < MIN_POS || input[motor] > 600)
        {
            return;
        }
    }
 
    yaw_current_value =   input[0];
    pitch_current_value = input[1];
    roll_current_value =  input[2];
    heave_current_value = input[3];
    sway_current_value =  input[4];
    surge_current_value = input[5];

}

inline void calibrateIMU()
{
  pitch_corr = 0.0;
  roll_corr = 0.0;
  yaw_corr = 0.0;
  pitch_corr = pitch_corr + pitch_imu;
  roll_corr = roll_corr + roll_imu;
  yaw_corr = yaw_corr + yaw_imu;
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

void euler_to_rotation_matrix(float yaw, float pitch, float roll) {
    // Convert angles from degrees to radians
    float yaw_rad = yaw * PI / 180.0;
    float pitch_rad = pitch * PI / 180.0;
    float roll_rad = roll * PI / 180.0;

    // Define rotation matrices
    float yaw_matrix[3][3] = {
        {cos(yaw_rad), -sin(yaw_rad), 0},
        {sin(yaw_rad), cos(yaw_rad), 0},
        {0, 0, 1}
    };

    float pitch_matrix[3][3] = {
        {cos(pitch_rad), 0, sin(pitch_rad)},
        {0, 1, 0},
        {-sin(pitch_rad), 0, cos(pitch_rad)}
    };

    float roll_matrix[3][3] = {
        {1, 0, 0},
        {0, cos(roll_rad), -sin(roll_rad)},
        {0, sin(roll_rad), cos(roll_rad)}
    };

    // Temporary matrix to store intermediate multiplication results
    float temp_matrix[3][3];

    // Perform matrix multiplication: yaw_matrix * pitch_matrix
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            temp_matrix[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                temp_matrix[i][j] += yaw_matrix[i][k] * pitch_matrix[k][j];
            }
        }
    }

    // Perform matrix multiplication: temp_matrix * roll_matrix
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            rotation_matrix[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                rotation_matrix[i][j] += temp_matrix[i][k] * roll_matrix[k][j];
            }
        }
    }

}

void update_platform() {
    float pitch = pitch_current_value;
    float yaw = yaw_current_value;
    float roll = roll_current_value;
    float heave = heave_current_value;
    float sway = sway_current_value;
    float surge = surge_current_value;

    euler_to_rotation_matrix(yaw, pitch, roll);

    float transformation_matrix[4][4] = {0};
    // Copy rotation matrix to transformation matrix
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            transformation_matrix[i][j] = rotation_matrix[i][j];
        }
    }
    // Add translation components
    transformation_matrix[0][3] = surge;
    transformation_matrix[1][3] = sway;
    transformation_matrix[2][3] = heave;
    transformation_matrix[3][3] = 1;

    float platform_joints_transformed[6][3]; // Assuming 6 platform joints
    // Transform platform joints
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 4; j++) {
            platform_joints_transformed[i][j] = 0;
            for (int k = 0; k < 4; k++) {
                platform_joints_transformed[i][j] += transformation_matrix[j][k] * platform_joints[i][k];
            }
            if (j == 2) {
                platform_joints_transformed[i][j] += 788.2;
            }
        }
    }

    float actuator_lengths[6];
    // Calculate actuators' lengths
    for (int i = 0; i < 6; i++) {
        float x = platform_joints_transformed[i][0] - base_joints[i][0];
        float y = platform_joints_transformed[i][1] - base_joints[i][1];
        float z = platform_joints_transformed[i][2] - base_joints[i][2];
        actuator_lengths[i] = sqrt(x*x + y*y + z*z) - 832.26;
        // Further processing of actuator lengths (interpolation, absolute value) can be done here
    }

    for (int i = 0; i < 6; i++) {
      actuator_lengths[i] = (int)actuator_lengths[i];
      desired_pos[i] = actuator_lengths[i];
    }


/*
    for (int i = 0; i < 6; i++) {
        Serial.print (actuator_lengths[i]); 
        Serial.print("  ");
    }
    Serial.println();
*/
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
    move_times[motor] = map(total_diff[motor], MIN_POS, MAX_POS, MIN_MOVE_TIME, MAX_MOVE_TIME);

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