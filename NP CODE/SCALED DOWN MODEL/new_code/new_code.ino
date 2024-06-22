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
#define MIN_POS -50
#define MAX_POS 50
#define MIN_PWM 0
#define MAX_PWM 255
#define INPUT_TRIGGER 11

// Serial configuration parameters
#define BAUD_RATE 115200  // baud rate for serial port (also needs to be set on host side)

// Pin group arrays
const uint8_t DIR_A_PINS[NUM_MOTORS] = { DIR_A1_PIN, DIR_A2_PIN, DIR_A3_PIN, DIR_A4_PIN, DIR_A5_PIN, DIR_A6_PIN };
const uint8_t DIR_B_PINS[NUM_MOTORS] = { DIR_B1_PIN, DIR_B2_PIN, DIR_B3_PIN, DIR_B4_PIN, DIR_B5_PIN, DIR_B6_PIN };
const uint8_t PWM_PINS[NUM_MOTORS]   = { PWM_PIN_1, PWM_PIN_2, PWM_PIN_3, PWM_PIN_4, PWM_PIN_5, PWM_PIN_6 };
const uint8_t EN_PINS[NUM_MOTORS]    = { EN_PIN_1, EN_PIN_2, EN_PIN_3, EN_PIN_4, EN_PIN_5, EN_PIN_6 };

// Position variables
long pos[NUM_MOTORS];           // current position (measured by analog read) of each actuator
long desired_pos[NUM_MOTORS];   // desired (user-inputted and validated) position of each actuator
long pos_diff[NUM_MOTORS];
unsigned long delay_times[NUM_MOTORS];
int16_t input[NUM_MOTORS];
float rotation_matrix[3][3];
uint8_t motor; 
int command = 0;
unsigned long startTime;

float pitch = 0;
float yaw =   0;
float roll =  0;
float heave = 0;
float sway =  0;
float surge = 0;

float base_joints[6][4] = {
    {180,  -65,  0, 1},
    {-34, -188, 0, 1},
    {-146, -123, 0, 1},
    {-146,  123, 0, 1},
    {-34,  188, 0, 1},
    {180,   65,  0, 1}
};

float platform_joints[6][4] = 
    {{108,  -95, 0, 1},
     {28,   -141, 0, 1},
     {-137, -46,  0, 1},
     {-137,  46,  0, 1},
     {28,    141, 0, 1},
     {108,   95, 0, 1}};

void setup() {

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
    analogWrite(PWM_PINS[motor], MIN_PWM);

    // We are setting up all the motor/actuator enable pins as output and setting it to the Value LOW
    pinMode(EN_PINS[motor], OUTPUT);
    digitalWrite(EN_PINS[motor], HIGH);
  }

  for (motor = 0; motor < NUM_MOTORS; ++motor) // For safety, set initial actuator settings and speed to 0
  {
    desired_pos[motor] = 0;
    pos[motor] = 0;
    pos_diff[motor] = 0;
  }

  // Start serial communication at a baud rate of 9600
  Serial.begin(BAUD_RATE);
}

void loop() {

  if (Serial.available() >= INPUT_TRIGGER)
  {
    readSerial();
    update_platform();
    startTime = millis();
  }
  // down();
  //up();
  move();
}


/*
 * Read and parse serial input into actuator positions.
 */
inline void readSerial()
{

  // Parse ints from serial
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    pos[motor] = desired_pos[motor];
    input[motor] = Serial.parseInt();
  }

  // Check that inputs are valid
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    if (input[motor] < MIN_POS || input[motor] > MAX_POS)
    {
      return;
    }
  }

  yaw   = input[0];
  pitch = input[1];
  roll  = input[2];
  heave = input[3];
  sway  = input[4];
  surge = input[5];
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
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            temp_matrix[i][j] = 0;
            for (int k = 0; k < 3; ++k) {
                temp_matrix[i][j] += yaw_matrix[i][k] * pitch_matrix[k][j];
            }
        }
    }

    // Perform matrix multiplication: temp_matrix * roll_matrix
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            rotation_matrix[i][j] = 0;
            for (int k = 0; k < 3; ++k) {
                rotation_matrix[i][j] += temp_matrix[i][k] * roll_matrix[k][j];
            }
        }
    }
}

