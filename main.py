import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import generate_sine_wave, quantize_signal, calculate_fft, generate_pulse

THEME = "plotly_dark"  # Opciones: "plotly_dark", "plotly_white"

def plot_sinusoids_fft():
    # 1. Definir parametros de la senal (Tiempo Continuo de alta resolucion para simular analogico)
    fs_simulada = 1000.0
    duration = 1.0
    t_continuous = np.linspace(0, duration, int(fs_simulada * duration), endpoint=False)
    
    # Senal compuesta: Suma de dos frecuencias puras + Ruido
    f1 = 5.0
    amp1 = 2.0
    f2 = 12.0
    amp2 = 1.0
    
    y_clean_1 = generate_sine_wave(t_continuous, f=f1, amp=amp1)
    y_clean_2 = generate_sine_wave(t_continuous, f=f2, amp=amp2)
    ruido = np.random.normal(0, 0.4, size=t_continuous.shape)
    
    y_continuous = y_clean_1 + y_clean_2 + ruido

    # 2. Digitalizacion: Muestreo y Cuantizacion
    fs_sampling = 50.0  
    paso_muestreo = int(fs_simulada / fs_sampling)
    t_discrete = t_continuous[::paso_muestreo]
    y_discrete = y_continuous[::paso_muestreo]

    bits = 4
    y_quantized, levels = quantize_signal(y_discrete, bits, vmin=-4.5, vmax=4.5)

    # 3. Analisis Frecuencial (FFT)
    # FFT de senal pura/continua (muy alta resolucion -> aproxima al espectro ideal)
    freqs_cont, mag_cont = calculate_fft(y_continuous, fs_simulada)
    
    # FFT de señal digital
    freqs_quant, mag_quant = calculate_fft(y_quantized, fs_sampling)

    # 4. Visualizacion
    fig = make_subplots(
        rows=2, cols=1, 
        vertical_spacing=0.15,
        subplot_titles=(
            "Dominio del Tiempo: Sistema de Adquisición de Señal Compuesta + Ruido", 
            "Dominio de la Frecuencia (FFT): Separación Espectral y Piso de Ruido"
        )
    )

    # --- DOMINIO DEL TIEMPO (Arriba) ---
    fig.add_trace(go.Scatter(x=t_continuous, y=y_continuous, mode='lines', name='Senoides + Ruido', line=dict(color='cyan', width=2), opacity=0.6), row=1, col=1)
    
    # Stems para la señal digital
    t_stem = np.empty((3 * len(t_discrete),))
    t_stem[0::3], t_stem[1::3], t_stem[2::3] = t_discrete, t_discrete, np.nan
    y_stem = np.empty((3 * len(y_quantized),))
    y_stem[0::3], y_stem[1::3], y_stem[2::3] = 0, y_quantized, np.nan
    fig.add_trace(go.Scatter(x=t_stem, y=y_stem, mode='lines', name='Muestras', line=dict(color='red', width=1.5), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=t_discrete, y=y_quantized, mode='markers', name=f'Digital (Fs={fs_sampling}Hz, {bits} bits)', marker=dict(color='red', size=8, symbol='circle')), row=1, col=1)

    # --- DOMINIO DE LA FRECUENCIA (Abajo) ---
    # Graficamos espectro de base hasta un poco mas de Fs_sampling/2 para ver el límite de Nyquist
    limite_visual_freq = fs_sampling / 2.0
    mask = freqs_cont <= limite_visual_freq
    
    # Para el espectro continuo lo llenamos como un area
    fig.add_trace(go.Scatter(x=freqs_cont[mask], y=mag_cont[mask], mode='lines', name='Espectro Analógico (Ideal)', line=dict(color='cyan', width=1), fill='tozeroy'), row=2, col=1)
    
    # Stems para la FFT digital
    f_stem = np.empty((3 * len(freqs_quant),))
    f_stem[0::3], f_stem[1::3], f_stem[2::3] = freqs_quant, freqs_quant, np.nan
    mag_stem = np.empty((3 * len(mag_quant),))
    mag_stem[0::3], mag_stem[1::3], mag_stem[2::3] = 0, mag_quant, np.nan
    
    fig.add_trace(go.Scatter(x=f_stem, y=mag_stem, mode='lines', line=dict(color='red', width=2), showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=freqs_quant, y=mag_quant, mode='markers', name='Espectro Digital (Calculado)', marker=dict(color='red', size=6, symbol='diamond')), row=2, col=1)

    # Linea de limite de Nyquist
    fig.add_vline(x=fs_sampling/2, line_dash="dash", line_color="orange", annotation_text="Nyquist Fs/2", row=2, col=1)

    fig.update_layout(title='Análisis Dual: Tiempo vs Frecuencia (El poder de separar Senoidales)', height=800, template=THEME, hovermode="x unified")
    fig.update_xaxes(title_text="Tiempo [s]", row=1, col=1)
    fig.update_yaxes(title_text="Amplitud", row=1, col=1)
    fig.update_xaxes(title_text="Frecuencia [Hz]", row=2, col=1)
    fig.update_yaxes(title_text="Magnitud", row=2, col=1)

    fig.show()

def plot_pulse_fft():
    # 1. Parámetros del pulso
    fs = 1000.0  # Alta resolucion
    duration = 2.0
    # Simulamos sobre un intervalo mas amplio centrado en 0
    t = np.linspace(-duration/2, duration/2, int(fs * duration), endpoint=False)
    
    # Generamos un pulso cuadrado de ancho 0.2s en el centro
    width = 0.2
    y_pulse = generate_pulse(t, -width/2, width/2, amp=1.0)
    
    # 2. Análisis Frecuencial
    # Hacemos shift de la propia FFT si quisieramos verla simetrica,
    # pero nuestra calculate_fft devuelve el espectro magnitud de freq positiva.
    # Dado que un pulso en el tiempo (real, simetrico) da una Sinc en frecuencia,
    # la magnitud de la FFT sera la funcion abs(sinc(f)).
    freqs, mag = calculate_fft(y_pulse, fs)
    
    # 3. Visualización
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Pulso Rectangular (Dominio Temporal)", "Espectro del Pulso: Expansión de Banda (Sinc)")
    )
    
    fig.add_trace(go.Scatter(x=t, y=y_pulse, mode='lines', name='Pulso', line=dict(color='yellow', width=3)), row=1, col=1)
    
    # Aca el espectro de un pulso se extiende infinitamente, mostramos hasta 40 Hz
    mask = freqs <= 40
    fig.add_trace(go.Scatter(x=freqs[mask], y=mag[mask], mode='lines', name='Espectro (Magnitud)', fill='tozeroy', line=dict(color='magenta', width=2)), row=1, col=2)
    
    fig.update_layout(title='Análisis Frecuencial de Eventos (Señales Aperiódicas)', height=500, template=THEME)
    fig.update_xaxes(title_text="Tiempo [s]", range=[-1, 1], row=1, col=1)
    fig.update_yaxes(title_text="Amplitud", row=1, col=1)
    
    fig.update_xaxes(title_text="Frecuencia [Hz]", row=1, col=2)
    fig.update_yaxes(title_text="Magnitud", row=1, col=2)
    
    fig.show()

def main():
    print("Iniciando Fase 2: Módulos de Análisis...")
    print("Cargando Dashboard 1 (Senoidales y Resolución)...")
    plot_sinusoids_fft()
    
    print("Cargando Dashboard 2 (Pulsos y Sinc)...")
    plot_pulse_fft()

if __name__ == "__main__":
    main()
