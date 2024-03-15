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

#define MIN_POS 0
#define MAX_POS 50

#define MIN_PWM 0
#define MAX_PWM 255

#define MAX_MOVE_TIME 3500
#define MIN_MOVE_TIME 0

// Serial configuration parameters
#define BAUD_RATE 115200  // baud rate for serial port (also needs to be set on host side)

// Serial input parameters
#define INPUT_TRIGGER 11   // at minimum, 6 numbers + 5 spaces

long pos[NUM_MOTORS]; 
long desired_pos[NUM_MOTORS]; 
long pos_diff[NUM_MOTORS]; 
int16_t input[NUM_MOTORS];
unsigned long delay_times[NUM_MOTORS];

// Iterator/sum variables
uint8_t motor;                      // used to iterate through actuators by their indexing (0 to NUM_MOTORS - 1)

// Pin group arrays
const uint8_t DIR_A_PINS[NUM_MOTORS] = { DIR_A1_PIN, DIR_A2_PIN, DIR_A3_PIN, DIR_A4_PIN, DIR_A5_PIN, DIR_A6_PIN };
const uint8_t DIR_B_PINS[NUM_MOTORS] = { DIR_B1_PIN, DIR_B2_PIN, DIR_B3_PIN, DIR_B4_PIN, DIR_B5_PIN, DIR_B6_PIN };
const uint8_t PWM_PINS[NUM_MOTORS]   = { PWM_PIN_1, PWM_PIN_2, PWM_PIN_3, PWM_PIN_4, PWM_PIN_5, PWM_PIN_6 };
const uint8_t EN_PINS[NUM_MOTORS]    = { EN_PIN_1, EN_PIN_2, EN_PIN_3, EN_PIN_4, EN_PIN_5, EN_PIN_6 };

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
    analogWrite(PWM_PINS[motor], 0);

    // We are setting up all the motor/actuator enable pins as output and setting it to the Value LOW
    pinMode(EN_PINS[motor], OUTPUT);
    digitalWrite(EN_PINS[motor], HIGH);
  }

  for (motor = 0; motor < NUM_MOTORS; ++motor) // For safety, set initial actuator settings and speed to 0
  {
    desired_pos[motor] = 0;
    pos[motor] = 0;
  }

  // Start serial communication at a baud rate of 9600
  Serial.begin(BAUD_RATE);
}

void loop() {
  if (Serial.available() >= INPUT_TRIGGER)
  {
    readSerial();
  }

  move();

  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    Serial.print(pos[motor]);
    Serial.print("   ");
  }
  Serial.println();
 
  //move_up();
  //move_down();
}

inline void readSerial()
{
    // Parse ints from serial
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
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
 
    // Set the input as the desired positions
    for (motor = 0; motor < NUM_MOTORS; ++motor)
    {
      desired_pos[motor] = input[motor];
      pos_diff[motor] = abs(desired_pos[motor] - pos[motor]);
      delay_times[motor] = map(pos_diff[motor], 0, 50, 0, 3500);
    }
}

inline void move()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
   if(pos[motor] < desired_pos[motor])
    {
      //EXTEND
      digitalWrite(DIR_A_PINS[motor], HIGH);
      digitalWrite(DIR_B_PINS[motor], LOW);
    }
    else if(pos[motor] > desired_pos[motor])
    {
      //RETRACT
      digitalWrite(DIR_A_PINS[motor], LOW);
      digitalWrite(DIR_B_PINS[motor], HIGH);
    }
    else
    {
      return;
    }
  }  

  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
   if(pos[motor] != desired_pos[motor])
    {
      analogWrite(PWM_PINS[motor], MAX_PWM);
      delay(delay_times[motor]);
      analogWrite(PWM_PINS[motor], MIN_PWM);
      pos[motor] = desired_pos[motor];
    }
    else
    {
      return;
    }
  }
}

inline void move_up()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    digitalWrite(DIR_A_PINS[motor], HIGH);
    digitalWrite(DIR_B_PINS[motor], LOW);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
}

inline void move_down()
{
  for (motor = 0; motor < NUM_MOTORS; ++motor)
  {
    //RETRACT
    digitalWrite(DIR_A_PINS[motor], LOW);
    digitalWrite(DIR_B_PINS[motor], HIGH);
    analogWrite(PWM_PINS[motor], MAX_PWM);
  }
}