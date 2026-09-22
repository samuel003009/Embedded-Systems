#include <SoftwareSerial.h>

SoftwareSerial BT(2, 3);    // 定義藍牙模組的 RX 為 Pin 2, TX 為 Pin 3

void setup() {
  Serial.begin(9600);
  BT.begin(9600); 
}

void loop() {
  // 讀取電腦端的輸入，傳送給手機
  if (Serial.available()) {
    char val = Serial.read();
    BT.print(val);    // 將字元送往藍牙
  }

  // 讀取手機端傳來的訊息，顯示在電腦螢幕上
  if (BT.available()) {
    char val = BT.read();
    Serial.print(val);    // 將字元送往電腦
  }
}