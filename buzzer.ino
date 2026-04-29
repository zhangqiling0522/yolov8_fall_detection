const int buzzerPin = 8;
const int buttonPin = 7;
const int lightPin = 12;
bool alarm = false;
unsigned long previousMillis = 0;  // 记录上一次LED闪烁时间
const long blinkInterval = 500;
void setup() {
  pinMode(buzzerPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(lightPin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(buzzerPin, LOW);
  digitalWrite(lightPin, LOW);
}
void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'S' || cmd == 's') {
      alarm = true;
    }
    if (cmd == 'X' || cmd == 'x') {
      alarm = false;
    }
  }
  if (digitalRead(buttonPin) == LOW) {
    alarm = false;
  }
  digitalWrite(buzzerPin, alarm ? HIGH : LOW);
  if (alarm) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= blinkInterval) {
      previousMillis = currentMillis;  // 更新时间
      digitalWrite(lightPin, !digitalRead(lightPin));  // 翻转LED状态
    }
  } else {
    digitalWrite(lightPin, LOW);
  }
}