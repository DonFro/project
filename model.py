import soundfile as sf
import numpy as np
import os
import matplotlib.pyplot as plt
from pydub import AudioSegment
class Model:
    def __init__(self, file_path):
        self.length = None
        self.waveform = None
        self.file_path = file_path
        self.data = None
        self.sample_rate = None
        self.mono_data = None

    def get_waveform_data(self):
        return self.waveform

    def get_waveform_length(self):
        return self.length

    def get_file_path(self):
        return self.file_path

    def load_audio(self):
        if not os.path.splitext(self.file_path)[1].lower() == '.wav':
            # Convert the file to WAV format if it's not already
            src = self.file_path
            dst = os.path.splitext(self.file_path)[0] + '.wav'

            # Load the audio file using pydub
            sound = AudioSegment.from_file(src)

            # Convert stereo to mono if needed
            sound = sound.set_channels(1) if sound.channels > 1 else sound

            # Export the file as WAV format
            sound.export(dst, format="wav")

            # Process the converted file
            time, self.waveform, self.length = self.process_audio_file(dst)
            return time, self.waveform, self.length
        else:
            # Process the selected WAV file
            time, self.waveform, self.length = self.process_audio_file(self.file_path)
            return time, self.waveform, self.length

    def process_audio_file(self, filepath):
        if filepath:
            self.data, self.sample_rate = sf.read(filepath)

            if len(self.data.shape) > 1:
                self.mono_data = np.mean(self.data, axis=1)
            else:
                self.mono_data = self.data

            duration = len(self.mono_data) / self.sample_rate
            self.length = self.data.shape[0] / self.sample_rate

            return duration, self.mono_data, self.length

    def compute_resonance(self):
        spectrum = np.fft.fft(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)
        positive_frequencies = frequencies[:len(frequencies) // 2]
        positive_spectrum = spectrum[:len(spectrum) // 2]

        max_index = np.argmax(np.abs(positive_spectrum))
        highest_res_freq = positive_frequencies[max_index]

        return highest_res_freq

    def calculate_rt60(self, spectrum_slice, frequencies_slice):
        # Find the maximum amplitude and its corresponding frequency
        max_amplitude = np.max(np.abs(spectrum_slice))
        max_freq_index = np.argmax(np.abs(spectrum_slice))
        max_freq = frequencies_slice[max_freq_index]

        # Set a threshold for decay (60 dB lower than the maximum amplitude)
        threshold = max_amplitude / 1000  # For a 60 dB decrease, divide by 1000 (approx. 60 dB)

        # Find the index where the amplitude first falls below the threshold
        decay_indices = np.where(np.abs(spectrum_slice) < threshold)[0]
        if len(decay_indices) > 0:
            decay_point = decay_indices[0]
        else:
            decay_point = len(spectrum_slice) - 1

        # Calculate the time duration corresponding to the decay_point
        time = 1 / self.sample_rate
        rt60 = time * decay_point  # RT60 is the time taken to reach the decay point

        return max_freq, rt60

    def compute_rt60_for_frequencies(self, low_freq_range=(0, 100), medium_freq_range=(100, 1000),
                                     high_freq_range=(1000, None)):
        # Normalize the spectrum
        spectrum = np.fft.fft(self.mono_data) / len(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)

        # Find indices corresponding to each frequency range
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        medium_freq_indices = np.where((frequencies >= medium_freq_range[0]) & (frequencies < medium_freq_range[1]))[0]

        # Handle the case where high_freq_range[1] is None
        if high_freq_range[1] is None:
            high_freq_indices = np.where((frequencies >= high_freq_range[0]))[0]
        else:
            high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        # Calculate RT60 values for each frequency range
        rt60_low = self.calculate_rt60(spectrum[low_freq_indices], frequencies[low_freq_indices])
        rt60_medium = self.calculate_rt60(spectrum[medium_freq_indices], frequencies[medium_freq_indices])
        rt60_high = self.calculate_rt60(spectrum[high_freq_indices], frequencies[high_freq_indices])

        return rt60_low, rt60_medium, rt60_high

    def plot_combined_rt60(self, fs, signal, rt60_db):
        # Calculate RT60 for low, mid, and high frequency ranges
        low_rt60, mid_rt60, high_rt60 = self.compute_rt60_for_frequencies()

        # Assume rt60_db contains RT60 values in dB for each frequency range
        time_axis_low = np.arange(len(rt60_db[0])) * (1 / fs)
        time_axis_mid = np.arange(len(rt60_db[1])) * (1 / fs)
        time_axis_high = np.arange(len(rt60_db[2])) * (1 / fs)

        # Plotting the combined RT60 for low, mid, and high frequency ranges
        plt.figure(figsize=(8, 6))

        plt.plot(time_axis_low, rt60_db[0], label='Low Frequency Range')
        plt.plot(time_axis_mid, rt60_db[1], label='Medium Frequency Range')
        plt.plot(time_axis_high, rt60_db[2], label='High Frequency Range')

        plt.xlabel('Time (s)')
        plt.ylabel('RT60 (dB)')
        plt.title('Combined RT60 for Different Frequency Ranges')
        plt.legend()
        plt.grid()

        plt.show()

    def plot_rt60(self, fs, signal, rt60_db):
        def plot_rt60(self, fs, signal, rt60_db):
            # Assume rt60_db contains RT60 values in dB
            time_axis = np.arange(len(rt60_db)) * (1 / fs)

            # Find the decay point for each RT60 value
            decay_points = []
            for i in range(len(rt60_db)):
                # Convert RT60 in dB to linear scale
                rt60_linear = 10 ** (rt60_db[i] / 20)

                # Find the threshold for decay (e.g., 60 dB lower than the maximum amplitude)
                threshold = np.max(rt60_linear) / 1000  # For a 60 dB decrease

                # Find the index where the amplitude first falls below the threshold
                decay_indices = np.where(rt60_linear < threshold)[0]
                decay_point = decay_indices[0] if len(decay_indices) > 0 else len(rt60_db)
                decay_points.append(decay_point)

            # Plotting the RT60 values with the decay point
            plt.figure(figsize=(8, 6))

            plt.plot(time_axis, rt60_db, label='RT60')
            plt.scatter(time_axis[decay_points], rt60_db[decay_points], color='red', label='Decay Point', marker='o')

            plt.xlabel('Time (s)')
            plt.ylabel('RT60 (dB)')
            plt.title('RT60 with Decay Point')
            plt.legend()
            plt.grid()

            plt.show()
