import numpy as np
from config import DEFAULT_SAMPLING_RATE, DEFAULT_DURATION
from signal_generator import (
    generate_sine_wave, generate_cosine_wave, 
    generate_square_wave, generate_random_signal, add_noise
)
from vector_operations import (
    inner_product_manual, inner_product_numpy, 
    compute_norm, is_orthogonal, project, normalize, gram_schmidt
)
from visualization import plot_signal, plot_comparison, plot_projection
from utils import validate_dimensions, check_zero_vector

def main():
    print("=== Signal Representation using Vector Spaces ===\n")
    
    sampling_rate = DEFAULT_SAMPLING_RATE
    duration = DEFAULT_DURATION
    
    # ---------------------------------------------------------
    # 1. Signal Generation
    # ---------------------------------------------------------
    print("[1] Generating Signals...")
    sine_wave = generate_sine_wave(amplitude=1.0, frequency=5.0, sampling_rate=sampling_rate, duration=duration)
    cosine_wave = generate_cosine_wave(amplitude=1.0, frequency=5.0, sampling_rate=sampling_rate, duration=duration)
    square_wave = generate_square_wave(amplitude=0.5, frequency=2.0, sampling_rate=sampling_rate, duration=duration)
    random_signal = generate_random_signal(amplitude=1.0, sampling_rate=sampling_rate, duration=duration)
    
    print(" -> Successfully generated Sine, Cosine, Square, and Random signals.\n")
    
    # ---------------------------------------------------------
    # 2 & 3. Vector Representation & Linear Algebra Engine
    # ---------------------------------------------------------
    print("[2] Vector Operations & Linear Algebra Engine")
    
    # Inner Product: <x, y> = sum(x_i * y_i)
    # It measures the similarity between two signals. If it is 0, they are completely dissimilar (orthogonal).
    dot_manual = inner_product_manual(sine_wave, cosine_wave)
    dot_numpy = inner_product_numpy(sine_wave, cosine_wave)
    print(f" -> Inner Product (Sine, Cosine) [Manual]: {dot_manual:.6f}")
    print(f" -> Inner Product (Sine, Cosine) [NumPy] : {dot_numpy:.6f}")
    
    # Norm (Energy): ||x|| = sqrt(<x, x>)
    # Represents the total energy or 'length' of the signal vector.
    norm_sine = compute_norm(sine_wave)
    norm_square = compute_norm(square_wave)
    print(f" -> L2 Norm (Energy) of Sine wave   : {norm_sine:.6f}")
    print(f" -> L2 Norm (Energy) of Square wave : {norm_square:.6f}\n")
    
    # ---------------------------------------------------------
    # Orthogonality Validation
    # ---------------------------------------------------------
    print("[3] Validating Orthogonality")
    
    # Orthogonal Signals: Sine and Cosine of the same frequency
    ortho_same_freq = is_orthogonal(sine_wave, cosine_wave)
    print(f" -> Are Sine and Cosine (same freq) orthogonal? {ortho_same_freq}")
    
    # Non-orthogonal Signals: A signal with itself
    ortho_self = is_orthogonal(sine_wave, sine_wave)
    print(f" -> Are Sine and itself orthogonal?             {ortho_self}")
    
    # Edge case: Zero vector
    try:
        zero_vec = np.zeros(len(sine_wave))
        is_orthogonal(sine_wave, zero_vec)
        print(" -> Zero vector edge case handled (orthogonal to everything).")
    except Exception as e:
        print(f" -> Zero vector check failed: {e}")
        
    # Edge case: Different lengths
    try:
        short_sine = generate_sine_wave(1.0, 5.0, sampling_rate, duration=0.5)
        is_orthogonal(sine_wave, short_sine)
    except ValueError as e:
        print(f" -> Different length validation successful. Error raised: {e}\n")
        
    # ---------------------------------------------------------
    # 4. Projection and Signal Separation
    # ---------------------------------------------------------
    print("[4] Projection & Signal Separation")
    
    # Create a composite signal: S = Sine + 0.5 * Square
    composite_signal = sine_wave + 0.5 * square_wave
    
    # Project composite signal onto sine wave
    # Mathematically: Proj_y(x) = (<x, y> / <y, y>) * y
    # This separates the 'sine wave' component from the composite signal.
    proj_sine = project(composite_signal, sine_wave)
    print(" -> Computed projection of composite signal onto sine wave.\n")
    
    # ---------------------------------------------------------
    # 5. Advanced: Gram-Schmidt & Noise Robustness
    # ---------------------------------------------------------
    print("[5] Advanced: Gram-Schmidt & Noise")
    
    # Orthonormalize a set of vectors
    basis = gram_schmidt([composite_signal, sine_wave, square_wave])
    print(f" -> Gram-Schmidt generated {len(basis)} orthonormal basis vectors.")
    
    # Noise robustness
    noisy_sine = add_noise(sine_wave, snr_db=10)
    print(" -> Added noise to sine wave (SNR = 10dB).\n")
    
    # ---------------------------------------------------------
    # 6. Visualization
    # ---------------------------------------------------------
    print("[6] Visualizing Results (Close plot windows to proceed)...")
    
    # Plot Individual Signal
    plot_signal(sine_wave, sampling_rate, title="Sine Wave (5 Hz)")
    
    # Plot Orthogonal Comparison
    plot_comparison(
        [sine_wave, cosine_wave], 
        ["Sine (5Hz)", "Cosine (5Hz)"], 
        sampling_rate, 
        title="Orthogonal Signals: Sine vs Cosine"
    )
    
    # Plot Non-orthogonal Comparison (Phase shifted)
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    non_ortho = np.sin(2 * np.pi * 5.0 * t + np.pi/4) # 45 degree phase shift
    plot_comparison(
        [sine_wave, non_ortho], 
        ["Sine", "Sine (45° phase shift)"], 
        sampling_rate, 
        title="Non-Orthogonal Signals"
    )
    
    # Plot Projection Result
    plot_projection(
        composite_signal, 
        sine_wave, 
        proj_sine, 
        sampling_rate, 
        title="Projection of (Sine + 0.5*Square) onto Sine"
    )
    
    print("=== Execution Complete ===")

if __name__ == "__main__":
    main()
