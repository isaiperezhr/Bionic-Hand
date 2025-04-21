import tkinter as tk
import threading
import os
import serial
import csv
import time
import numpy as np
from scipy import signal

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.countdown = 5
        self.counter = 0
        self.subject_ID = ""
        self.session_number = ""
        self.interval_num = 1

        # Crear carpeta "EMG_data" si no existe
        self.global_path = "EMG_data"
        os.makedirs(self.global_path, exist_ok=True)

        # Labels and buttons for Subject ID
        self.label_subject_id = tk.Label(root, text="Subject ID", font=("Arial", 12), anchor="nw", bg=root["bg"])
        self.label_subject_id.pack(pady=10, anchor="nw")
        self.entry_subject_id = tk.Entry(root)
        self.entry_subject_id.pack(pady=5, anchor="nw")
        self.select_subject_id_button = tk.Button(root, text="Select", command=self.set_subject_id)
        self.select_subject_id_button.pack(pady=5, anchor="nw")

        # Labels and buttons for Session number
        self.label_session_number = tk.Label(root, text="Session number", font=("Arial", 12), anchor="nw", bg=root["bg"])
        self.label_session_number.pack(pady=10, anchor="nw")
        self.entry_session_number = tk.Entry(root)
        self.entry_session_number.pack(pady=5, anchor="nw")
        self.select_session_number_button = tk.Button(root, text="Select", command=self.set_session_number)
        self.select_session_number_button.pack(pady=5, anchor="nw")

        # Button to start the test
        self.start_button = tk.Button(root, text="Iniciar prueba", font=("Arial", 12), command=self.start_calibration)
        self.start_button.pack(pady=20)

        # Timer and counter labels
        self.label_timer = tk.Label(root, text="", font=("Arial", 20), anchor="nw", bg=root["bg"])
        self.label_timer.pack(pady=10, anchor="nw")

        self.label_counter = tk.Label(root, text="Counter: 0", font=("Arial", 20), anchor="nw", bg=root["bg"])
        self.label_counter.pack(pady=10, anchor="nw")

    def set_subject_id(self):
        self.subject_ID = "Subject_" + self.entry_subject_id.get()
        print(f"Subject ID set: {self.subject_ID}")

    def set_session_number(self):
        self.session_number = "Session_" + self.entry_session_number.get()
        print(f"Session number set: {self.session_number}")

    def start_calibration(self):
        self.start_button.configure(state=tk.DISABLED)  # Disable the button during calibration

        # Start the serial connection
        self.ser = serial.Serial('COM3', 9600)
        self.ser.flushInput()

        # Check if data starts to be received
        emg_data_started = False
        while not emg_data_started:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    emg_data_started = True
                    print("Data received. Starting calibration...")
                    # Start the timer and data collection after receiving data
                    data_thread = threading.Thread(target=self.collect_data_thread)
                    data_thread.start()
            except ValueError:
                continue

    def collect_data_thread(self):
        # Configure the parameters for collecting data
        interval_duration = 5  # Duration of each interval in seconds
        num_intervals = 7  # Number of intervals (7 for your requirement)

        # Prepare the CSV file with the new naming format
        filename = f"{self.subject_ID}_{self.session_number}_EMGdata_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.global_path, filename)

        # Create headers for the CSV file
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Sample", "EMG Value", "Interval"])

        # Loop through intervals
        for self.interval_num in range(1, num_intervals + 1):
            print(f"Starting interval {self.interval_num}...")
            self.collect_data_from_arduino(self.ser, interval_duration, filepath)

        # Close the serial connection after all intervals
        self.ser.close()

        print("Data collection complete.")

    def collect_data_from_arduino(self, ser, interval_duration, filepath):
        start_time = time.time()
        emg_data = []
        while time.time() - start_time < interval_duration:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    emg_value = int(line)
                    emg_data.append(emg_value)
                    self.counter += 1
                    with open(filepath, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([self.counter, emg_value, self.interval_num])
            except ValueError:
                continue

        # Update the labels
        self.label_counter.config(text=f"Counter: {self.counter}")
        self.label_timer.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.geometry("400x500")
    root.mainloop()
