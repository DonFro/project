import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.sample_rate = None  # Initialize sample_rate attribute

        self.load_button = tk.Button(self, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=0, column=0, pady=10)

        self.change_graph_button = tk.Button(self, text="Switch Graph", command=self.change_graph)
        self.change_graph_button.grid(row=1, column=0, pady=10)

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.loaded_data = None

    def load_audio(self):
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if file_path:
            try:
                self.sample_rate, audio_data = wavfile.read(file_path)
                # For stereo audio, take only one channel (use audio_data[:, 0] for left channel)
                if len(audio_data.shape) > 1:
                    audio_data = audio_data[:, 1]  # Taking right channel if available

                self.loaded_data = audio_data
                self.plot_waveform()
            except Exception as e:
                # Handle any exceptions (e.g., unsupported file format)
                print(f"Error loading audio: {e}")

    def change_graph(self):
        if self.loaded_data is not None:
            # Display a spectrogram instead of a waveform
            self.plot_spectrogram()

    def plot_waveform(self):
        if self.loaded_data is not None:
            self.ax.clear()
            time = np.linspace(0, len(self.loaded_data) / self.sample_rate, len(self.loaded_data))
            self.ax.plot(time, self.loaded_data)
            self.ax.set_title('Waveform')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Amplitude')
            self.canvas.draw()


    def set_controller(self, controller):
        # Set the controller for communication
        self.controller = controller
