import numpy as np

def entangled_bias(val: str, digits=['3', '6', '8'], strength=0.25):
    count = sum([d in val for d in digits])
    return 1 + strength * count

def reshape_amplitude(amplitudes, method="exp"):
    if method == "sqrt":
        return np.sqrt(amplitudes)
    elif method == "log":
        return np.log1p(amplitudes)
    elif method == "exp":
        return np.exp(amplitudes * 2)
    elif method == "power":
        return np.power(amplitudes, 1.5)
    return amplitudes

def advanced_reshape_amplitude(amplitudes, method="exp", phase_mod=True, freq=10):
    reshaped = reshape_amplitude(amplitudes, method=method)
    if phase_mod:
        indices = np.arange(len(amplitudes))
        phase_shift = np.sin(2 * np.pi * freq * indices / len(amplitudes))
        complex_wave = reshaped * np.exp(1j * phase_shift)
    else:
        complex_wave = reshaped.astype(np.complex128)
    return complex_wave
