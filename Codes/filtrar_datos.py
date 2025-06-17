import pandas as pd
import os
import glob

# Ruta base del proyecto
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "EMG_data")
output_dir = os.path.join(data_dir, "filtered")

# Crear carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Buscar todos los archivos CSV en EMG_data que siguen el patrón de nombre
csv_files = glob.glob(os.path.join(
    data_dir, "Subject_*_Session_*_EMGdata_*.csv"))

# Procesar cada archivo
for file_path in csv_files:
    try:
        # Leer CSV
        df = pd.read_csv(file_path)

        # Filtrar por ID
        df_filtrado = df[df["Sample"] >= 300]

        # Nombre base del archivo (sin ruta)
        filename = os.path.basename(file_path)

        # Guardar archivo en la carpeta "filtered"
        output_path = os.path.join(output_dir, filename)
        df_filtrado.to_csv(output_path, index=False)

        print(f"Archivo procesado: {filename}")
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
