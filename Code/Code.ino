void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);   // start serial communication

  int A_opt = 22;
  int B_opt = 23;
  int C_opt = 24;
  int D_opt = 25;
  int exp = 26;
  int next_ques = 27;

  pinMode(A_opt, INPUT);
  pinMode(B_opt, INPUT);
  pinMode(C_opt, INPUT);
  pinMode(D_opt, INPUT);
  pinMode(exp, INPUT);
  pinMode(next_ques, INPUT);
}

void loop() {
  // Read the current state of the input pins
  int A_state = digitalRead(22);
  int B_state = digitalRead(23);
  int C_state = digitalRead(24);
  int D_state = digitalRead(25);
  int exp_state = digitalRead(26);
  int next_state = digitalRead(27);

  // Check which button is pressed
  if (A_state == LOW) {
    Serial.println('A');
  }
  else if (B_state == LOW) {
    Serial.println('B');
  }
  else if (C_state == LOW) {
    Serial.println('C');
  }
  else if (D_state == LOW) {
    Serial.println('D');
  }
  else if (exp_state == LOW) {
    Serial.println('E');
  }
  else if (next_state == LOW) {
    Serial.println('N');
  }

  delay(200); // small delay to avoid multiple prints
}