#include <LiquidCrystal.h>

#define GREEN 9
#define BLUE 10
#define RED 11

byte Bell[] = {
  B00100,
  B01110,
  B01110,
  B01110,
  B11111,
  B00000,
  B00100,
  B00000
};
LiquidCrystal lcd = LiquidCrystal(2, 3, 4, 5, 6, 7);
void setup() {
lcd.begin(16, 2);
pinMode(RED, OUTPUT);
pinMode(GREEN, OUTPUT);
pinMode(BLUE, OUTPUT);
digitalWrite(RED, LOW);
digitalWrite(GREEN, LOW);
digitalWrite(BLUE, LOW);
Serial.begin(9600);
lcd.createChar(1, Bell);
}

int redValue;
int greenValue;
int blueValue;
int a = 2;
#define delayTime 2
int analogPin = A1;

void loop() {

int piSignal = analogRead(analogPin);
float voltage = piSignal * (5.0/1024.0);
Serial.println(voltage);

if(voltage>3.00){
for(int i = 0; i < 18; i += 1) {
lcd.setCursor(1,0);
lcd.print(" Hey Bud!");
lcd.write(byte(1));
lcd.setCursor(1,1);
lcd.print(" Pay Attention pls");
lcd.scrollDisplayLeft();


for(int i = 0; i < 255; i += 1) 
{
redValue -= 1;
greenValue += 1;
analogWrite(RED, redValue);
analogWrite(GREEN, greenValue);
delay(delayTime);
}

for(int i = 0; i < 255; i += 1) // fades out green bring blue full when i=255
{
greenValue -= 1;
blueValue += 1;
analogWrite(GREEN, greenValue);
analogWrite(BLUE, blueValue);
delay(delayTime);
}

for(int i = 0; i < 255; i += 1) // fades out blue bring red full when i=255
{
blueValue -= 1;
redValue += 1;
analogWrite(BLUE, blueValue);
analogWrite(RED, redValue);
delay(delayTime);
}
}
lcd.clear();
delay(1000);
}
else{
digitalWrite(RED, LOW);
digitalWrite(GREEN, LOW);
digitalWrite(BLUE, LOW);
}

}
