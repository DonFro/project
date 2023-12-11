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
        self.figure, self.ax_waveform = plt.subplots(figsize=(6, 6))
        self.ax_waveform = self.figure.add_subplot(111)

        # Create a FigureCanvasTkAgg instance and add it to a Canvas widget
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and place widgets using grid
        self.load_button = tk.Button(self, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=1, column=0, pady=10)

        self.change_graph_button = tk.Button(self, text="Switch Graph", command=self.change_graph)
        self.change_graph_button.grid(row=1, column=1, pady=10)

        self.combine_button = tk.Button(self, text="Combine Frequencies", command=self.combine_frequencies)
        self.combine_button.grid(row=1, column=2, pady=10)

        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=2, column=0, columnspan=3, pady=5)

        self.highest_res_freq_label = tk.Label(self, text="")
        self.highest_res_freq_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=4, column=0, columnspan=3, pady=5)

        self.rt60_label = tk.Label(self, text="")
        self.rt60_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.sample_rate = None
        self.loaded_data = None
        self.controller = None

    def load_audio(self):
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if file_path:
            self.loaded_data = file_path  # For simplicity, saving the file path
            self.sample_rate, signal = wavfile.read(file_path)
            time = np.arange(0, len(signal)) / self.sample_rate

            # Clear the existing plot
            self.ax_waveform.clear()

            # Plot waveform
            self.ax_waveform.plot(time, signal)
            self.ax_waveform.set_xlabel('Time (s)')
            self.ax_waveform.set_ylabel('Amplitude')
            self.ax_waveform.set_title('Waveform')

            # Redraw the canvas with the new graph
            self.canvas.draw()

            # Call plot_waveform to ensure the graph is displayed after loading
            self.plot_waveform()

    def plot_waveform(self):
        if self.loaded_data:
            fs, signal = wavfile.read(self.loaded_data)
            time = np.arange(0, len(signal)) / self.sample_rate

            # Check if the canvas and figure are initialized
            if self.canvas is None or self.figure is None:
                self.figure, self.ax_waveform = plt.subplots(figsize=(6, 6))
                self.ax_waveform = self.figure.add_subplot(111)
                self.canvas = FigureCanvasTkAgg(self.figure, master=self)
                self.canvas_widget = self.canvas.get_tk_widget()
                self.canvas_widget.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

            self.ax_waveform.clear()
            self.ax_waveform.plot(time, signal)
            self.ax_waveform.set_xlabel('Time (s)')
            self.ax_waveform.set_ylabel('Amplitude')
            self.ax_waveform.set_title('Waveform')

            # Redraw the canvas with the new graph
            self.canvas.draw()

    def set_controller(self, controller):
        # Set the controller for communication
        self.controller = controller

    def get_controller(self):
        # Get the set controller
        return self.controller

    def plot_combined_rt60(self):
        # Clear the current graph
        self.ax_waveform.clear()

        # Get file path and signal data
        filepath = self.controller.get_file_path()
        fs, signal = wavfile.read(filepath)

        # Calculate RT60 for low, mid, and high frequency ranges
        low_rt60, mid_rt60, high_rt60 = self.controller.compute_rt60_for_frequencies()

        # Plot combined RT60 for low, mid, and high frequency ranges
        time_axis_low, amplitude_low = self.controller.plot_combined_rt60(filepath, fs, signal, low_rt60)
        time_axis_mid, amplitude_mid = self.controller.plot_combined_rt60(filepath, fs, signal, mid_rt60)
        time_axis_high, amplitude_high = self.controller.plot_combined_rt60(filepath, fs, signal, high_rt60)

        # Plot the curves
        self.ax_waveform.plot(time_axis_low, 20 * np.log10(amplitude_low), label='Low RT60 Decay Curve')
        self.ax_waveform.plot(time_axis_mid, 20 * np.log10(amplitude_mid), label='Mid RT60 Decay Curve')
        self.ax_waveform.plot(time_axis_high, 20 * np.log10(amplitude_high), label='High RT60 Decay Curve')

        # Set labels and legend
        self.ax_waveform.set_xlabel('Time (s)')
        self.ax_waveform.set_ylabel('Amplitude (dB)')
        self.ax_waveform.set_title('Combined Reverberation Time Calculation')
        self.ax_waveform.legend()

        # Redraw the canvas with the new graph
        self.canvas.draw()

    def update_filename_label(self, filename):
        # Update Filename Label
        if hasattr(self, 'filename_label'):
            self.filename_label.config(text=f"File: {filename}")
        else:
            print("Filename label not found in the view.")

    def display_time_value(self, time):
        # Display time value on the GUI
        if hasattr(self, 'time_label'):
            self.time_label.config(text=f"Time: {time:.2f} seconds")
        else:
            print("Time label not found in the view.")

    def change_graph(self):
        # Method to change and update the displayed graph
        if hasattr(self, 'canvas') and self.controller:
            self.reset_canvas()
            self.rt60_label.config(text="")

            # Get the controller
            controller = self.get_controller()

            # Check if the controller has a method to plot a new graph
            if hasattr(controller, 'plot_waveform'):
                # Call the method in the controller to plot a new graph
                controller.plot_waveform()
            else:
                print("Controller does not have a method to plot a new graph.")
        else:
            print("Canvas or related components not found in the view, or controller not set.")

    def reset_canvas(self):
        # Reset the Matplotlib canvas
        if hasattr(self, 'figure') and hasattr(self, 'canvas'):
            self.ax_waveform.clear()  # Clear the current subplot
            self.canvas.draw()  # Redraw the canvas
        else:
            print("Canvas or related components not found in the view.")

    def plot_waveform(self):
        # Get waveform data and time values from the controller
        waveform_data = self.controller.get_waveform_data()
        time_values = self.controller.get_waveform_length()

        # Check if both data and time values are available
        if waveform_data is not None and time_values is not None:
            # Plot waveform using waveform_data and time_values
            plt.figure(figsize=(8, 6))
            plt.plot(time_values, waveform_data)
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.title('Waveform')
            plt.grid()
            plt.show()
        else:
            print("Failed to plot waveform due to missing data.")

    def combine_frequencies(self, filepath, fs, signal, rt60):
        # Method to combine frequencies
        controller = self.set_controller()  # Retrieve the controller set via set_controller() method

        if controller is not None:
            controller.combine_frequencies(filepath, fs, signal, rt60)
        else:
            print("Controller is not set or available.")

    def display_highest_freq(self, highest_res_freq):
        # Update GUI to display the highest resonance frequency
        self.highest_res_freq_label.config(text=f"Highest Resonance Frequency: {highest_res_freq:.2f} Hz")
