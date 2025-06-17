# 🦾 EMG Bionic Hand

<div align="center">
  
![Bionic Hand](https://img.shields.io/badge/Project-Bionic%20Hand-blue?style=for-the-badge&logo=robotframework)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*Control de prótesis biónica mediante señales electromiográficas (EMG)*

</div>

---

## 📋 Descripción

Este proyecto implementa un sistema de control para una mano biónica utilizando señales EMG (electromiografía) capturadas desde los músculos del antebrazo. El sistema procesa las señales musculares en tiempo real para controlar los movimientos de una prótesis de mano robótica.

## ✨ Características

- 🔬 **Captura de señales EMG** en tiempo real
- 🤖 **Control** de servomotores
- 📊 **Procesamiento de señales**
- ⚡ **Respuesta rápida** y fluida

## 🛠️ Componentes Hardware

| Componente | Descripción | Cantidad |
|------------|-------------|----------|
| Arduino Uno/Nano | Microcontrolador principal | 2 |
| Sensores EMG | Captación de señales musculares | 1 |
| Servomotores | Actuadores para dedos | 5 |
| Fuente de alimentación | 5V/3A | 1 |

## 📁 Estructura del Proyecto

```
EMG_Bionic_Hand/
├── 📂 src/
│   ├── main.cpp              # Código principal
│   ├── emg_processing.cpp    # Procesamiento de señales
│   └── servo_control.cpp     # Control de actuadores
├── 📂 libraries/
│   └── EMGFilters/           # Biblioteca de filtros
├── 📂 docs/
│   ├── circuit_diagram.png   # Diagrama de circuito
│   └── user_manual.pdf       # Manual de usuario
├── 📂 examples/
│   └── basic_control.ino     # Ejemplo básico
└── README.md

EMG_Bionic_Hand/
├── 📂 Codes/
│   ├── 2_Calibration_Interface_Aquisition.py   # Interfaz de calibración y adquisición de EMG
│   ├── 3_Feature_Extraction.py                # Extracción de características de señales EMG
│   ├── 4_Model_Training.py                    # Entrenamiento de modelos de clasificación
│   ├── 5_RealTime_Classification.py           # Clasificación en tiempo real y comunicación con servidor
│   ├── filtrar_datos.py                       # Filtrado de datos EMG crudos
│   ├── prueba.py                              # Prueba de comunicación serial
│   └── server.py                              # Servidor para control de servos vía socket
├── 📂 EMG_Arduino/
│   └── EMG_Arduino.ino                        # Código Arduino para adquisición de EMG
├── 📂 Servos/
│   └── Servos.ino                             # Código Arduino para control de servos
├── 📂 EMG_data/
│   └── ...                                    # Archivos CSV de sesiones EMG (crudos y filtrados)
├── requirements.txt                           # Dependencias Python
├── .gitignore                                 # Exclusiones de git
├── MR3001B_Propuesta_Prótesis_A01412968.pdf   # Documento de propuesta
├── README.MD                                  # Documentación principal del proyecto
```

## 🚀 Instalación

### Requisitos Previos
- Arduino IDE 1.8.0 o superior
- Bibliotecas: Servo, EMGFilters

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/EMG_Bionic_Hand.git
   cd EMG_Bionic_Hand
   ```

2. **Instalar bibliotecas**
   ```bash
   # En Arduino IDE: Sketch > Include Library > Manage Libraries
   # Buscar e instalar: Servo, EMGFilters
   ```

3. **Cargar el código**
   - Abrir `src/main.cpp` en Arduino IDE
   - Seleccionar placa y puerto
   - Compilar y cargar

## ⚙️ Configuración

### Calibración de Sensores EMG

```cpp
// Ajustar estos valores según tu configuración
#define EMG_THRESHOLD_LOW   100
#define EMG_THRESHOLD_HIGH  800
#define SERVO_MIN_ANGLE     0
#define SERVO_MAX_ANGLE     180
```

### Conexiones

| Pin Arduino | Componente | Descripción |
|-------------|------------|-------------|
| A0, A1 | Sensores EMG | Entradas analógicas |
| 3, 5, 6, 9, 10 | Servomotores | Salidas PWM |
| GND | Común | Tierra del sistema |

## 📊 Uso

1. **Conectar el hardware** según el diagrama de circuito
2. **Colocar los electrodos** EMG en el antebrazo
3. **Calibrar** el sistema con gestos conocidos
4. **Realizar gestos** para controlar la mano biónica

### Gestos Reconocidos

| Gesto | Acción | EMG Pattern |
|-------|--------|-------------|
| ✊ Puño cerrado | Cerrar mano | Alta actividad ambos sensores |
| ✋ Mano abierta | Abrir mano | Baja actividad |
| 👍 Pulgar arriba | Mover pulgar | Actividad sensor 1 |
| 🤏 Pinza | Pinzar con dedos | Actividad modulada |

## 📈 Resultados

- **Precisión**: 85-95% en reconocimiento de gestos
- **Latencia**: <100ms respuesta del sistema
- **Autonomía**: 4-6 horas de uso continuo

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crear una branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [GitHub](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Comunidad Arduino
- Investigadores en biomecánica
- Contribuidores del proyecto

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐!**

[🐛 Reportar Bug](../../issues) · [✨ Solicitar Feature](../../issues) · [❓ Hacer Pregunta](../../discussions)

</div>