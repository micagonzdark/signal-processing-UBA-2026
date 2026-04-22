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

def calculate_fft(signal, fs):
    """
    Calcula la Transformada Rápida de Fourier (FFT) de una señal real.
    Devuelve solo las frecuencias positivas y la magnitud normalizada (escalada por 2/N).
    
    Args:
        signal: Array con la señal en el tiempo.
        fs: Frecuencia de muestreo (Hz).
        
    Returns:
        freqs: Array de frecuencias positivas en Hz.
        magnitude: Array de la magnitud espectral normalizada.
    """
    N = len(signal)
    
    # np.fft.fft calcula ambos lados del espectro
    fft_result = np.fft.fft(signal)
    
    # np.fft.fftfreq devuelve las frecuencias asociadas a cada coeficiente
    freqs = np.fft.fftfreq(N, d=1/fs)
    
    # Nos quedamos con la primera mitad (frecuencias positivas) -> Simetria Hermitiana
    half_N = N // 2
    freqs_pos = freqs[:half_N]
    
    # Normalizamos magnitud dividiendo por N. Multiplicamos por 2 para no perder 
    # la energia de la mitad negativa descartada (excepto el componente DC, pero 
    # para ser practicos visualmente a menudo se escala todo por 2/N).
    magnitude = np.abs(fft_result[:half_N]) * (2.0 / N)
    
    return freqs_pos, magnitude

def generate_pulse(t, t_start, t_end, amp=1.0):
    """
    Genera un pulso rectangular matemático.
    
    Args:
        t: Array de tiempos.
        t_start: Tiempo donde inicia el pulso.
        t_end: Tiempo donde finaliza el pulso.
        amp: Amplitud del pulso.
        
    Returns:
        Array de la misma longitud que t con el pulso.
    """
    return np.where((t >= t_start) & (t <= t_end), amp, 0.0)
