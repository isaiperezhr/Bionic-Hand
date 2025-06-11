#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// --------------------------------------------------
// Ejemplo MyoWare streaming + control LED por clase
// --------------------------------------------------

void setup() {
  Serial.begin(115200);
  while (!Serial);                 // Espera al monitor serie
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // 1) Leer EMG y mandar al PC
  int sensorValue = analogRead(A3); // Cambia a A0 si tu sensor está ahí
  Serial.println(sensorValue);

  // 2) Leer clase enviada por Python y controlar LED
  emgControl();

  delay(50);
}

void emgControl() {
  if (Serial.available() > 0) {
    int classVal = Serial.parseInt();    // Lee hasta dígitos
    Serial.readStringUntil('\n');        // Limpia el '\n'
    if (classVal == 0) {
      digitalWrite(LED_BUILTIN, HIGH);
    } else {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
