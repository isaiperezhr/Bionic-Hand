/**
 * @file BionicHandServoControl.ino
 * @brief Control de múltiples servos usando PCA9685 con velocidad configurable.
 *
 * Modificaciones para aumentar la velocidad de movimiento:
 *  - Se añadió kPulseStep para definir el tamaño de paso en micro-pulsos.
 *  - Se reimplementó moveServosParallel usando un bucle while que avanza kPulseStep.
 *
 * @date   2025-06-11
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// ====== CONFIGURACIÓN DEL DRIVER PCA9685 ======
constexpr uint8_t  kPCA9685_Address = 0x40;
constexpr uint32_t kOscillatorFreq  = 27000000U;
constexpr uint16_t kServoFrequency  = 50;

// ====== PARÁMETROS DE LOS SERVOS ======
constexpr uint16_t kServoMinPulse = 150;  // Pulso mínimo (0°)
constexpr uint16_t kServoMaxPulse = 600;  // Pulso máximo (180°)
constexpr uint8_t  kMaxServos     = 12;   // Canales 0..11
// Incremento en micro-pulsos para cada iteración (mayor = más rápido)
constexpr uint16_t kPulseStep     = 5;

// ====== MAPEO DINÁMICO CANAL->CLASE->ÁNGULO ======
const uint8_t angleMap[kMaxServos][3] = {
  { 50, 180,   0 },
  { 50, 180,   0 },
  { 50,   0, 180 },
  { 50,   0, 180 },
  { 50,   0, 180 },
  { 25,   1,  50 },
  { 25,   1,  50 },
  { 90, 180,   0 },
  { 90, 180,   0 },
  { 90, 180,   0 },
  { 90, 180,   0 },
  { 90, 180,   0 }
};
uint8_t servoAngles[kMaxServos] = {0};

Adafruit_PWMServoDriver pwm(kPCA9685_Address);

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setOscillatorFrequency(kOscillatorFreq);
  pwm.setPWMFreq(kServoFrequency);
  while (!Serial); 
  delay(10);
}

/**
 * @brief Mueve todos los servos en paralelo con paso kPulseStep.
 * @param targetAngles  Array de kMaxServos valores de ángulo [0..180]
 */
void moveServosParallel(const uint8_t targetAngles[]) {
  uint16_t currentPulses[kMaxServos], targetPulses[kMaxServos];
  for (uint8_t i = 0; i < kMaxServos; ++i) {
    currentPulses[i] = map(servoAngles[i], 0, 180, kServoMinPulse, kServoMaxPulse);
    targetPulses[i]  = map(targetAngles[i], 0, 180, kServoMinPulse, kServoMaxPulse);
  }
  bool moving = true;
  while (moving) {
    moving = false;
    for (uint8_t i = 0; i < kMaxServos; ++i) {
      if (currentPulses[i] < targetPulses[i]) {
        uint16_t step = currentPulses[i] + kPulseStep;
        currentPulses[i] = min(step, targetPulses[i]);
        pwm.setPWM(i, 0, currentPulses[i]);
        moving = true;
    } else if (currentPulses[i] > targetPulses[i]) {
        uint16_t step = currentPulses[i] - kPulseStep;
        currentPulses[i] = max(step, targetPulses[i]);
        pwm.setPWM(i, 0, currentPulses[i]);
        moving = true;
    }

    }
  }
  for (uint8_t i = 0; i < kMaxServos; ++i) {
    servoAngles[i] = targetAngles[i];
  }
}

/**
 * @brief Lee la clase EMG y mueve los servos según el mapeo.
 */
void servoControl() {
  if (Serial.available() >= 1) {
    int classVal = Serial.parseInt();
    Serial.readStringUntil('\n');
    uint8_t targetAngles[kMaxServos];
    for (uint8_t ch = 0; ch < kMaxServos; ++ch) {
      if (classVal >= 0 && classVal < 3) {
        targetAngles[ch] = angleMap[ch][classVal];
      } else {
        targetAngles[ch] = 90;
      }
    }
    moveServosParallel(targetAngles);
  }
}

void loop() {
  // Leer clase enviada por Python y controlar servos
  servoControl();

  delay(50);
}
