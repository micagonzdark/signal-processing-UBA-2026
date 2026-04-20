import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    
    # 2. Descomposicion Matemática Manual - Explicacion del motor
    # Parámetro W (Window / Ventana): Tamano de la memoria de la media movil
    W = 30
    
    # A) CALCULO DE TENDENCIA (T[n]): Media Movil
    # Formula: T[n] = (1/W) * SUM_{k=0}^{W-1} Y[n-k]
    # Concepto: Promediar el entorno cercano (30 dias) actua como un filtro de suavizado
    # que apaga la variabilidad acelerada o estacional, dejando ver el rumbo principal.
    df['Tendencia'] = df['Precio'].rolling(window=W, center=True).mean()
    
    # B) CALCULO DE SEÑAL SIN TENDENCIA / RUIDO (R[n])
    # Modelo Aditivo base: Y[n] = T[n] + R[n]  ->  R[n] = Y[n] - T[n]
    # Concepto: Al restarle el curso de largo plazo a la senal, nos quedamos con toda la
    # variabilidad rapida, interferencias de noticias, panico/euforia o estacionalidad corta.
    df['Ruido'] = df['Precio'] - df['Tendencia']
    
    # Limpieza de bordes por calculo de promedios finitos
    df = df.dropna()

    # 3. Visualizacion Interactiva de Subplots con Plotly
    fig = make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(
            "Serie Original Observada (Y[n])", 
            f"Tendencia Calculada manualmente (Filtro Media Móvil, W={W})", 
            "Ruido y Alta Frecuencia Matemática (R[n])"
        )
    )
    
    # Graficos independientes de la descomposicion
    fig.add_trace(go.Scatter(x=df.index, y=df['Precio'], mode='lines', name='Precio (Y[n])', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Tendencia'], mode='lines', name='Tendencia (T[n])', line=dict(color='orange', width=3)), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Ruido'], mode='lines', name='Ruido (R[n])', line=dict(color='magenta')), row=3, col=1)
    
    fig.update_layout(
        title='Descomposición Matemática Manual de Serie Temporal (Bitcoin)',
        height=900,
        template=THEME,
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text="Precio (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Tendencia Central", row=2, col=1)
    fig.update_yaxes(title_text="Desviación (Zero-Mean)", row=3, col=1)

    fig.show()

if __name__ == "__main__":
    main()
