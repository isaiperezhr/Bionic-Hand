# 🦾 EMG Bionic Hand

<div align="center">
  
![Bionic Hand](https://img.shields.io/badge/Project-Bionic%20Hand-blue?style=for-the-badge&logo=robotframework)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*Control de prótesis biónica mediante señales electromiográficas (EMG)*

</div>

---

## 📋 Descripción

Este proyecto implementa un sistema de control para una mano biónica utilizando señales EMG (electromiografía) capturadas desde los músculos del antebrazo. El sistema procesa las señales musculares en tiempo real para controlar los movimientos de una prótesis de mano robótica, integrando adquisición, procesamiento, clasificación y control de actuadores.

## ✨ Características

- 🔬 **Captura de señales EMG** en tiempo real (Arduino + Python)
- 🤖 **Control de servomotores** mediante comunicación serial y sockets
- 📊 **Procesamiento y extracción de características** de señales EMG
- 🧠 **Entrenamiento y uso de modelos de clasificación** (Random Forest, SVM, Árbol de Decisión)
- ⚡ **Respuesta rápida** y fluida

## 🛠️ Componentes Hardware

| Componente         | Descripción                       | Cantidad |
|--------------------|-----------------------------------|----------|
| Arduino Uno/Nano   | Microcontrolador principal        | 2        |
| Sensores EMG       | Captación de señales musculares   | 1        |
| Servomotores       | Actuadores para dedos             | 5        |
| PCA9685            | Driver para control de servos     | 1        |
| Fuente de alimentación | 5V/3A                        | 1        |

## 📁 Estructura del Proyecto

```
EMG_Bionic_Hand/
├── Codes/
│   ├── 2_Calibration_Interface_Aquisition.py   # Interfaz de adquisición de EMG
│   ├── 3_Feature_Extraction.py                # Extracción de características de señales EMG
│   ├── 4_Model_Training.py                    # Entrenamiento de modelos de clasificación
│   ├── 5_RealTime_Classification.py           # Clasificación en tiempo real y comunicación con servidor
│   ├── filtrar_datos.py                       # Filtrado de datos EMG crudos
│   ├── prueba.py                              # Prueba de comunicación serial
│   └── server.py                              # Servidor para control de servos vía socket
├── EMG_Arduino/
│   └── EMG_Arduino.ino                        # Código Arduino para adquisición de EMG
├── Servos/
│   └── Servos.ino                             # Código Arduino para control de servos
├── EMG_data/
│   ├── Subject_Aramis_Session_01_EMGdata_*.csv # Archivos CSV de sesiones EMG (crudos)
│   └── filtered/                              # Carpeta de archivos CSV filtrados
├── emg_dataset.csv                            # Dataset de características EMG
├── random_forest_model.pkl                    # Modelo Random Forest entrenado
├── MR3001B_Propuesta_Prótesis_A01412968.pdf   # Documento de propuesta
├── requirements.txt                           # Dependencias Python
├── .gitignore                                 # Exclusiones de git
├── README.MD                                  # Documentación principal del proyecto
```

## 🚀 Instalación

### Requisitos Previos
- Arduino IDE 1.8.0 o superior
- Python 3.8+
- Bibliotecas Arduino: Adafruit PWM Servo Driver
- Bibliotecas Python: ver `requirements.txt`

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/EMG_Bionic_Hand.git
   cd EMG_Bionic_Hand
   ```

2. **Instalar dependencias de Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instalar bibliotecas en Arduino IDE**
   - Sketch > Include Library > Manage Libraries
   - Buscar e instalar: Adafruit PWM Servo Driver

4. **Cargar el código Arduino**
   - Abrir `EMG_Arduino/EMG_Arduino.ino` para adquisición de EMG
   - Abrir `Servos/Servos.ino` para control de servos
   - Seleccionar placa y puerto, compilar y cargar

## ⚙️ Configuración

### Adquisición de EMG

- Ejecuta `Codes/2_Calibration_Interface_Aquisition.py` para iniciar la interfaz de adquisición y etiquetado.
- Los datos se guardarán automáticamente en la carpeta `EMG_data/`.

### Extracción de Características y Entrenamiento

- Ejecuta `Codes/filtrar_datos.py` para filtrar los datos crudos.
- Ejecuta `Codes/3_Feature_Extraction.py` para generar el dataset de características.
- Ejecuta `Codes/4_Model_Training.py` para entrenar y guardar el mejor modelo.

### Clasificación en Tiempo Real

- Ejecuta `Codes/server.py` en el equipo conectado a los servos.
- Ejecuta `Codes/5_RealTime_Classification.py` en el equipo de adquisición para enviar la clase predicha al servidor.

## 📊 Uso

1. **Conectar el hardware** según el diagrama de circuito.
2. **Colocar los electrodos** EMG en el antebrazo.
3. **Realizar gestos** para controlar la mano biónica en tiempo real.

### Gestos Reconocidos

| Gesto         | Acción        | Clase |
|---------------|--------------|-------|
| ✊ Puño cerrado| Cerrar mano  |   2   |
| ✋ Mano abierta| Abrir mano   |   1   |
| 🤚 Reposo     | Reposo       |   0   |

## 📈 Resultados

- **Precisión**: 85-95% en reconocimiento de gestos
- **Latencia**: <=1000ms respuesta del sistema

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit a tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Isaí Pérez Herrera** - *Desarrollo inicial* - [GitHub](https://github.com/isaiperezhr)

## 🙏 Agradecimientos

- Comunidad Arduino
- Investigadores en biomecánica
- Contribuidores del proyecto

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐!**

[🐛 Reportar Bug](../../issues) · [✨ Solicitar Feature](../../issues) ·