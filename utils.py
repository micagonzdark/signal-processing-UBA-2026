import numpy as np

def generate_sine_wave(t, f, amp=1.0):
    """Genera una onda senoidal pura.
    
    Args:
        t: Array de tiempos.
        f: Frecuencia de la senal en Hz.
        amp: Amplitud maxima de la senal.
    """
    return amp * np.sin(2 * np.pi * f * t)

def quantize_signal(signal, bits, vmin, vmax):
    """
    Cuantiza una senal dada utilizando una resolucion de 'bits'.
    
    Args:
        signal: Array con la senal original (valores continuos de amplitud).
        bits: Cantidad de bits para la cuantizacion (ej. 3 bits = 8 niveles).
        vmin/vmax: Rango de amplitudes esperado.
    
    Returns:
        quantized: Array con la senal cuantizada.
        levels: Valores de los niveles de cuantizacion generados.
    """
    num_levels = 2 ** bits
    # Definimos los niveles posibles distribuidos uniformemente
    levels = np.linspace(vmin, vmax, num_levels)
    
    # Cuantizamos encontrando el nivel mas cercano para cada punto en la senal
    # (usamos np.digitize o calculo directo de indices)
    quantized = np.zeros_like(signal)
    for i, val in enumerate(signal):
        idx = np.argmin(np.abs(levels - val))
        quantized[i] = levels[idx]
        
    return quantized, levels
