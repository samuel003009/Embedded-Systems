#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

LiquidCrystal_I2C lcd(0x27, 16, 2);   //16位元,2列
const int ledPin = 12;
const int DHTPIN = A0; 
#define DHTTYPE DHT11
const float tempThreshold = 40.0; // 溫度門檻
const float humiThreshold = 80.0; // 濕度門檻
const int inter_time = 1000;
int time = 0;


DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  lcd.init();   // 初始化
  lcd.backlight(); // 開啟背光
  lcd.setCursor(0, 0);
  pinMode(ledPin, OUTPUT);
  dht.begin();
}

void loop() 
{
  float duration, distance;
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("s, Humidity: ");
  Serial.print(h);
  Serial.print("%, Temp: ");
  Serial.print(t);
  Serial.println("C");


  lcd.setCursor(0, 0);    // 設定螢幕座標
  lcd.print("Hum: ");
  lcd.print(h, 1);
  lcd.print("%     ");
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(t, 1); 
  lcd.print((char)223); 
  lcd.print("C   ");

    
  if ( t > tempThreshold || h > humiThreshold) 
  {
    digitalWrite(ledPin, HIGH);
    delay(10); 
    digitalWrite(ledPin, LOW);
    delay(10);
  } else {
    digitalWrite(ledPin, LOW); 
  }
  time = time + inter_time;
  delay(inter_time);

}

