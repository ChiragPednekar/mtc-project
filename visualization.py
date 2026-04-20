import matplotlib.pyplot as plt
import numpy as np

def plot_signal(signal, sampling_rate, title="Signal", xlabel="Time (s)", ylabel="Amplitude"):
    """Plots a single signal."""
    t = np.linspace(0, len(signal)/sampling_rate, len(signal), endpoint=False)
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal, color='dodgerblue', linewidth=2)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_comparison(signals, labels, sampling_rate, title="Signal Comparison"):
    """Plots multiple signals on the same graph for comparison."""
    plt.figure(figsize=(10, 4))
    colors = ['dodgerblue', 'darkorange', 'forestgreen', 'crimson']
    
    for idx, (sig, label) in enumerate(zip(signals, labels)):
        t = np.linspace(0, len(sig)/sampling_rate, len(sig), endpoint=False)
        plt.plot(t, sig, label=label, alpha=0.8, linewidth=2, color=colors[idx % len(colors)])
        
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_projection(x, y, projection, sampling_rate, title="Signal Projection"):
    """Plots the original signal, target signal, and the projection result as subplots."""
    plt.figure(figsize=(10, 8))
    
    t = np.linspace(0, len(x)/sampling_rate, len(x), endpoint=False)
    
    plt.subplot(3, 1, 1)
    plt.plot(t, x, 'dodgerblue', label="Original Signal (x)", linewidth=2)
    plt.title("Signal x", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(t, y, 'darkorange', label="Target Signal (y)", linewidth=2)
    plt.title("Signal y (Target for Projection)", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.plot(t, projection, 'crimson', label="Projection of x onto y", linewidth=2)
    plt.title("Projection Result", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
