import numpy as np
import matplotlib.pyplot as plt


def generate_sine_wave(freq, duration, sampling_rate):
    time = np.arange(0, duration, 1 / sampling_rate)
    amplitude = np.sin(2 * np.pi * freq * time)
    return time, amplitude


def plot_sine_wave(freq, duration, sampling_rate):
    time, amplitude = generate_sine_wave(freq, duration, sampling_rate)

    plt.plot(time, amplitude)
    plt.title(f'Sine Wave - Frequency: {freq} Hz')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Example usage:
    frequency = 100  # Hz
    wave_duration = 1  # seconds
    sample_rate = 1000  # samples per second

    plot_sine_wave(frequency, wave_duration, sample_rate)