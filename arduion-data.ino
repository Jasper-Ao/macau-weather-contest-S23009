#include <PMS.h>
#include <SoftwareSerial.h>
#include <Arduino.h>


int phase = 0;
void nextphase(int phase_num) {
  phase = phase_num;
}


SoftwareSerial bd_serial(8, 9);
String buffer = "";
bool end = false;

String str_char = "";
bool is_num(String str){
  if (str.length() == 0) return false;

  for (byte i=0;i<str.length();i++) {
    str_char = String(str.charAt(i));
    if (str_char != ".") {
      if (!isDigit(str.charAt(i))) {
        return false;
      }
    }
  }
  return true;
}


SoftwareSerial pms_serial(2, 3);
PMS pms(pms_serial);
PMS::DATA data;


int O3_NUM = 0;
float O3_V = 0.0;
float O3_ppb = 0.0;
int sensorPin = A0;


String output = "";

void setup() {
  Serial.begin(4800);

  bd_serial.begin(9600);
  while (true) {
    if (bd_serial.available()) {
      char c = bd_serial.read();

      if (c == '\n') {
        if (buffer.startsWith("$GNGLL")) {
          end = processGNGLL(buffer);
          if (end) {
            bd_serial.end();
            break;
          }
        }
        buffer = "";
      }
      else {
        buffer += c;
      }
    }
  }

  pms_serial.begin(9600);
}


void loop() {
  if (phase == 0) {
    getPMS();
  }

  else if (phase == 1) {
    getO3();
  }
}


void getPMS() {
  if (pms.read(data)) {
    output = String(data.PM_AE_UG_2_5) + "," + String(data.PM_AE_UG_10_0);
    
    nextphase(1);
    delay(1000);
  }
}

void getO3() {
  O3_NUM = analogRead(sensorPin);
  O3_V = (O3_NUM * 5.0) / 1024;
  O3_ppb = -79.894 * O3_V * O3_V * O3_V * O3_V * O3_V
           + 1288.4 * O3_V * O3_V * O3_V * O3_V
           - 8315.9 * O3_V * O3_V * O3_V
           + 26880 * O3_V * O3_V
           - 43659 * O3_V
           + 28765;
  
  output = output + "," + String(O3_ppb);

  nextphase(0);
  delay(2000);

  Serial.println(output);
  output = "";
}

bool processGNGLL(String data) {
  char charBuffer[100];
  data.toCharArray(charBuffer, 100);

  char *token = strtok(charBuffer, ",");

  int index = 0;
  String latitude = "";
  String longitude = "";

  while (token != NULL) {
    switch (index) {
      case 1:
        latitude = token;
        break;
      case 3:
        longitude = token;
        break;
    }

    token = strtok(NULL, ",");
    index++;
  }
  Serial.print(latitude);
  Serial.print(",");
  Serial.print(longitude);
  Serial.println("");

  if (is_num(latitude) && is_num(longitude)) {
    return true;
  } else {
    return false;
  }
}
