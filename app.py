from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import numpy as np
import os

from config import DEFAULT_SAMPLING_RATE, DEFAULT_DURATION
from signal_generator import generate_sine_wave, generate_cosine_wave, generate_square_wave, generate_random_signal, add_noise
from vector_operations import inner_product_numpy, compute_norm, is_orthogonal, project

app = FastAPI(title="Signal Vector Spaces API")

# Ensure static folder exists
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    # Redirect root URL to the frontend UI
    return RedirectResponse(url="/static/index.html")

class SignalRequest(BaseModel):
    type1: str = "sine"
    freq1: float = 5.0
    amp1: float = 1.0
    
    type2: str = "cosine"
    freq2: float = 5.0
    amp2: float = 1.0
    
    noise_level: float = 0  # 0 means no noise
    
    duration: float = 1.0
    sampling_rate: int = 400

def get_signal(sig_type, amp, freq, sr, dur):
    if sig_type == "sine":
        return generate_sine_wave(amp, freq, sr, dur)
    elif sig_type == "cosine":
        return generate_cosine_wave(amp, freq, sr, dur)
    elif sig_type == "square":
        return generate_square_wave(amp, freq, sr, dur)
    elif sig_type == "random":
        return generate_random_signal(amp, sr, dur)
    else:
        return np.zeros(int(sr * dur))

@app.post("/api/analyze")
def analyze_signals(req: SignalRequest):
    try:
        # Generate base signals
        sig1 = get_signal(req.type1, req.amp1, req.freq1, req.sampling_rate, req.duration)
        sig2 = get_signal(req.type2, req.amp2, req.freq2, req.sampling_rate, req.duration)
        
        # Add noise if requested
        # A higher noise level on slider means lower SNR. 
        # Slider is 0-20. 0 = off. 20 = very noisy.
        if req.noise_level > 0:
            snr_actual = max(0.1, 30.0 - req.noise_level)
            sig1 = add_noise(sig1, snr_actual)
            
        t = np.linspace(0, req.duration, int(req.sampling_rate * req.duration), endpoint=False)
        
        # Calculate vector math
        dot = inner_product_numpy(sig1, sig2)
        norm1 = compute_norm(sig1)
        norm2 = compute_norm(sig2)
        
        # Relaxed tolerance for web interactive visualization
        ortho = is_orthogonal(sig1, sig2, tolerance=1e-2)
        
        if norm2 > 0:
            proj = project(sig1, sig2)
        else:
            proj = np.zeros_like(sig1)
            
        return {
            "time": t.tolist(),
            "signal1": sig1.tolist(),
            "signal2": sig2.tolist(),
            "projection": proj.tolist(),
            "metrics": {
                "dot_product": float(dot),
                "norm_sig1": float(norm1),
                "norm_sig2": float(norm2),
                "is_orthogonal": bool(ortho)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
