import socket
import serial
import time

# Configuración del puerto serial para Arduino
PUERTO_SERIAL = 'COM8'   # Ajusta al puerto donde esté conectado el Arduino
BAUD_RATE = 115200

# Configuración del servidor socket
HOST = '0.0.0.0'     # Escucha en todas las interfaces
PORT = 5000   # Debe coincidir con el cliente


def start_server():
    # 1) Abrir conexión serial con Arduino
    arduino = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)  # Espera a que Arduino inicialice

    # 2) Crear socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f"Servidor escuchando en puerto {PORT}…")

        # 3) Aceptar conexión entrante
        conn, addr = server_sock.accept()
        with conn:
            print(f"Cliente conectado desde {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Cliente desconectado.")
                    break

                mensaje = data.decode('utf-8').strip()
                print(f"Recibido del cliente: '{mensaje}'")

                # 4) Verificar que el mensaje sea "0", "1" o "2"
                if mensaje in ('0', '1', '2'):
                    # Enviar al Arduino
                    arduino.write(f"{mensaje}\n".encode('utf-8'))
                    print(f"Enviado a Arduino: {mensaje}")

                    # Responder al cliente que fue válido
                    respuesta = f"OK, recibí mensaje válido: {mensaje}\n"
                    conn.sendall(respuesta.encode('utf-8'))
                else:
                    # Responder error al cliente
                    error_msg = f"Error: mensaje incorrecto '{mensaje}'. Solo 0, 1 o 2 permitidos.\n"
                    conn.sendall(error_msg.encode('utf-8'))

    # 5) Cerrar serial al terminar
    arduino.close()


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Cerrando servidor…")
