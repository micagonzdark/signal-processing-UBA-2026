# Clase 01: Fundamentos de DSP y Series Temporales

En este apunte se desglosan los 10 conceptos teóricos fundamentales de la Clase 1, analizando rigurosamente sus implicancias matemáticas y mostrando en qué parte exacta de nuestro proyecto de código (`main.py` y `serie_temporal_real.py`) fueron aplicados. Ocasionalmente usaremos notación matemática dura ya que es la base natural en el estudio de las señales.

---

## 1. Sistema de Procesamiento de Señales
Un sistema de procesamiento es un operador matemático, equipo físico o conjunto de algoritmos $\mathcal{H}$ que transforma una señal de entrada $x(t)$ o $x[n]$ en una señal de salida $y(t)$ o $y[n]$ para extraer información, limpiar ruido o analizar su comportamiento.
$$ y[n] = \mathcal{H}\{x[n]\} $$

**En el código:** Todo nuestro proyecto actual actúa integralmente como un sistema digital. Por ejemplo, en `serie_temporal_real.py`, el bloque que toma el Precio original $Y[n]$ y lo hace pasar por un promedio móvil para generar la Tendencia $T[n]$ es, en esencia, un **Filtro Pasa-Bajos** ($\mathcal{H}$), uno de los sistemas convolutivos más fundamentales en la historia del DSP.

## 2. Digitalización de una Señal Analógica
El mundo físico es infinito y continuo tanto en tiempo $t \in \mathbb{R}$ como en amplitud $x \in \mathbb{R}$. Las computadoras (con memoria finita) no pueden almacenar resoluciones infinitas, por lo que toda señal del mundo real que entra a una CPU sufre un proceso de digitalización, que siempre está dividido matemáticamente en dos etapas totalmente independientes:
1. **Discretización Temporal (Muestreo o Sampling):** Limitar los puntos de observación de $x(t) \to x[n]$.
2. **Discretización en Amplitud (Cuantización o Quantization):** Obligar infinitos valores intermedios a "redondearse" o calzar en niveles discretos artificiales $x_q[n] \in \{L_0, L_1, \dots, L_k\}$.

**En el código (`main.py`):** Simulamos el "mundo ideal y continuo" generando una señal senoidal con una altísima y densa resolución temporal (`t_continuous = np.linspace(0, duration, 1000)`). Acto seguido, aplicamos el muestreo extrayendo solo 1 de cada 20 valores (`t_continuous[::paso]`), y finalmente cuantizamos pasando el arreglo de datos por la función aritmética custom `quantize_signal`.

## 3. Teorema del Muestreo (Tiempo) y Muestreo en Amplitud
### Muestreo en el Tiempo (Teorema de Nyquist-Shannon)
El mandamiento más sagrado en el procesamiento de señales: para no perder información irrecuperablemente (fenómeno nocivo conocido como *Aliasing*, donde altas frecuencias se disfrazan como bajas), la frecuencia de muestreo $F_s$ (medida en Hertz: muestras por segundo) debe ser estrictamente mayor al doble de la máxima frecuencia presente en la señal continua original ($f_{max}$):
$$ F_s > 2 \cdot f_{max} $$

**En el código:** Nuestra señal compuesta estática (`main.py`) tiene un armónico fundamental de $5\text{ Hz}$ y un segundo armónico "rápido" sumado gravitando en torno a $12\text{ Hz}$. Por inferencia lógica analógica, $f_{max} = 12\text{ Hz}$. La teoría exige incondicionalmente $F_s > 24\text{ Hz}$. En el script definimos hardcodeadamente `fs_sampling = 50.0`, rebasando la cota de Nyquist y permitiendo retener las frecuencias originales intactas.

### Muestreo en Amplitud (Cuantización Matemática)
Si almacenamos amplitud usando memorias binarias de *b* bits, el número máximo de niveles estables posibles será $L = 2^b$. La distancia, escalón o salto fijo entre dos niveles adyacentes es lo que se conoce como **Resolución** $\Delta$:
$$ \Delta = \frac{V_{max} - V_{min}}{2^b - 1} $$
Todo valor $x[n]$ es redondeado hacia su peldaño más contiguo (usando minimización iterativa, interpolaciones o funciones techo), generando invariablemente el intrínseco **Error de Cuantización**:  $e[n] = x[n] - x_q[n]$.

**En el código (`utils.py`):** La estructura algorítmica de `quantize_signal` implementa numéricamente este mapeo. Le limitamos la capacidad destructiva a apenas $b=4$ bits, implicando que todo posible valor del voltaje fue reducido o comprimido a uno de solo $16$ escalones posibles ($2^4 = 16$), equiespaciados mediante `np.linspace(vmin, vmax, 16)`.

## 4. Aplicaciones
El procesamiento de señales es el corazón silencioso de la era cibernética y de cualquier máquina interactuante con el universo exterior. 
- Transceptores de modulación de antenas satelitales (GPS), WiFi 4G/5G.
- Ingeniería de Sonido, códecs de mp3 y sistemas de Inteligencia Artificial como Siri limpiando el ruido blanco del viento cuando hablas a tu micrófono.
- Electrocardiogramas Digitales, donde máquinas purifican las tenues ondas emitidas por el miocardio en presencia de severo ruido ambiental electromagnético.
- Trading algorítmico estadístico de alta volatilidad (Algorithmic Trading).

