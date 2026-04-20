# Signal Representation using Vector Spaces

## Overview
This project implements a system that represents communication signals as mathematical vectors and performs linear algebra operations on them. By modeling signals as vectors, we can leverage vector space concepts to analyze orthogonality, compute energy (norm), measure similarity (inner product), and separate signal components (projection).

## Project Structure
```text
signal_vector_spaces/
│── main.py                # Main workflow script demonstrating features
│── signal_generator.py    # Functions to generate various signal types
│── vector_operations.py   # Linear algebra engine (inner product, norm, projection)
│── visualization.py       # Matplotlib-based plotting module
│── config.py              # Configuration constants
│── utils.py               # Helper functions (validation, edge cases)
│── README.md              # Project documentation
```

## Theory

### 1. Vector Representation of Signals
A continuous signal $s(t)$ sampled at discrete intervals forms a vector $\mathbf{v} \in \mathbb{R}^N$. Each sample corresponds to a coordinate in an $N$-dimensional vector space.

### 2. Inner Product
The inner (dot) product of two signals measures their similarity:
$$ \langle \mathbf{x}, \mathbf{y} \rangle = \sum_{i=1}^{N} x_i y_i $$
If the inner product is high, the signals are highly correlated.

### 3. Orthogonality
Two signals are orthogonal if their inner product is zero (within a numerical tolerance):
$$ \langle \mathbf{x}, \mathbf{y} \rangle = 0 $$
Orthogonal signals do not interfere with each other, which is a fundamental concept in modulation schemes like OFDM.

### 4. Projection
The projection of signal $\mathbf{x}$ onto signal $\mathbf{y}$ extracts the component of $\mathbf{x}$ that points in the direction of $\mathbf{y}$:
$$ \text{Proj}_{\mathbf{y}}(\mathbf{x}) = \frac{\langle \mathbf{x}, \mathbf{y} \rangle}{\langle \mathbf{y}, \mathbf{y} \rangle} \mathbf{y} $$
This allows us to isolate specific signals from a composite mixture.

## Setup and Installation

1. Ensure you have Python 3.7+ installed.
2. Install the required dependencies:
```bash
pip install numpy matplotlib
```

## How to Run
Navigate to the `signal_vector_spaces` directory and run the main script to see the operations and visualizations in action:
```bash
python main.py
```

## Sample Outputs
When running `main.py`, you will see console outputs similar to:
```text
=== Signal Representation using Vector Spaces ===

[1] Generating Signals...
 -> Successfully generated Sine, Cosine, Square, and Random signals.

[2] Vector Operations & Linear Algebra Engine
 -> Inner Product (Sine, Cosine) [Manual]: -0.000000
 -> Inner Product (Sine, Cosine) [NumPy] : -0.000000
 -> L2 Norm (Energy) of Sine wave   : 22.360680
 -> L2 Norm (Energy) of Square wave : 15.811388

[3] Validating Orthogonality
 -> Are Sine and Cosine (same freq) orthogonal? True
 -> Are Sine and itself orthogonal?             False
 -> Zero vector edge case handled (orthogonal to everything).
 -> Different length validation successful. Error raised: Vectors must have the same length. Got 1000 and 500

[4] Projection & Signal Separation
 -> Computed projection of composite signal onto sine wave.

[5] Advanced: Gram-Schmidt & Noise
 -> Gram-Schmidt generated 3 orthonormal basis vectors.
 -> Added noise to sine wave (SNR = 10dB).

[6] Visualizing Results (Close plot windows to proceed)...
=== Execution Complete ===
```
Plots will sequentially pop up, allowing you to visually analyze the properties of orthogonal and non-orthogonal signals, as well as signal projection.
