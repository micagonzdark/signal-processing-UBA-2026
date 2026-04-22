# Clase 02: El Dominio de la Frecuencia (Laboratorio Avanzado)

Esta clase profundiza sobre los aspectos físicos, matemáticos y computacionales del pasaje al **dominio de la frecuencia**. Mediante la Transformada Rápida de Fourier (FFT), no solo visualizamos "tonos", sino que podemos entender las limitaciones del mundo digital (resolución, enventanado, Nyquist y cuantización).

A continuación, detallamos el trasfondo de cada uno de los experimentos implementados en el `main.py` de nuestro proyecto:

---

## 1. El Motor FFT: Escalado Físico y Simetría Hermitiana

La **Fast Fourier Transform (FFT)** es un bastión fundamental del Procesamiento de Señales Digitales (DSP). Computacionalmente, implementarla requiere entender _qué_ escupe el algoritmo para traducirlo a la física de nuestro universo real.

### 📐 Simetría y Doblado de Espectro
Toda señal de tiempo **real** (sin componentes imaginarios complejos) genera un espectro de Fourier que posee **Simetría Hermitiana**. Esto significa que las _frecuencias negativas_ son un reflejo complejo conjugado de las _frecuencias positivas_.
- **En nuestro código (`utils.calculate_fft`)**: Cortamos el vector a exactamente la mitad `$N/2$`. No procesar las frecuencias negativas nos ahorra procesamiento y limpia la gráfica, porque toda la información analítica ya reside en el semieje positivo.

### 📐 Escalado de Amplitud (El factor $2/N$)
El algoritmo estándar de FFT suma las componentes a lo largo de las $N$ muestras, lo cual hace que los valores escalen proporcionalmente al tamaño del bloque N analizado, perdiendo su significado físico de "Amplitud".
- Dividimos por $N$ para promediar la magnitud.
- Multiplicamos por $2$ porque, al descartar brutalmente la mitad izquierda del espectro (frecuencias negativas), perdimos la mitad de la energía espectral generada por la FFT. Es decir: Multiplicar por 2 "levanta" el pico para que iguale a la amplitud exacta del seno original que introdujimos.

---

## 2. Resolución Espectral y Enventanado (Leakage)

Una ventana de tiempo finita en el mundo continuo equivale a tomar la señal y "multiplicarla" por una compuerta rectangular.
La resolución espectral que la FFT nos puede dar está regida matemáticamente por el tamaño del balde ("Bin") de frecuencia:
$$\Delta f = \frac{F_s}{N}$$
Donde $F_s$ es la frecuencia de muestreo y $N$ es la cantidad de muestras de la ventana.

### 🧪 Demostración en Código (`plot_spectral_resolution`)
Al ejecutar la opción de resolución en nuestro menú de consola de `main.py`, visualizamos cómo dos senoidales muy cercanas (100 Hz y 102 Hz) se fusionan en un "Lóbulo gordo" cuando intentamos mirarlas bajo un N pobre ($N=128$). A medida que subimos a $N=2048$, el tamaño del Bin $\Delta f$ se vuelve diminuto, permitiendo discernir los picos finamente afilados como agujas. A eso le llamamos **Leakage** y Separabilidad Espectral.

---

## 3. La Ley Inversa de los Pulsos: Expansión de Banda

La Transformada de Fourier impone una de las leyes más famosas de la naturaleza (directamente vinculada al principio de incertidumbre en la mecánica cuántica):
**La escala de compresión en el tiempo es inversamente proporcional a la expansión en la frecuencia.** Matemáticamente:

$$x(at) \xleftrightarrow{\text{FFT}} \frac{1}{|a|} X\left(\frac{f}{a}\right)$$

Si el pulso es muy corto ($0.05$s), necesita invocar frecuencias infinitamente altas para construir artificialmente bordes tan afilados y repentinos.

### 🧪 Demostración en Código (`plot_pulse_bandwidth_comparison`)
En nuestra función graficamos de manera simultánea una compuerta de $0.5$s y una extremadamente angosta de $0.05$s. En el espectro observamos gráficamente que el pulso estrecho arrastra una función **Sinc** ($\frac{\sin(x)}{x}$) enorme y expandida de base muy ancha, demostrando que eventos súbitos en electrónica requieren muchísimo ancho de banda para transmitirse.

---

## 4. Piso de Ruido por Cuantización (Quantization Noise Floor)

Finalmente, uno de los peores demonios de la conversión ADC (Analog-to-Digital Converter) es el error de redondeo de los bits. El error $e[n]$ se define como la diferencia entre el voltaje ideal y el escalón discreto asignado.

Este error $e[n]$, lejos de ser armónico, se asemeja a un **ruido blanco** uniforme que inyecta basura energética a lo largo de *todas* las frecuencias hasta la frontera de límite de Nyquist ($F_s/2$).

### 🧪 Demostración en Código (`plot_quantization_noise_floor`)
Tomamos una señal pura y la degradamos (por ejemplo a 4 bits). Luego, analizamos matemáticamente `señal_original - señal_cuantizada` y le sacamos la FFT a *solo el error*.
La gráfica de Plotly, en escala logarítmica (para visualizar correctamente lo que los ingenieros llaman el "Muro" o "Noise Floor"), muestra cómo el ruido de 4 bits se sostiene constante como una alfombra destructiva por sobre todo el espectro, tapando posibles armónicos menores que caigan por debajo de él.
