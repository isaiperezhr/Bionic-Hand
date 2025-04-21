import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard

# Configuración del puerto serial
serial_port = 'COM3'  # Puerto de Arduino
baud_rate = 9600

# Configuración del gráfico
max_samples = 10000  # Número máximo de muestras en el gráfico
y_min, y_max = 0, 1000

# Configuración de la línea
x_data, y_data = [], []
line, = plt.plot([], [])

#Declarar las últimas muestras que se desplegarán
x_muestras = 60

# Función para inicializar la comunicación serial
def initialize_serial():
    ser =  serial.Serial(serial_port, baud_rate)
    ser.flushInput()
    return ser

# Inicializar la comunicación serial
ser = initialize_serial()

def EMGdata_Aq():
    try:
        # Leer una línea de datos desde el puerto serial
        line = ser.readline().decode().strip()
        value = tuple(map(float, line.split(' ')))

    except KeyboardInterrupt:
        ser.close()
        print('Serial connection closed.')
        exit()
   
    return value

# Configurar etiquetas y título
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('EMG Signal')

# Configurar límites de los ejes
fig = plt.gcf()  # Obtener la figura actual
ax = plt.gca()  # Obtener los ejes actuales
ax.set_ylim(y_min, y_max)  # Establecer límites en el eje y

espacio_presionado = False

def animate(i):
    data = EMGdata_Aq()
    amplitude = int(data[-1])

    x_data.append(i)
    y_data.append(amplitude)

    # Mantener solo las últimas x muestras
    x_data_window = x_data[-x_muestras:]
    y_data_window = y_data[-x_muestras:]

    line.set_data(x_data_window, y_data_window)

    if keyboard.is_pressed('space'):
        global espacio_presionado
        espacio_presionado = True

    # Ajustar el límite en el eje x según los datos recibidos
    ax.set_xlim(max(0, i - x_muestras), i)

    # Ajustar la escala automática en el eje y
    ax.relim()  # Recalcula los límites de los ejes
    ax.autoscale_view(scalex=False, scaley=True)

    return line,

ani = animation.FuncAnimation(fig, animate, frames=max_samples, interval=1, blit=True)

plt.show()