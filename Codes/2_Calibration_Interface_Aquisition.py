import tkinter as tk
from tkinter import ttk
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
        self.root.title("EMG Bionic Hand Calibration")
        self.countdown = 15
        self.counter = 0
        self.subject_ID = ""
        self.session_number = ""
        self.interval_num = 1

        # Color scheme
        self.bg_color = "#f0f0f5"  # Light blueish background
        self.header_bg = "#3a7ebf"  # Blue header
        self.text_color = "#333333"  # Dark gray text
        self.accent_color = "#2e86de"  # Accent blue for buttons/highlights
        self.success_color = "#2ed573"  # Green for success messages
        self.error_color = "#ff4757"  # Red for error messages

        # Set window background
        self.root.configure(bg=self.bg_color)

        # Crear carpeta "EMG_data" si no existe
        self.global_path = "EMG_data"
        os.makedirs(self.global_path, exist_ok=True)

        # Main container
        self.main_frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.header_frame = tk.Frame(
            self.main_frame, bg=self.header_bg, padx=15, pady=15)
        self.header_frame.pack(fill=tk.X)

        self.header_label = tk.Label(
            self.header_frame,
            text="EMG Acquisition Interface",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg=self.header_bg
        )
        self.header_label.pack()

        # Input section
        self.input_frame = tk.LabelFrame(
            self.main_frame,
            text="Configuration",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        self.input_frame.pack(fill=tk.X, pady=15)

        # Subject ID row
        self.subject_frame = tk.Frame(self.input_frame, bg=self.bg_color)
        self.subject_frame.pack(fill=tk.X, pady=5)

        self.label_subject_id = tk.Label(
            self.subject_frame,
            text="Subject ID:",
            font=("Helvetica", 11),
            width=12,
            anchor="w",
            bg=self.bg_color,
            fg=self.text_color
        )
        self.label_subject_id.pack(side=tk.LEFT, padx=(0, 10))

        self.entry_subject_id = tk.Entry(
            self.subject_frame,
            font=("Helvetica", 11),
            bd=2,
            relief=tk.GROOVE
        )
        self.entry_subject_id.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.select_subject_id_button = tk.Button(
            self.subject_frame,
            text="Select",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            activebackground="#1e6bc8",
            activeforeground="white",
            bd=0,
            padx=10,
            command=self.set_subject_id
        )
        self.select_subject_id_button.pack(side=tk.LEFT, padx=(10, 0))

        # Session number row
        self.session_frame = tk.Frame(self.input_frame, bg=self.bg_color)
        self.session_frame.pack(fill=tk.X, pady=5)

        self.label_session_number = tk.Label(
            self.session_frame,
            text="Session number:",
            font=("Helvetica", 11),
            width=12,
            anchor="w",
            bg=self.bg_color,
            fg=self.text_color
        )
        self.label_session_number.pack(side=tk.LEFT, padx=(0, 10))

        self.entry_session_number = tk.Entry(
            self.session_frame,
            font=("Helvetica", 11),
            bd=2,
            relief=tk.GROOVE
        )
        self.entry_session_number.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.select_session_number_button = tk.Button(
            self.session_frame,
            text="Select",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            activebackground="#1e6bc8",
            activeforeground="white",
            bd=0,
            padx=10,
            command=self.set_session_number
        )
        self.select_session_number_button.pack(side=tk.LEFT, padx=(10, 0))

        # Status section
        self.status_frame = tk.LabelFrame(
            self.main_frame,
            text="Status",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        self.status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Timer and instruction display
        self.label_timer = tk.Label(
            self.status_frame,
            text="",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            height=2
        )
        self.label_timer.pack(fill=tk.X, pady=10)

        # Progress frame
        self.progress_frame = tk.Frame(self.status_frame, bg=self.bg_color)
        self.progress_frame.pack(fill=tk.X, pady=5)

        # Counter label
        self.label_counter = tk.Label(
            self.progress_frame,
            text="",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.label_counter.pack(side=tk.LEFT, padx=5)

        # Progress bar (will be shown during calibration)
        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

        # Status message
        self.status_message = tk.Label(
            self.status_frame,
            text="Ready to start acquisition",
            font=("Helvetica", 10, "italic"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.status_message.pack(pady=10)

        # Button to start the test
        self.start_button = tk.Button(
            self.main_frame,
            text="Start Acquisition",
            font=("Helvetica", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#1e6bc8",
            activeforeground="white",
            bd=0,
            pady=10,
            padx=20,
            cursor="hand2",
            command=self.start_calibration
        )
        self.start_button.pack(pady=15)

        # Round corners for buttons (for supported platforms)
        self._style_buttons()

    def _style_buttons(self):
        """Apply styling to buttons for better appearance"""
        buttons = [
            self.select_subject_id_button,
            self.select_session_number_button,
            self.start_button
        ]

        for button in buttons:
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#1e6bc8"))
            button.bind("<Leave>", lambda e,
                        b=button: b.config(bg=self.accent_color))

    def set_subject_id(self):
        self.subject_ID = "Subject_" + self.entry_subject_id.get()
        print(f"Subject ID set: {self.subject_ID}")
        self.status_message.config(text=f"Subject ID set: {self.subject_ID}")

    def set_session_number(self):
        self.session_number = "Session_" + self.entry_session_number.get()
        print(f"Session number set: {self.session_number}")
        self.status_message.config(
            text=f"Session number set: {self.session_number}")

    def start_calibration(self):
        # Disable input fields and buttons
        self.start_button.configure(state=tk.DISABLED, bg="#a0a0a0")
        self.select_subject_id_button.configure(
            state=tk.DISABLED, bg="#a0a0a0")
        self.select_session_number_button.configure(
            state=tk.DISABLED, bg="#a0a0a0")
        self.entry_subject_id.configure(state=tk.DISABLED)
        self.entry_session_number.configure(state=tk.DISABLED)

        # Update status
        self.label_timer.config(text="Connecting...", fg=self.accent_color)
        self.status_message.config(
            text="Attempting to connect to COM7...", fg=self.accent_color)

        # 2) Attempt to open serial port
        try:
            self.ser = serial.Serial("COM7", 115200, timeout=1)
            self.label_timer.config(text="Connected", fg=self.success_color)
            self.status_message.config(
                text="Successfully connected. Preparing to start...", fg=self.success_color)
        except serial.SerialException as e:
            # If opening serial port fails, show an error
            self.label_timer.config(
                text="Connection Failed", fg=self.error_color)
            self.status_message.config(
                text=f"Error opening serial port: {e}", fg=self.error_color)
            self._reset_interface()
            return

        # 3) Wait until data actually starts to come in
        self.status_message.config(
            text="Waiting for data stream...", fg=self.accent_color)

        # Start a thread to check for incoming data
        check_thread = threading.Thread(
            target=self._wait_for_data, daemon=True)
        check_thread.start()

    def _wait_for_data(self):
        """Wait for data from Arduino in a separate thread"""
        emg_data_started = False
        attempts = 0
        max_attempts = 20  # Timeout after 20 attempts

        while not emg_data_started and attempts < max_attempts:
            try:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    emg_data_started = True
                    print("Data received. Starting calibration sequence...")

                    # Update GUI in the main thread
                    self.root.after(0, lambda: self.status_message.config(
                        text="Data stream detected. Starting calibration...",
                        fg=self.success_color
                    ))

                    # Once we know data is flowing, start the data-collection thread
                    data_thread = threading.Thread(
                        target=self.collect_data_thread, daemon=True)
                    data_thread.start()
                    return

            except ValueError:
                pass

            attempts += 1
            time.sleep(0.5)

            # Update progress in main thread
            self.root.after(0, lambda a=attempts: self.status_message.config(
                text=f"Waiting for data stream... (attempt {a}/{max_attempts})"
            ))

        # If we get here, we timed out
        if not emg_data_started:
            self.root.after(0, lambda: self._handle_timeout())

    def _handle_timeout(self):
        """Handle timeout when no data is received"""
        self.label_timer.config(text="Timeout", fg=self.error_color)
        self.status_message.config(
            text="No data received from device. Please check connections and try again.",
            fg=self.error_color
        )
        try:
            self.ser.close()
        except:
            pass
        self._reset_interface()

    def _reset_interface(self):
        """Reset the interface to allow for retry"""
        self.start_button.configure(state=tk.NORMAL, bg=self.accent_color)
        self.select_subject_id_button.configure(
            state=tk.NORMAL, bg=self.accent_color)
        self.select_session_number_button.configure(
            state=tk.NORMAL, bg=self.accent_color)
        self.entry_subject_id.configure(state=tk.NORMAL)
        self.entry_session_number.configure(state=tk.NORMAL)

    def collect_data_thread(self):
        interval_duration = 5   # seconds per interval
        num_intervals = 7       # total number of intervals

        # Update interface to show we're starting
        self.root.after(0, lambda: self.progress.configure(
            maximum=num_intervals))

        # Prepare CSV file
        filename = f"{self.subject_ID}_{self.session_number}_EMGdata_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.global_path, filename)
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Sample", "EMG Value", "Interval"])

        # Update status
        self.root.after(0, lambda: self.status_message.config(
            text=f"Created data file: {filename}",
            fg=self.success_color
        ))

        # === (A) Countdown from 5→0 ===
        for i in range(self.countdown, 0, -1):
            # Update label_timer in the main thread
            self.root.after(0, lambda i=i: self.label_timer.config(
                text=f"Starting in {i}...",
                fg="#ff9f43"  # Orange for countdown
            ))
            time.sleep(1)

        # Final "GO!" message
        self.root.after(0, lambda: self.label_timer.config(
            text="GO!",
            fg=self.success_color
        ))
        self.root.after(0, lambda: self.status_message.config(
            text="Calibration in progress...",
            fg=self.accent_color
        ))
        time.sleep(0.5)

        # === (B) Loop through each of the 7 intervals ===
        for self.interval_num in range(1, num_intervals + 1):
            print(f"Starting interval {self.interval_num}...")

            # Update progress bar in main thread
            self.root.after(
                0, lambda n=self.interval_num: self.progress.configure(value=n-1))

            # Decide which instruction to show
            if self.interval_num in (1, 3, 5):
                instruction = "Rest"
                color = "#0abde3"  # Blue for rest
            elif self.interval_num in (2, 6):
                instruction = "Open Hand"
                color = "#2ed573"  # Green for open
            else:
                instruction = "Close Hand"
                color = "#ff6b81"  # Red for close

            # Show the instruction on the UI in main thread
            self.root.after(0, lambda i=instruction,
                            c=color: self.label_timer.config(text=i, fg=c))
            self.root.after(0, lambda i=self.interval_num, t=num_intervals: self.status_message.config(
                text=f"Collecting data for interval {i}/{t}...",
                fg=self.accent_color
            ))

            # Collect data for this interval
            self.collect_data_from_arduino(
                self.ser, interval_duration, filepath)

            # Update progress bar in main thread after interval completes
            self.root.after(
                0, lambda n=self.interval_num: self.progress.configure(value=n))

        # After all intervals:
        self.ser.close()
        print("Data collection complete.")

        # Update UI in main thread
        self.root.after(0, lambda: self.label_timer.config(
            text="Calibration Complete!",
            fg=self.success_color
        ))
        self.root.after(0, lambda: self.status_message.config(
            text=f"Successfully collected data for all {num_intervals} intervals.",
            fg=self.success_color
        ))
        self.root.after(0, lambda: self._reset_interface())

    def collect_data_from_arduino(self, ser, interval_duration, filepath):
        start_time = time.time()
        emg_data = []

        while time.time() - start_time < interval_duration:
            try:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    emg_value = int(line)
                    emg_data.append(emg_value)
                    self.counter += 1
                    with open(filepath, "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(
                            [self.counter, emg_value, self.interval_num])

                    # Update counter in main thread occasionally (not every sample to avoid GUI lag)
                    if self.counter % 10 == 0:
                        self.root.after(0, lambda c=self.counter: self.label_counter.config(
                            text=f"Samples: {c}"
                        ))
            except ValueError:
                continue

        # At the end of this interval, update the counter label
        self.root.after(0, lambda c=self.counter: self.label_counter.config(
            text=f"Samples: {c}"
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.geometry("500x650")
    root.resizable(False, False)
    root.mainloop()
