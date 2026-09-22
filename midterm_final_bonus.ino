#include <Wire.h> 
#define CUSTOM_SETTINGS
#define INCLUDE_GAMEPAD_MODULE
#include <Dabble.h>

const int right_IR_A0 = A0; 
const int right_IR_D0 = 11;  
const int left_IR_A0 = A1; 
const int left_IR_D0 = 12; 

// 左馬達控制設定
const byte LEFT1 = 8; 
const byte LEFT2 = 9; 
const byte LEFT_PWM = 10;

// 右馬達控制設定
const byte RIGHT1 = 7; 
const byte RIGHT2 = 6; 
const byte RIGHT_PWM = 5;

// 設定速度
byte leftSpeed = 65;
byte rightSpeed = 75;

int mode = 0;   // 初始是遙控邏輯


///
const int trig = 4;
const int echo = 13;
const int inter_time = 10;
int time = 0;



void forward() {      // 前進
  digitalWrite(LEFT1, HIGH);
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM, leftSpeed);
  digitalWrite(RIGHT1, LOW);
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM, rightSpeed);
}

void backward() {     // 後退
  digitalWrite(LEFT1, LOW);
  digitalWrite(LEFT2, HIGH);
  analogWrite(LEFT_PWM, leftSpeed);
  digitalWrite(RIGHT1, HIGH);
  digitalWrite(RIGHT2, LOW);
  analogWrite(RIGHT_PWM, rightSpeed);
}

void turnLeft() {     // 左轉
  // 左輪後退，右輪前進
  digitalWrite(LEFT1, LOW);
  digitalWrite(LEFT2, HIGH);
  analogWrite(LEFT_PWM, 100);
  
  digitalWrite(RIGHT1, LOW);
  digitalWrite(RIGHT2, HIGH);
  analogWrite(RIGHT_PWM, 100);      // 轉彎速度100
}

void turnRight() {      // 右轉
  // 右輪後退，左輪前進
  digitalWrite(LEFT1, HIGH);
  digitalWrite(LEFT2, LOW);
  analogWrite(LEFT_PWM, 100);
  
  digitalWrite(RIGHT1, HIGH);
  digitalWrite(RIGHT2, LOW);
  analogWrite(RIGHT_PWM, 100);      // 轉彎速度100
}

void stopMotor() {
  analogWrite(LEFT_PWM, 0);
  analogWrite(RIGHT_PWM, 0);
}

void setup() {
  pinMode(LEFT1, OUTPUT);
  pinMode(LEFT2, OUTPUT);
  pinMode(LEFT_PWM, OUTPUT);
  pinMode(RIGHT1, OUTPUT);
  pinMode(RIGHT2, OUTPUT);
  pinMode(RIGHT_PWM, OUTPUT);
  
  pinMode(right_IR_D0, INPUT);
  pinMode(left_IR_D0, INPUT);

  Dabble.begin(9600, 2, 3);
  Serial.begin(9600);
  
  ///
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
}

void loop() {
  Dabble.processInput();
  if (GamePad.isSquarePressed()) {
    mode = !mode;     // 在 0 和 1 之間切換
    stopMotor();
    delay(500);
  }

  if (mode == 0) {
    handleGamepad();     // 執行遙控邏輯
  } 
  else {
    handleLineFollower(); // 執行循跡邏輯
  }
}


void handleGamepad() {
  // 速度調整
  if (GamePad.isCirclePressed()) { // 按下圓圈等速
    leftSpeed = 65;
    rightSpeed = 75;
    delay(300); 
  }
  if (GamePad.isTrianglePressed()) { // 按下三角形加速
    leftSpeed = 91;
    rightSpeed = 105;
    delay(300); 
  }
  if (GamePad.isCrossPressed()) { // 按下叉叉加速
    leftSpeed = 117;
    rightSpeed = 135;
    delay(300);
  }

  // 方向控制
  if (GamePad.isUpPressed()) {
    forward();
  }
  else if (GamePad.isDownPressed()) {
    backward();
  }
  else if (GamePad.isLeftPressed()) {
    turnLeft();
  }
  else if (GamePad.isRightPressed()) {
    turnRight();
  }
  else {
    stopMotor();
  }
}

void handleLineFollower() {
    ///
  float duration, distance;
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  duration = pulseIn(echo,HIGH);
  distance = (duration/2)/29;
  time = time + inter_time;
  delay(inter_time);

  if (distance < 20){
    backward();
    delay(100);
  }
  /*
  if (distance < 20){

    turnRight();

    delay(300);

    forward();

    delay(1500);

    turnLeft();

    delay(300);

    forward();

    delay(2000);

    turnLeft();

    delay(300);

    forward();

    delay(1500);

    turnRight();

    delay(300);

  }
  */

  // 讀取數位訊號（1: 碰到黑線, 0: 白色區域）
  int right_D0 = digitalRead(right_IR_D0);
  int right_A0 = analogRead(right_IR_A0); // 類比值 (0-1023)
  int left_D0 = digitalRead(left_IR_D0);
  int left_A0 = analogRead(left_IR_A0); // 類比值 (0-1023)

  /*
  if (left_D0 == 0 && right_D0 == 1) {
    // 右邊碰到黑線 -> 向右修正
    turnRight();
  } 
  else if (left_D0 == 1 && right_D0 == 0) {
    // 左邊碰到黑線 -> 向左修正
    turnLeft();
  } 
  //else if (left_in == 1 && right_in == 1) {
    // 兩邊都碰到黑線 -> 停止
  //  stopMotor();
  //}
  else {
    // 兩邊都沒碰到黑線 -> 前進
    forward();
  } 
  */


  if (left_A0 < 250 && right_A0 >= 250) {
    // 右邊碰到黑線 -> 向右修正
    turnRight();
  } 
  else if (left_A0 >= 250 && right_A0 < 250) {
    // 左邊碰到黑線 -> 向左修正
    turnLeft();
  } 
  else {
    // 兩邊都沒碰到黑線 -> 前進
    forward();
  } 
}