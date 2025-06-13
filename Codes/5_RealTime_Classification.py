import serial
import pandas as pd
import numpy as np
import joblib
import time
import socket

# 1) Configuración de Serial para lectura desde Arduino
puerto_serial = 'COM7'
baud_rate = 115200
arduino = serial.Serial(puerto_serial, baud_rate, timeout=1)
time.sleep(2)  # Espera a que Arduino inicialice el Serial

# 2) Configuración de socket cliente
SERVER_IP = '10.34.159.3'  # Dirección IP del servidor destino
SERVER_PORT = 5000           # Puerto en el que corre el servidor Python
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((SERVER_IP, SERVER_PORT))
print(f"Conectado al servidor {SERVER_IP}:{SERVER_PORT}")

# 3) Cargar modelo
model = joblib.load('random_forest_model.pkl')


def calcular_features(datos):
    """Calcula mean, std y max de la lista de valores."""
    return pd.DataFrame([[
        np.mean(datos),
        np.std(datos),
        np.max(datos)
    ]], columns=['Mean value', 'Std Dev', 'Maximum'])


def realizar_prediccion(features):
    """Obtiene la clase y la envía por socket al servidor."""
    clase = int(model.predict(features)[0])
    print(f"Predicción: {clase}")
    # Envío de la predicción al servidor
    client_sock.sendall(f"{clase}\n".encode('utf-8'))
    # Recepción de la respuesta del servidor (opcional)
    respuesta = client_sock.recv(1024).decode('utf-8').strip()
    print(f"Respuesta del servidor: {respuesta}")


datos_arduino = []

# 4) Bucle principal de lectura y predicción
try:
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

        # Cada 50 muestras, predice y reinicia buffer
        if len(datos_arduino) >= 50:
            feats = calcular_features(datos_arduino)
            realizar_prediccion(feats)
            datos_arduino = []

except KeyboardInterrupt:
    print("Interrumpido por el usuario. Cerrando conexiones…")
finally:
    arduino.close()
    client_sock.close()
