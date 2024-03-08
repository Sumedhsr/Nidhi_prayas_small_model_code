void setup() {
  // Start serial communication at a baud rate of 9600
  Serial.begin(9600);
}

void loop() {
  // Check if any data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();

    // Print the received byte
    Serial.print("Received: ");
    Serial.println(incomingByte);
  }
}