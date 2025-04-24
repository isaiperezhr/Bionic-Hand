// Definir el pin analógico donde se conecta la señal de MyoWare 2.0
const int myoWarePin = A0; 

// Variable para almacenar la señal leída
int signalValue = 0;

void setup() {
  // Inicializar el puerto serie para la comunicación con el monitor serie
  Serial.begin(9600);
  
  // Asegurarse de que la señal de salida de MyoWare es de 0 a 5V
  pinMode(myoWarePin, INPUT);
}

void loop() {
  // Leer el valor analógico del pin donde está conectada la señal de MyoWare
  signalValue = analogRead(myoWarePin);
  
  // Enviar el valor al monitor serie
  Serial.print("Señal EMG: ");
  Serial.println(signalValue);
  
  // Retardo para hacer las lecturas más legibles
  delay(100);
}
