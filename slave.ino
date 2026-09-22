#include <SoftwareSerial.h>
SoftwareSerial BT(2, 3);
char val;
void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  BT.begin(9600);
}

void loop() {
  if (Serial.available()) {
    val = Serial.read();
    Serial.print(val);
    BT.print(val);
  }
  if (BT.available()) {
    val = BT.read();
    Serial.print(val);
  }
}
