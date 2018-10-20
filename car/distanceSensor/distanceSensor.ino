#include <NewPing.h>
 
#define SONAR_NUM     4 // Number or sensors.
#define MAX_DISTANCE 400 // Max distance in cm.
#define PING_INTERVAL 100 // Milliseconds between pings.
#define RED_LED 12
#define GREEN_LED 11

unsigned long pingTimer[SONAR_NUM]; // When each pings.
unsigned int cm[SONAR_NUM]; // Store ping distances.
uint8_t currentSensor = 0; // Which sensor is active.
 
NewPing sonar[SONAR_NUM] = { // Sensor object array.
  NewPing(2, 3, MAX_DISTANCE),
  NewPing(5, 4, MAX_DISTANCE),
  NewPing(6, 7, MAX_DISTANCE),
  NewPing(8, 9, MAX_DISTANCE)
};
 
void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  Serial.begin(115200);
  pingTimer[0] = millis() + 75; // First ping start in ms.
  for (uint8_t i = 1; i < SONAR_NUM; i++)
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
}
 
void loop() {
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    if (millis() >= pingTimer[i]) {
      pingTimer[i] += PING_INTERVAL * SONAR_NUM;
      if (i == 0 && currentSensor == SONAR_NUM - 1)
        oneSensorCycle(); // Do something with results.
      sonar[currentSensor].timer_stop();
      currentSensor = i;
      cm[currentSensor] = 0;
      sonar[currentSensor].ping_timer(echoCheck);
    }
  }
  maybeUpdateCarState();
}
 
void echoCheck() { // If ping echo, set distance to array.
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}
 
void oneSensorCycle() { // Do something with the results.
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    Serial.print(cm[i]);
    if (i != SONAR_NUM - 1){
      Serial.print(",");
    } else {
      Serial.println();
    }
  }
}

void maybeUpdateCarState() {
  if (Serial.available() > 0) {
    int stateByte = Serial.read();
    if (stateByte == 0) {
      digitalWrite(RED_LED, HIGH);
      digitalWrite(GREEN_LED, LOW);
    } else {
      digitalWrite(RED_LED, LOW);
      digitalWrite(GREEN_LED, HIGH);
    }
  }
}