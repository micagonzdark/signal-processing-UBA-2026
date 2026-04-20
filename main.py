import numpy as np
import plotly.graph_objects as go
from utils import generate_sine_wave, quantize_signal

THEME = "plotly_dark"  # Opciones: "plotly_dark", "plotly_white"

def main():
    # 1. Definir parametros de la senal analogica simulada REALISTA (Tiempo Continuo)
    duration = 1.0
    t_continuous = np.linspace(0, duration, 1000)
    
    # Senal compuesta: Suma de dos frecuencias puras + Ruido
    y_clean_1 = generate_sine_wave(t_continuous, f=5.0, amp=2.0)
    y_clean_2 = generate_sine_wave(t_continuous, f=12.0, amp=1.0)
    ruido = np.random.normal(0, 0.4, size=t_continuous.shape)
    
    y_continuous = y_clean_1 + y_clean_2 + ruido

    # 2. Digitalizacion: Muestreo (Sampling) Fs=50 Hz
    fs_sampling = 50.0  
    paso_muestreo = int(1000 / fs_sampling)
    t_discrete = t_continuous[::paso_muestreo]
    y_discrete = y_continuous[::paso_muestreo]

    # 3. Digitalizacion: Cuantizacion (Quantization)
    bits = 4
    y_quantized, levels = quantize_signal(y_discrete, bits, vmin=-4.5, vmax=4.5)

    # 4. Visualizacion Interactiva (Plotly)
    fig = go.Figure()

    # Senal continua original
    fig.add_trace(go.Scatter(
        x=t_continuous, y=y_continuous,
        mode='lines',
        name='Señal Analógica + Ruido',
        line=dict(color='cyan', width=2),
        opacity=0.6
    ))

    # Tallo para la señal digital (Dibujando las lineas verticales matemáticamente usando 'NaN')
    # Esto genera el efecto de stem de forma hiper-eficiente en plotly
    t_stem = np.empty((3 * len(t_discrete),))
    t_stem[0::3], t_stem[1::3], t_stem[2::3] = t_discrete, t_discrete, np.nan
    y_stem = np.empty((3 * len(y_quantized),))
    y_stem[0::3], y_stem[1::3], y_stem[2::3] = 0, y_quantized, np.nan

    fig.add_trace(go.Scatter(
        x=t_stem, y=y_stem,
        mode='lines',
        name='Muestras (Línea)',
        line=dict(color='red', width=1.5),
        showlegend=False
    ))

    # Puntos discretos cuantizados
    fig.add_trace(go.Scatter(
        x=t_discrete, y=y_quantized,
        mode='markers',
        name=f'Señal Digital (Fs={fs_sampling}Hz, {bits} bits)',
        marker=dict(color='red', size=8, symbol='circle')
    ))

    # Lineas de cuantizacion horizontales
    for level in levels:
        fig.add_hline(y=level, line_dash="dash", line_color="gray", opacity=0.3)

    fig.update_layout(
        title='Dominio del Tiempo: Muestreo y Cuantización Interactiva',
        xaxis_title='Tiempo [s]',
        yaxis_title='Amplitud',
        template=THEME,
        hovermode="x unified"
    )

    fig.show()

if __name__ == "__main__":
    main()
