const int ledPin = 12;

const int trig = 5;
const int echo = 6;  
const int threshold = 5;   
const int inter_time = 1000;
int time = 0;


void setup() 
{
  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() 
{
  float duration, distance;

  digitalWrite(trig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = (duration/2)/29;
  Serial.print("Data:");
  Serial.print(time/1000);
  Serial.print(",d = ");
  Serial.print(distance);
  Serial.println(" cm");


  if (distance < threshold) 
  {
    digitalWrite(ledPin, HIGH);
    delay(10); 
    digitalWrite(ledPin, LOW);
    delay(10);
  } else 
  {
    digitalWrite(ledPin, LOW); 
  }
  time = time + inter_time;
  delay(inter_time);
}
