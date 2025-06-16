Collecting workspace information# EMG Bionic Hand

Este proyecto implementa un sistema completo de adquisición, procesamiento y clasificación de señales EMG para controlar una mano protésica biónica mediante dos Arduinos: uno para la adquisición de señales EMG y otro para el control de servomotores.

---

## Estructura del Proyecto

```
EMG_Bionic_Hand/
│
├── Codes/
│   ├── 2_Calibration_Interface_Aquisition.py
│   ├── 3_Feature_Extraction.py
│   ├── 4_Model_Training.py
│   ├── 5_RealTime_Classification.py
│   ├── server.py
│   └── ...
├── EMG_Arduino/
│   └── EMG_Arduino.ino
├── Servos/
│   └── Servos.ino
├── EMG_data/
│   └── ...
├── requirements.txt
├── emg_dataset.csv
└── ...
```

---

## Requisitos

- Python 3.8+
- Arduino UNO/Nano (x2)
- Sensores EMG MyoWare
- Módulo PCA9685 (para control de servos)
- Servomotores
- Bibliotecas Python (ver abajo)

### Instalación de dependencias

Instala todas las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

---

## 1. Configuración de Hardware

- **Arduino Lector (Adquisición EMG):**  
  Sube el código `EMG_Arduino.ino` al Arduino conectado al sensor EMG.
- **Arduino Controlador (Servos):**  
  Sube el código `Servos.ino` al Arduino conectado a los servomotores y al módulo PCA9685.

---

## 2. Recolección de Datos EMG

Ejecuta la interfaz gráfica para la adquisición de datos EMG:

```sh
python Codes/2_Calibration_Interface_Aquisition.py
```

- Ingresa el ID del sujeto y el número de sesión.
- Sigue las instrucciones en pantalla para realizar las acciones (reposo, abrir, cerrar mano).
- Los datos se guardarán automáticamente en la carpeta EMG_data.

---

## 3. Extracción de Características

Procesa los archivos de datos EMG y extrae características estadísticas:

```sh
python Codes/3_Feature_Extraction.py
```

Esto generará o actualizará el archivo emg_dataset.csv con las características extraídas.

---

## 4. Entrenamiento del Modelo

Entrena y evalúa modelos de clasificación (Árbol de Decisión, SVM, Random Forest):

```sh
python Codes/4_Model_Training.py
```

- El script selecciona y guarda automáticamente el modelo con mejor precisión (por defecto, random_forest_model.pkl).

---

## 5. Clasificación y Control en Tiempo Real

### 5.1. Inicia el Servidor

Primero, ejecuta el servidor que se comunica con el Arduino controlador de servos:

```sh
python Codes/server.py
```

Asegúrate de que el puerto serial (`COM8` por defecto) corresponda al Arduino de servos.

### 5.2. Ejecuta la Clasificación en Tiempo Real

En otra terminal, ejecuta el script de predicción:

```sh
python Codes/5_RealTime_Classification.py
```

Este script:
- Lee datos EMG en tiempo real del Arduino lector.
- Extrae características y predice la clase (reposo, abrir, cerrar).
- Envía la predicción al servidor, que a su vez la transmite al Arduino de servos para mover la mano protésica.

---

## Notas Importantes

- **Orden de ejecución:**  
  1. Sube los códigos a ambos Arduinos.  
  2. Ejecuta primero `server.py`.  
  3. Luego ejecuta `5_RealTime_Classification.py`.
- **Configuración de puertos:**  
  Ajusta los nombres de los puertos seriales (`COMx`) en los scripts según tu sistema operativo y conexiones.
- **Entrenamiento adicional:**  
  Si recolectas nuevos datos, repite los pasos de extracción de características y entrenamiento para actualizar el modelo.

---

## Créditos

Desarrollado para el control de una mano biónica basada en señales EMG.  
Para dudas o mejoras, contacta al autor del repositorio.