void update_platform() {
  // Serial.print(yaw);   Serial.print("   ");
  // Serial.print(pitch); Serial.print("   ");
  // Serial.print(roll);  Serial.print("   ");
  // Serial.print(heave); Serial.print("   ");
  // Serial.print(sway);  Serial.print("   ");
  // Serial.print(surge); Serial.print("   ");
  // Serial.println();

  euler_to_rotation_matrix(yaw, pitch, roll);

  // // Print the matrix to the Serial Monitor
  // for (int i = 0; i < 3; i++) { // Iterate over rows
  //   for (int j = 0; j < 3; j++) { // Iterate over columns
  //     Serial.print(rotation_matrix[i][j]);
  //     Serial.print(" "); // Print a space between numbers
  //   }
  //   Serial.println(); // Move to the next line after printing each row
  // }

  float transformation_matrix[4][4] = {0};
  // Copy rotation matrix to transformation matrix
  for (int i = 0; i < 3; ++i) {
    for (int j = 0; j < 3; ++j) {
      transformation_matrix[i][j] = rotation_matrix[i][j];
    }
  }
  // Add translation components
  transformation_matrix[0][3] = surge;
  transformation_matrix[1][3] = sway;
  transformation_matrix[2][3] = heave;
  transformation_matrix[3][3] = 1;

  float platform_joints_transformed[6][4]; // Corrected array size for proper matrix multiplication
  // Transform platform joints
  for (int i = 0; i < 6; ++i) {
    for (int j = 0; j < 4; ++j) {
      platform_joints_transformed[i][j] = 0;
      for (int k = 0; k < 4; ++k) {
        platform_joints_transformed[i][j] += transformation_matrix[j][k] * platform_joints[i][k];
      }
      if (j == 2) {
        platform_joints_transformed[i][j] += 240;
      }
    }
  }

  float actuator_lengths[6];
  // Calculate actuators' lengths
  for (int i = 0; i < 6; ++i) {
    float x = platform_joints_transformed[i][0] - base_joints[i][0];
    float y = platform_joints_transformed[i][1] - base_joints[i][1];
    float z = platform_joints_transformed[i][2] - base_joints[i][2];
    actuator_lengths[i] = sqrt(x*x + y*y + z*z)-240;
    actuator_lengths[i] = map(actuator_lengths[i], 12, 60, 0, 50);
    // Further processing of actuator lengths (interpolation, absolute value) can be done here
  }

    // Set the input as the desired positions
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    desired_pos[motor] = actuator_lengths[motor];
    pos_diff[motor] = abs(desired_pos[motor] - pos[motor]);  // reset integral feedback given a new target
    delay_times[motor] = map(pos_diff[motor], 0, 50, 0, 3300);
  }

  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    Serial.print(desired_pos[motor]);
    Serial.print("   ");
  }
  Serial.println();
}


// inline void move()
// {
//   for (motor = 0; motor < NUM_MOTORS; ++motor)
//   {
//     if(pos[motor] < desired_pos[motor])
//     {
//       //EXTEND
//       digitalWrite(DIR_A_PINS[motor], HIGH);
//       digitalWrite(DIR_B_PINS[motor], LOW);
//     }
//     else if(pos[motor] > desired_pos[motor])
//     {
//       //RETRACT
//       digitalWrite(DIR_A_PINS[motor], LOW);
//       digitalWrite(DIR_B_PINS[motor], HIGH);
//     }
//   }

//   for (motor = 0; motor < NUM_MOTORS; ++motor)
//   {
//     if(pos[motor] != desired_pos[motor])
//     {
//       analogWrite(PWM_PINS[motor], MAX_PWM);
//       delay(delay_times[motor]);
//       analogWrite(PWM_PINS[motor], MIN_PWM);
//       pos[motor] = desired_pos[motor];
//     }
//   }
// }

inline void move()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
   if(pos[motor] < desired_pos[motor])
    {
      move_up(motor);
    }
    else if(pos[motor] > desired_pos[motor])
    {
      move_down(motor);
    }
  }  

  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    if(pos_diff[motor] == 0)
    {
      pos[motor] = desired_pos[motor];
    }
  }
}

inline void move_up(int motor)
{
  if (millis() - startTime <= delay_times[motor])
  {
    digitalWrite(DIR_A_PINS[motor], HIGH);
    digitalWrite(DIR_B_PINS[motor], LOW);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
  else if (millis() - startTime > delay_times[motor])
  {
    analogWrite(PWM_PINS[motor], MIN_PWM);
    pos_diff[motor] = 0;
  }
}

inline void move_down(int motor)
{

  if (millis() - startTime <= delay_times[motor])
  {
    digitalWrite(DIR_A_PINS[motor], LOW);
    digitalWrite(DIR_B_PINS[motor], HIGH);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
  else if (millis() - startTime > delay_times[motor])
  {
    analogWrite(PWM_PINS[motor], MIN_PWM);
    pos_diff[motor] = 0;
  }

}

inline void up()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(DIR_A_PINS[motor], HIGH);
    digitalWrite(DIR_B_PINS[motor], LOW);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
}

inline void down()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(DIR_A_PINS[motor], LOW);
    digitalWrite(DIR_B_PINS[motor], HIGH);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
}