import numpy as np

def generate_sine_wave(amplitude, frequency, sampling_rate, duration):
    """Generates a sine wave signal vector."""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def generate_cosine_wave(amplitude, frequency, sampling_rate, duration):
    """Generates a cosine wave signal vector."""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    return amplitude * np.cos(2 * np.pi * frequency * t)

def generate_square_wave(amplitude, frequency, sampling_rate, duration):
    """Generates a square wave signal vector."""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    return amplitude * np.sign(np.sin(2 * np.pi * frequency * t))

def generate_random_signal(amplitude, sampling_rate, duration):
    """Generates a random noise signal vector uniformly distributed between -amplitude and +amplitude."""
    n_samples = int(sampling_rate * duration)
    return amplitude * (2 * np.random.rand(n_samples) - 1)

def add_noise(signal, snr_db):
    """
    Bonus: Adds Gaussian noise to a signal given a target Signal-to-Noise Ratio (SNR) in dB.
    """
    signal_power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    
    if snr_linear == 0:
        return signal
        
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power) * np.random.randn(len(signal))
    return signal + noise
