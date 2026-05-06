const int dataOutPin = 2;      // Pin to output bit sequence
const int clkPin = 3;          // Clock output pin
const int inputPin = 4;        // Input pin to read from
const int clockDelay = 1000;    // Clock period in ms

String bitSequence = "000";
int bitIndex = 0;

void setup() {
  pinMode(dataOutPin, OUTPUT);
  pinMode(clkPin, OUTPUT);
  pinMode(inputPin, INPUT);
  pinMode(5, OUTPUT);
  
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  digitalWrite(5,LOW);
  delay(100);
  digitalWrite(5, HIGH);
  delay(100);
  Serial.begin(9600);
  Serial.println("Starting sequence output and input read...");
}

void loop() {
  // Rising edge of clock
  

  // Output bit from the sequence
  int bitValue = bitSequence[bitIndex] - '0';
  digitalWrite(dataOutPin, bitValue);
  delay(50);
  Serial.println(digitalRead(11));
  digitalWrite(clkPin, HIGH);
  delay(clockDelay / 2);

  // Read and print input pin value
  int inputValue = digitalRead(inputPin);
  Serial.print("Read from pin 4: ");
  Serial.println(inputValue);

  Serial.print(digitalRead(10));
  Serial.print(digitalRead(9));
  Serial.println(digitalRead(8));
  //Serial.println(digitalRead(11));
  

  // Falling edge of clock
  digitalWrite(clkPin, LOW);
  //Serial.println(digitalRead(11));
  delay(clockDelay / 2);

  // Move to next bit in the sequence (loop around)
  bitIndex = (bitIndex + 1) % bitSequence.length();
}
