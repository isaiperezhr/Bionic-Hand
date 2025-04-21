import csv
import os
import numpy as np
import pandas as pd

# Definir la frecuencia de muestreo y el intervalo de tiempo
sampling_rate = 100  # Hz
time_window = 0.5  # segundos
samples_per_window = int(sampling_rate * time_window)

# Función para calcular características dentro de ventanas
def calculate_features(arr):
    arr = np.array(arr)
    windowed_means = []
    windowed_stds = []
    windowed_maxs = []

    for i in range(0, len(arr), samples_per_window):
        window = arr[i:i+samples_per_window]
        if len(window) > 0:
            windowed_means.append(np.mean(window))
            windowed_stds.append(np.std(window))
            windowed_maxs.append(np.max(window))

    return np.mean(windowed_means), np.mean(windowed_stds), np.mean(windowed_maxs)

# Definir el nombre del archivo CSV de salida
output_file = 'emg_dataset.csv'

# Revisar si el archivo ya existe
file_exists = os.path.isfile(output_file)

# Abrir el archivo en modo 'append' si existe, o 'write' si no existe
with open(output_file, mode='a' if file_exists else 'w', newline='') as file:
    writer = csv.writer(file)

    # Si el archivo no existe, escribir el encabezado
    if not file_exists:
        writer.writerow(['Mean value', 'Std Dev', 'Maximum', 'Output'])

    # Iterar sobre todos los archivos CSV en la carpeta EMG_data
    folder_path = 'EMG_data'
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            print(f"Procesando archivo: {file_path}")

            # Leer el CSV
            df = pd.read_csv(file_path)

            # Inicializar arrays para almacenar los valores
            rest = []
            open1 = []
            close1 = []
            open2 = []
            close2 = []
            open3 = []
            close3 = []

            # Clasificar los elementos de acuerdo con la tercera columna
            for _, row in df.iterrows():
                value = row[1]  # Elemento de la segunda columna
                label = row[2]  # Elemento de la tercera columna

                if label == 1:
                    rest.append(value)
                elif label == 2:
                    open1.append(value)
                elif label == 3:
                    close1.append(value)
                elif label == 4:
                    open2.append(value)
                elif label == 5:
                    close2.append(value)
                elif label == 6:
                    open3.append(value)
                elif label == 7:
                    close3.append(value)

            # Calcular características para cada array
            mean_rest, std_rest, max_rest = calculate_features(rest)
            mean_open1, std_open1, max_open1 = calculate_features(open1)
            mean_close1, std_close1, max_close1 = calculate_features(close1)
            mean_open2, std_open2, max_open2 = calculate_features(open2)
            mean_close2, std_close2, max_close2 = calculate_features(close2)
            mean_open3, std_open3, max_open3 = calculate_features(open3)
            mean_close3, std_close3, max_close3 = calculate_features(close3)

            # Calcular promedios generales para los arrays "open" y "close"
            mean_open = np.mean([mean_open1, mean_open2, mean_open3])
            std_open = np.mean([std_open1, std_open2, std_open3])
            max_open = np.mean([max_open1, max_open2, max_open3])

            mean_close = np.mean([mean_close1, mean_close2, mean_close3])
            std_close = np.mean([std_close1, std_close2])
            max_close = np.mean([max_close1, max_close2, max_close3])

            # Agregar las nuevas filas al archivo de salida
            # Fila 1: Características de "rest"
            writer.writerow([mean_rest, std_rest, max_rest, 0])

            # Fila 2: Características promedio de "open"
            writer.writerow([mean_open, std_open, max_open, 1])

            # Fila 3: Características promedio de "close"
            writer.writerow([mean_close, std_close, max_close, 2])

print("Archivos procesados exitosamente y datos agregados al archivo 'emg_dataset.csv'.")
