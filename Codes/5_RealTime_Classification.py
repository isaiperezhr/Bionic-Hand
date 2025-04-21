import serial
import pandas as pd
import numpy as np
import joblib

# Configuración de la comunicación serial
puerto_serial = 'COM3'  # Reemplaza 'COM3' con el puerto serial correcto
baud_rate = 9600  # Ajusta el baud rate según la configuración de tu Arduino

# Cargar el modelo desde el archivo pkl
model = joblib.load('decision_tree_model.pkl')

def calcular_features(datos):
    # Crear DataFrame con 'data' dentro de una lista
    df = pd.DataFrame(data=datos, columns=['data'])  
    df['Mean value'] = np.mean(df['data'])
    df['Std Dev'] = np.std(df['data'])
    df['Maximum'] = np.max(df['data'])
    return df[['Mean value', 'Std Dev', 'Maximum']]

def realizar_prediccion(features):
    # Hacer la predicción utilizando el modelo cargado
    prediccion = model.predict(features)

    # Imprimir la predicción (0, 1 o 2)
    print("Predicción:")
    print(prediccion)

# Inicializar la comunicación serial con Arduino
arduino = serial.Serial(puerto_serial, baud_rate, timeout=1)

# Inicializar la lista de datos en tiempo real
datos_arduino = []

while True:
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode('utf-8').strip()
        
        try:
            # Convertir el valor leído en un entero
            data = int(linea)
            datos_arduino.append(data)
        except ValueError:
            # Si el valor leído no es un número, se ignora
            print(f"Valor inválido recibido: {linea}")

        # Si se han recibido suficientes datos, realizar la clasificación
        if len(datos_arduino) >= 100:  # Ajusta este valor según tu necesidad de muestras
            # Calcular los features en tiempo real
            features = calcular_features(datos_arduino)

            # Realizar la predicción en tiempo real
            realizar_prediccion(features)

            # Limpiar la lista de datos para la próxima clasificación
            datos_arduino = []

# Cerrar la comunicación serial con Arduino (opcional en este código)
arduino.close()
