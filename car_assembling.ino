#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#define CUSTOM_SETTINGS
#define INCLUDE_GAMEPAD_MODULE
#include <Dabble.h>



// 左馬達控制設定
const byte LEFT1 = 8;    // IN1
const byte LEFT2 = 9;    // IN2
const byte LEFT_PWM = 10;

// 右馬達控制設定
const byte RIGHT1 = 7;   // IN3
const byte RIGHT2 = 6;   // IN4
const byte RIGHT_PWM = 5;

// 設定 PWM 輸出值（代表的是車子的速度）
byte leftSpeed = 130;
byte rightSpeed = 150;

void forward() { // 前進
  // 左輪
  digitalWrite(LEFT1, HIGH);
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM, leftSpeed);

  // 右輪。因在小車上馬達安裝方向左右兩個是相對的
  digitalWrite(RIGHT1, LOW);
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM, rightSpeed);
}

void backward() { // 後退
  // 左輪
  digitalWrite(LEFT1, LOW);
  digitalWrite(LEFT2, HIGH);
  analogWrite(LEFT_PWM, leftSpeed);

  // 右輪
  digitalWrite(RIGHT1, HIGH);
  digitalWrite(RIGHT2, LOW);
  analogWrite(RIGHT_PWM, rightSpeed);
}

void turnLeft() { // 左轉
  // 左輪不動，右輪動（速度為0）
  analogWrite(LEFT_PWM, 0);

  digitalWrite(RIGHT1, LOW);
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM, leftSpeed);
}

void turnRight() { // 右轉
  // 右輪不動，左輪動（速度為0）
  digitalWrite(LEFT1, HIGH);
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM, rightSpeed);

  analogWrite(RIGHT_PWM, 0);
}

void stopMotor() { // 停止，兩輪速度為0
  analogWrite(LEFT_PWM, 0);
  analogWrite(RIGHT_PWM, 0);
}


// 
// 初始化 LCD 0x27。16字, 2列
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int right_IR_A0 = A0; 
const int right_IR_D0 = 11;  
const int left_IR_A0 = A1; 
const int left_IR_D0 = 12;  


void setup() {
  // 設定每一個 PIN 的模式
  pinMode(LEFT1, OUTPUT);
  pinMode(LEFT2, OUTPUT);
  pinMode(LEFT_PWM, OUTPUT);
  pinMode(RIGHT1, OUTPUT);
  pinMode(RIGHT2, OUTPUT);
  pinMode(RIGHT_PWM, OUTPUT);
  Dabble.begin(9600, 2, 3);
  Serial.begin(9600);


  // 
  // 設定數位腳位為輸入模式
  pinMode(right_IR_D0, INPUT);
  pinMode(left_IR_D0, INPUT);

  // 初始化 LCD
  lcd.init();
  lcd.backlight(); // 開啟背光

  // 顯示啟動文字
  lcd.setCursor(0, 0);
  lcd.print("IR Sensor Test");
  delay(2000);
  lcd.clear();
}

void loop() {
  Dabble.processInput();
  if (GamePad.isTrianglePressed()) { // 按下三角形加速
    leftSpeed += 50;
    rightSpeed += 50;
    if (leftSpeed > 255) 
    {
      leftSpeed = 255;
    }
    if (rightSpeed > 255) 
    {
      rightSpeed = 255;
    }
    delay(100); 
  }
  if (GamePad.isCrossPressed()) { // 按下叉叉減速
    leftSpeed -= 50;
    rightSpeed -= 50;
    if (leftSpeed < 100) 
    {
      leftSpeed = 100;
    }
    if (rightSpeed < 100) 
    {
      rightSpeed = 100;
    }
    delay(100);
  }
  if (GamePad.isUpPressed()) {
    Serial.println("Gamepad: Up");
    forward();
  }
  else if (GamePad.isDownPressed()) {
    Serial.println("Gamepad: Down");
    backward();
  }
  else if (GamePad.isLeftPressed()) {
    Serial.println("Gamepad: Left");
    turnLeft();
  }
  else if (GamePad.isRightPressed()) {
    Serial.println("Gamepad: Right");
    turnRight();
  }
  else {
    stopMotor();
  }
  
  

  
  // 
  // 讀取感測器數值
  int right_valA0 = analogRead(right_IR_A0); // 類比值 (0-1023)
  int right_valD0 = digitalRead(right_IR_D0); // 數位值 (0 或 1)
  int left_valA0 = analogRead(left_IR_A0); // 類比值 (0-1023)
  int left_valD0 = digitalRead(left_IR_D0); // 數位值 (0 或 1)

  // 將數值印到序列埠監控視窗
  Serial.print("R_Analog: "); Serial.print(right_valA0);
  Serial.print(" | Digital: "); Serial.println(right_valD0);
  Serial.print("L_Analog: "); Serial.print(left_valA0);
  Serial.print(" | Digital: "); Serial.println(left_valD0);

  lcd.setCursor(0, 0);
  lcd.print("R:");
  lcd.print(right_valA0);
  lcd.print("/");
  lcd.print(right_valD0);
  lcd.print("    "); 

  lcd.setCursor(0, 1);
  lcd.print("L:");
  lcd.print(left_valA0);
  lcd.print("/");
  lcd.print(left_valD0);
  lcd.print("    "); 

  delay(50); 

  if(right_valD0 == 1)
  {
    turnLeft();
    delay(150);
    stopMotor();
  }
  if(left_valD0 == 1)
  {
    turnRight();
    delay(150);
    stopMotor();
  }
}