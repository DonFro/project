import os

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio(self, file_path):
        self.model.file_path = file_path
        self.view.update_filename_label(os.path.basename(file_path))
        time, waveform, length = self.model.load_audio()
        self.view.display_time_value(time)
        self.view.change_graph()
        self.view.display_highest_freq(self.model.compute_resonance())

    def get_waveform_length(self):
        return self.model.get_waveform_length()

    def get_waveform_data(self):
        return self.model.get_waveform_data()

    def get_file_path(self):
        return self.model.get_file_path()

    def combine_frequencies(self, filepath, fs, signal, rt60):
        low_rt60_db = self.compute_rt60_for_range('low')
        time_axis_low, low = self.model.plot_combined_rt60(fs, signal, low_rt60_db)

        mid_rt60_db = self.compute_rt60_for_range('mid')
        time_axis_mid, mid = self.model.plot_combined_rt60(fs, signal, mid_rt60_db)

        high_rt60_db = self.compute_rt60_for_range('high')
        time_axis_high, high = self.model.plot_combined_rt60(fs, signal, high_rt60_db)

        return time_axis_low, low, time_axis_mid, mid, time_axis_high, high

    def compute_rt60_for_frequencies(self):
        low_rt60 = self.compute_rt60_for_range('low')
        mid_rt60 = self.compute_rt60_for_range('mid')
        high_rt60 = self.compute_rt60_for_range('high')
        return low_rt60, mid_rt60, high_rt60

    def compute_rt60_for_range(self, frequency_range):
        if frequency_range == 'low':
            return self.compute_rt60_for_range_helper(0, 100)
        elif frequency_range == 'mid':
            return self.compute_rt60_for_range_helper(100, 1000)
        elif frequency_range == 'high':
            return self.compute_rt60_for_range_helper(1000, None)
        else:
            return None  # Handle other cases if needed

    def compute_rt60_for_range_helper(self, min_freq, max_freq):
        fs, signal = wavfile.read(self.model.get_file_path())

        # Filter the signal for the specified frequency range
        filtered_signal = [s for s in signal if
                           min_freq <= abs(s) < max_freq or (max_freq is None and abs(s) >= min_freq)]

        # Calculate RT60 for the filtered signal
        rt60 = self.calculate_rt60(filtered_signal)
        return rt60

    def calculate_rt60(self, signal):
        max_amplitude = max(abs(s) for s in signal)
        threshold = max_amplitude / 1000  # Set threshold for decay (60 dB lower than the maximum amplitude)
        decay_point = next((i for i, s in enumerate(signal) if abs(s) < threshold), len(signal) - 1)
        time = 1 / self.model.sample_rate
        rt60 = time * decay_point  # RT60 is the time taken to reach the decay point
        return rt60

    def plot_waveform(self):
        if self.model and self.view:
            waveform_data = self.get_waveform_data()
            time_values = self.model.get_waveform_length()

            if waveform_data and time_values:
                self.view.plot_waveform_from_data(waveform_data, time_values)
            else:
                print("Failed to retrieve waveform data or time values.")
        else:
            print("Model or View not available to plot a new graph.")