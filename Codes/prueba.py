import serial


def main():
    # Configura aquí tu puerto y velocidad
    # Cambia al nombre de tu puerto ("/dev/ttyUSB0" en Linux, por ejemplo)
    puerto = "COM5"
    velocidad = 115200     # Baudrate que use tu dispositivo

    try:
        ser = serial.Serial(puerto, velocidad, timeout=1)
        print(f"Abierto {puerto} a {velocidad} bps. Esperando datos...\n")

        while True:
            # Leer hasta salto de línea (o timeout) y decodificar
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if linea:
                # Imprime cada línea no vacía
                print(f"> {linea}")

    except serial.SerialException as e:
        print(f"Error al abrir {puerto}: {e}")
    except KeyboardInterrupt:
        # Ctrl+C para salir limpio
        print("\nInterrupción por teclado, cerrando puerto...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto serial cerrado.")


if __name__ == "__main__":
    main()
