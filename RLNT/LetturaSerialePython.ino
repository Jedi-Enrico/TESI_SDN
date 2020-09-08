#include <Wire.h>
#include <TimeLib.h>
#include <DS1307RTC.h>

const char *monthName[12] = {
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};

tmElements_t tm;

char inByte=0;
int lenbuffer=19;
byte bufferDATA[19];

String myString;
String Hour;
String Min;
String Sec;
String Day;
String Month;
String Year;

    void setup() {  
      Serial.begin(115200);  
      pinMode(LED_BUILTIN, OUTPUT);
      digitalWrite(LED_BUILTIN, LOW);
      while (!Serial) {  
        ; // wait for serial port to connect. Needed for native USB  
      }  
    }  
      
    void loop() {

      String DATA;
      if (Serial.available() > 0) //Waiting for request   
      {
        Serial.readBytes(bufferDATA,lenbuffer);
        myString = String((char *)bufferDATA);
        Hour=myString.substring(11, 13);
        Min=myString.substring(14, 16);
        Sec=myString.substring(17, 19);
        Day=myString.substring(8, 10);
        Month=myString.substring(5, 7);
        Year=myString.substring(0, 4);
  
        tm.Hour = Hour.toInt();
        tm.Minute = Min.toInt();
        tm.Second = Sec.toInt();
        tm.Day = Day.toInt();
        tm.Month = Month.toInt();
        tm.Year = CalendarYrToTm(Year.toInt());
        RTC.write(tm);
        Serial.print("1");
        delay(1000);
      }
       
    }  
