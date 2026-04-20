# Proyecto DSP Cursada 2026

Este repositorio es el proyecto práctico y acumulativo de la materia de Procesamiento de Señales Digitales (DSP).

## Nivel de Arquitectura del Proyecto (Fase 1)
- **Visualización Profesional:** Implementado íntegramente de forma interactiva con `Plotly` (Soporte dark/light global mediante la constante `THEME`).
- **Datos Sensométricos / Monetarios Reales:** Uso de `yfinance` para captar la realidad ruidosa del mundo exterior en series de tiempo, abandonando las utopías matemáticas perfectas.

## Fases y Conceptos Teóricos

### Clase 1: Fundamentos de Sistemas y Digitalización
- **Dominio del Tiempo:** Se observa el avance dinámico de señales contínuas.
- **Interferencia y Señales Complejas:** Uso de distribución de Gauss para simular ruido térmico/estático de cualquier sensor real sobre combinaciones frecuenciales.
- **Muestreo (Nyquist) y Cuantización (Analógico a Digital):** Transformación forzada de una señal a rangos bit-limitados demostrando el *Error de Cuantización*. (Ver en `main.py`).

### Clases de Series Temporales (Descomposición Numérica Manual)
- **Tendencia ($T[n]$) - Media Móvil:** Se programó matemáticamente cómo aplicar un filtro pasabajos primitivo (una ventana de promedios de tamaño W) para suavizar la estacionalidad y conseguir la macrotendencia.
- **Ruido y Aleatoriedad ($R[n]$):** Extracción aritmética restando la Tendencia sobre la Señal original ruidosa. (Ver en `serie_temporal_real.py`).

### Ejecución
```bash
python main.py
python serie_temporal_real.py
```