**En el código:** La aplicación que decidimos prototipar fue precisamente el análisis macro de la métrica financiera interactiva procesando, decantando y aislando el subyacente precio de un activo especulativo (Bitcoin).

## 5. Métodos de Análisis Computacional
Las matrices o arreglos numéricos de señales pueden ser sometidas a dos frentes de escrutinio bien demarcados:
1. **Dominio del Tiempo:** Se visualiza explícita y directamente la amplitud ($Y$) del array conforme suceden los tics del índice de actualización ($n$). Evaluamos transientes y retardos.
2. **Dominio de la Frecuencia (Espectral):** Valiéndonos de matemáticas complejas (Integración y la **Transformada Rápida de Fourier - FFT** y **Transformadas $\mathcal{Z}$**), la señal cambia de base, revelándonos misterios analíticos sobre las *energías frecuenciales que componen a la onda* en vez de *cuándo* ocurren. Es la visión radiológica preferida en el área.

**En el código:** Al tratarse solo de la Clase 1, hasta el momento el proyecto ha estado anclado enteramente al **Dominio del Tiempo**.

## 6. Descripción de una Serie Temporal
Una Serie Temporal (o *Time Series Process*) es una colección u ordenamiento secuencial de observaciones o variables aleatorias estocásticas, de toma distanciada uniformemente por incrementos en t ($t_n = n \cdot T_s$):
$$ \{ y[0], y[1], y[2], y[3], \dots, y[N] \} $$

## 7. Ejemplo Práctico de Serie Temporal
Un histórico de mediciones meteorológicas de satélites registradas cada 6 horas por la humedad media, las ventas absolutas o cierres del mercado bursátil emitidos cada atardecer a las 16hs por la NYSE.
**En el código:** Descargamos la Serie Temporal empírica (`BTC-USD`) con el gestor `yfinance`, con una Tasa de Muestreo Fija y absoluta de: $1\text{ muestra}/\text{día}$.

## 8. Detalle Estructural de la Serie Temporal
Bajo un espectro clásico sociológico/económico, a diferencia del sistema frecuencial puro, el comportamiento general de todo *Time Series* se subdivide convencionalmente asumiendo 3 subcomponentes primarios bajo el **Modelo Aditivo**:
$$ Y[n] = T[n] + S[n] + R[n] $$
1. **Tendencia Secuencial ($T[n]$ - Trend Segment):** El arrastre lento o transitorio en gran escala. Una de las operativas matemáticas rudimentarias para purificarla es calculando la media espacial (Media Móvil):
$$ T[n] = \frac{1}{W} \sum_{k=-(W/2)}^{(W/2)} Y[n-k] $$
2. **Estacionalidad u Oscilación ($S[n]$ - Seasonality Segment):** Fluctuaciones fuertemente auto-correlacionadas con períodos armónicos preestablecidos temporalmente. Picos en inviernos, navidades, franjas horarias etc.
3. **Ruido No Reversible ($R[n]$ - Residual/Noise Factor):** Una interferencia aleatoria de alto ritmo (Alta Frecuencia) que el núcleo analítico sistemático es incapaz de encausar.
**En el código (`serie_temporal_real.py`):** Realizamos el cálculo para descubrir $T[n]$ usando una inyección local de `.rolling(window=30 días)` y un centro métrico simétrico. Posteriormente, descubrimos la altísima variabilidad descontrolada del mercado $R[n]$ simplemente sustrayendo $Y[n] - T[n]$ por propiedades reflexivas.

## 9. Dominio del Tiempo Extenso
Es el plano gráfico dimensional puro donde la variable libre es ininterrumpidamente el eje cronológico de actualización $n$. Trabajar y observar el Dominio del Tiempo puro nos facilita computar analiticamente ciertas limitantes de ingeniería: tiempo de respuesta (Rise time), derivadas direccionales, caídas transitorias y porcentajes sistemáticos de *overshoot*. Nuestras gráficas iterables implementadas en *Plotly* lo demuestran elocuentemente en el eje x.

## 10. Generación de una Línea del Tiempo y su Serie Contigua
Todo entorno *sandbox* de simulación (como Python/NumPy) está obligado a definir una matriz basal continua explícita para poder operar el universo físico:
- **Paso analógico (`main.py`):** `t_continuous = np.linspace(0, 1.0, 1000)`. Crea un generador denso al interior del CPU de $10^3$ tensores para representar el contínuum espacio-infinito dentro de $[0, 1]s$. 
- **Paso Muestreado (Array Discretos):** `t_discrete = t_continuous[::paso_muestreo]`. Fuerza la selección escalonada acatando estrictamente el determinismo de la Teoría de Muestreo de Nyquist.
- **Series Formales Extendidas (`serie_temporal_real.py`):** La línea del tiempo trasciende la notación matemática $1, 2, 3..n$ en pos de Datetimes indexados con `pd.date_range()` (generados automáticamente por `yfinance`), asegurando rigor de *Time Series Analysis* real.
