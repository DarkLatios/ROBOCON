 #include<Servo.h>
Servo m1,m2;
int x;

void setup() {
  m1.attach(3);
  m2.attach(10);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    x=Serial.parseInt();
    if(x<=180)
    {
      m1.write(x);
      Serial.print("Motor 1:");
      Serial.println(x);
    }
    else
    if(x>=200)
    {
      m2.write(x-200);
      Serial.print("Motor 2:");
      Serial.println(x-200);
    }
  }
}
