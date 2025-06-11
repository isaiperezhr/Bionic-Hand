import serial
import pandas as pd
import numpy as np
import joblib
import time

# 1) Abrir Serial y esperar arranque de Arduino
puerto_serial = 'COM8'
baud_rate = 115200
arduino = serial.Serial(puerto_serial, baud_rate, timeout=1)
time.sleep(2)  # Importante para que Arduino inicialice el Serial

# 2) Cargar modelo
model = joblib.load('random_forest_model.pkl')


def calcular_features(datos):
    return pd.DataFrame([[
        np.mean(datos),
        np.std(datos),
        np.max(datos)
    ]], columns=['Mean value', 'Std Dev', 'Maximum'])


def realizar_prediccion(features):
    clase = int(model.predict(features)[0])
    print(f"Predicción: {clase}")
    arduino.write(f"{clase}\n".encode('utf-8'))


datos_arduino = []

# 3) Bucle principal
while True:
    linea = arduino.readline().decode('utf-8').strip()
    if not linea:
        continue
    try:
        valor = int(linea)
        datos_arduino.append(valor)
    except ValueError:
        print(f"Recibido no numérico: {linea}")
        continue

    # 4) Cada N muestras, predice y reinicia buffer
    if len(datos_arduino) >= 50:
        feats = calcular_features(datos_arduino)
        realizar_prediccion(feats)
        datos_arduino = []

# (arduino.close() aquí es opcional, el script nunca sale del while)
