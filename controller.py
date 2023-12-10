import os

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio(self, file_path):
        self.model.file_path = file_path

        self.view.update_filename(os.path.basename(file_path))
        time, waveform, length = self.model.load_audio()
        self.view.display_time(time)
        self.view.plot_waveform(waveform, length)

        # For illustration purposes, computing and plotting combined RT60
        time_axis_low, amplitude_low = self.model.compute_rt60('low')
        time_axis_mid, amplitude_mid = self.model.compute_rt60('mid')
        time_axis_high, amplitude_high = self.model.compute_rt60('high')
        self.view.plot_combined_rt60(time_axis_low, amplitude_low, time_axis_mid, amplitude_mid, time_axis_high, amplitude_high)

    # Other methods...
