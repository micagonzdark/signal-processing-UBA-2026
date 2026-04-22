import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import calculate_fft

THEME = "plotly_dark"  # Opciones: "plotly_dark", "plotly_white"

def main():
    # 1. Obtencion de Datos Reales de API externa (Tema: Recoleccion del entorno)
    print("Descargando datos historicos de BTC-USD...")
    ticker = yf.Ticker("BTC-USD")
    hist = ticker.history(period="2y")
    
    # Extraemos la Serie Temporal original Y[n]
    df = pd.DataFrame()
    df['Precio'] = hist['Close']
    df = df.dropna()
    
    # 2. Descomposicion Matemática Manual
    # Parámetro W (Window / Ventana): Tamano de la memoria de la media movil
    W = 30
    
    # A) CALCULO DE TENDENCIA (T[n]): Media Movil
    df['Tendencia'] = df['Precio'].rolling(window=W, center=True).mean()
    
    # B) CALCULO DE SEÑAL SIN TENDENCIA / RUIDO (R[n])
    df['Ruido'] = df['Precio'] - df['Tendencia']
    df = df.dropna()

    # C) ANALISIS ESPECTRAL DEL RUIDO (FFT de la desviación)
    # Consideramos Fs = 1 muestra por dia
    fs_dias = 1.0  
    ruido_np = df['Ruido'].values
    freqs, mag = calculate_fft(ruido_np, fs_dias)
    
    # Omitimos el DC (frecuencia 0) para limpieza visual
    freqs_plot = freqs[1:]
    mag_plot = mag[1:]

    # 3. Visualizacion Interactiva de Subplots con Plotly
    fig = make_subplots(
        rows=4, cols=1, 
        shared_xaxes=False,
        vertical_spacing=0.08,
        subplot_titles=(
            "Serie Original Observada BTC-USD (Y[n])", 
            f"Tendencia Calculada manualmente (Filtro Media Móvil, W={W} días)", 
            "Ruido y Alta Frecuencia Matemática (R[n])",
            "Análisis Espectral del Ruido (FFT): Detección de Ciclicidad"
        )
    )
    
    # Trazos temporales
    fig.add_trace(go.Scatter(x=df.index, y=df['Precio'], mode='lines', name='Precio (Y[n])', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Tendencia'], mode='lines', name='Tendencia (T[n])', line=dict(color='orange', width=3)), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Ruido'], mode='lines', name='Ruido (R[n])', line=dict(color='magenta')), row=3, col=1)
    
    # Trazo Frecuencial (FFT del Ruido)
    fig.add_trace(go.Scatter(x=freqs_plot, y=mag_plot, mode='lines', name='Espectro Ruido', line=dict(color='lime'), fill='tozeroy'), row=4, col=1)
    
    fig.update_layout(
        title='Descomposición Matemática Manual y Espectral de Serie Temporal (Bitcoin)',
        height=1100,
        template=THEME,
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text="Precio (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Tendencia Central", row=2, col=1)
    fig.update_yaxes(title_text="Desviación (Zero-Mean)", row=3, col=1)
    fig.update_xaxes(title_text="Frecuencia [Ciclos/Día]", row=4, col=1)
    fig.update_yaxes(title_text="Magnitud", row=4, col=1)

    fig.show()

if __name__ == "__main__":
    main()
