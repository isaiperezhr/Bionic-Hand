// --------------------------------------------------
// MyoWare streaming 
// --------------------------------------------------

void setup() {
  Serial.begin(115200);
  while (!Serial);                 // Espera al monitor serie
}

void loop() {
  // 1) Leer EMG y mandar al PC
  int sensorValue = analogRead(A3); // Cambia a Ax si tu sensor está ahí
  Serial.println(sensorValue);

  delay(50);
}
