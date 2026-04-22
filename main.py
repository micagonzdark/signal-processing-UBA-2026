import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys

from utils import generate_sine_wave, quantize_signal, calculate_fft, generate_pulse
import serie_temporal_real

THEME = "plotly_dark"

def plot_spectral_resolution():
    """
    Lab 3.1: Efecto del Enventanado (Windowing / N size) en la Resolución Espectral
    """
    fs = 500.0  # Cumple Nyquist holgadamente para 100Hz
    f1, f2 = 100.0, 102.0
    
    N_values = [128, 256, 1024, 2048]
    colors = ['rgba(255, 50, 50, 0.4)', 'rgba(255, 165, 0, 0.7)', 'rgba(50, 200, 255, 0.9)', 'rgba(255, 50, 255, 1.0)']
    
    fig = go.Figure()
    
    # Generamos la FFT para cada tamaño de ventana
    for idx, N in enumerate(N_values):
        duration = N / fs
        t = np.linspace(0, duration, N, endpoint=False)
        
        # Señal compuesta: 100Hz y 102Hz
        y = generate_sine_wave(t, f1, amp=1.0) + generate_sine_wave(t, f2, amp=0.8)
        
        freqs, mag = calculate_fft(y, fs)
        
        # Filtramos para visualizar únicamente la zona de interés
        mask = (freqs >= 90) & (freqs <= 112)
        
        fig.add_trace(go.Scatter(
            x=freqs[mask], y=mag[mask], 
            mode='lines+markers' if N<=256 else 'lines', 
            name=f'N={N} (Δf={fs/N:.2f}Hz)', 
            line=dict(color=colors[idx], width=3 if N>=1024 else 2)
        ))

    fig.update_layout(
        title='Resolución Espectral: Separabilidad de Frecuencias según el tamaño de N', 
        xaxis_title='Frecuencia [Hz]', 
        yaxis_title='Magnitud Normalizada', 
        template=THEME,
        hovermode="x unified"
    )
    fig.show()

def plot_pulse_bandwidth_comparison():
    """
    Lab 3.2: Contraste de Pulso Ancho vs Pulso Angosto y Ensanchamiento Espectral
    """
    fs = 1000.0
    duration = 2.0
    t = np.linspace(-duration/2, duration/2, int(fs * duration), endpoint=False)
    
    width_wide = 0.5
    width_narrow = 0.05
    
    y_wide = generate_pulse(t, -width_wide/2, width_wide/2, amp=1.0)
    y_narrow = generate_pulse(t, -width_narrow/2, width_narrow/2, amp=1.0)
    
    f_w, mag_w = calculate_fft(y_wide, fs)
    f_n, mag_n = calculate_fft(y_narrow, fs)
    
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Onda Cuadrada: Compresión en el Tiempo", "Espectro: Función Sinc y Ensanchamiento de Banda")
    )
    
    fig.add_trace(go.Scatter(x=t, y=y_wide, name='Pulso Ancho (0.5s)', line=dict(color='cyan', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=y_narrow, name='Pulso Estrecho (0.05s)', line=dict(color='yellow', width=2)), row=1, col=1)
    
    # Filtramos las frecuencias visuales
    mask = f_w <= 80
    fig.add_trace(go.Scatter(x=f_w[mask], y=mag_w[mask], name='FFT Pulso Ancho', line=dict(color='cyan', width=2), fill='tozeroy'), row=1, col=2)
    fig.add_trace(go.Scatter(x=f_n[mask], y=mag_n[mask], name='FFT Pulso Estrecho', line=dict(color='yellow', width=2), fill='tonexty'), row=1, col=2)
    
    fig.update_layout(
        title='Ley Dispersiva: A menor duración en el tiempo, mayor Ancho de Banda necesario', 
        template=THEME
    )
    
    fig.update_xaxes(title_text="Tiempo [s]", range=[-0.6, 0.6], row=1, col=1)
    fig.update_xaxes(title_text="Frecuencia [Hz]", row=1, col=2)
    
    fig.show()

def plot_quantization_noise_floor():
    """
    Lab 3.3: Degradación de Señal y Piso de Ruido por Cuantización (16 bit vs 4 bit)
    """
    fs = 500.0
    duration = 2.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    y_analog = generate_sine_wave(t, f=25.0, amp=4.0)
    
    # Cuantizamos a alta resolucion y baja resolucion
    y_16, _ = quantize_signal(y_analog, bits=16, vmin=-5, vmax=5)
    y_4, _  = quantize_signal(y_analog, bits=4, vmin=-5, vmax=5)
    
    # Extracción de la Señal de Ruido Termonuclear (Error = Medición Pura - Cuantizada)
    error_16 = y_analog - y_16
    error_4  = y_analog - y_4
    
    f_16, mag_err_16 = calculate_fft(error_16, fs)
    f_4,  mag_err_4  = calculate_fft(error_4, fs)
    
    # FFT de la señal útil completa para mostrar que sobresale del piso
    f_signal, mag_signal = calculate_fft(y_4, fs)
    
    mask = f_signal <= (fs / 2)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=f_signal[mask], y=mag_signal[mask], 
        name='Espectro de la Señal (4 bits)', 
        line=dict(color='white', width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=f_16[mask], y=mag_err_16[mask], 
        name='Piso Ruido Cuantización (16 bits)', 
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=f_4[mask], y=mag_err_4[mask], 
        name='Piso Ruido Cuantización (4 bits)', 
        line=dict(color='red', width=2)
    ))
    
    # Eje Y tipo Logaritmico es fundamental para graficar "Pisó de ruido"
    fig.update_layout(
        title='Análisis de Degradación Cíclica: Piso de Ruido Disperso por Cuantización', 
        xaxis_title='Frecuencia [Hz]',
        yaxis_title='Magnitud (Escala Lineal-Log visual)',
        yaxis_type="log",
        template=THEME,
        hovermode="x unified"
    )
    fig.show()

def main_menu():
    while True:
        print("\n" + "="*50)
        print(" LABORATORIO DE SEÑALES: Análisis Frecuencial")
        print("="*50)
        print("1. Resolución Espectral: Efecto N en tonos adyacentes")
        print("2. Ancho de Banda y Pulsos: Ley Sinc y dispersión")
        print("3. Cuantización: Demostración FFT del Piso de Ruido")
        print("4. Casos Reales: Volatilidad BTC (Descomposicion Tiempo/Ruido)")
        print("0. Salir")
        print("="*50)
        
        opt = input("Seleccione un número para ejecutar el Dashboard deseado: ")
        
        if opt == '1':
            print(">> Abriendo ventana PLOTLY: Resolución Espectral...")
            plot_spectral_resolution()
        elif opt == '2':
            print(">> Abriendo ventana PLOTLY: Contraste de Pulsos...")
            plot_pulse_bandwidth_comparison()
        elif opt == '3':
            print(">> Abriendo ventana PLOTLY: Ruido Cuantizado en FFT...")
            plot_quantization_noise_floor()
        elif opt == '4':
            print(">> Abriendo Dashboard Bitcoin (Laboratorio previo)...")
            serie_temporal_real.main()
        elif opt == '0':
            print("Saliendo del laboratorio...")
            sys.exit(0)
        else:
            print("Error: Selección inválida.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nSaliendo...")
