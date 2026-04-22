# Clase 02: El Dominio de la Frecuencia

Esta clase marca la transición del análisis clásico en el **dominio del tiempo** (donde observamos la evolución de la señal segundo a segundo) hacia el **dominio de la frecuencia**, permitiéndonos descomponer las señales en sus ingredientes (tonos puros o armónicos) gracias a la Transformada de Fourier.

A continuación vemos los temas clave y cómo se aplican matemáticamente en el código de nuestro proyecto.

---

## 1. De la Serie Temporal al Dominio Espectral (FT, DFT, FFT)

La **Transformada de Fourier** establece que cualquier señal periódica o de energía finita se puede representar como una suma infinita de senos y cosenos de distintas frecuencias. En el mundo del procesamiento digital (con computadoras), no podemos usar integrales continuas (FT), por lo que usamos la **Transformada Discreta de Fourier (DFT)**.

Para calcularla de manera computacionalmente eficiente, usamos un algoritmo llamado **Fast Fourier Transform (FFT)**, que reduce enormemente la cantidad de operaciones matemáticas necesarias, de $O(N^2)$ a $O(N \log N)$.

### 🔗 Vínculo con el Proyecto: Implementación de FFT
En nuestro código, aislamos toda la complejidad del motor FFT dentro del archivo `utils.py`:
- **Función:** `calculate_fft(signal, fs)`
- **Línea ~39 de `utils.py`:**
  ```python
  fft_result = np.fft.fft(signal)
  freqs = np.fft.fftfreq(N, d=1/fs)
  ```
- **Simetría Hermitiana:** Como nuestras señales son números reales, la mitad del espectro (las frecuencias negativas) contiene información redundante. En el código recortamos el array a `half_N` y **multiplicamos la amplitud por `2/N`**. Dividir por N normaliza la magnitud que el algoritmo FFT hace crecer, y multiplicar por 2 recompensa la energía perdida al descartar las frecuencias negativas para que el pico resultante mida exactamente lo mismo que la amplitud del seno original.

---

## 2. Senoidales y su Espectro

Si analizamos un **tono puro** (una función seno perfecta) en el tiempo, vemos una oscilación constante. En el dominio de la frecuencia, la Transformada de Fourier de un seno ideal infinito es un par de **Deltas de Dirac** (impactos de anchura nula y altura infinita) ubicados en su frecuencia fundamental $+f_0$ y $-f_0$. Para fines prácticos y al usar señales reales cortadas abruptamente por computadoras, veremos picos concentrados.

Cuando generamos la **Suma de dos senoidales** (ej. $f_1 = 5$ Hz y $f_2 = 12$ Hz), estamos aplicando el **principio de linealidad**. La función en el tiempo puede parecer caótica, pero la FFT obedece a la linealidad matemática: $FFT(A + B) = FFT(A) + FFT(B)$.

### 🔗 Vínculo con el Proyecto: Descomposición de Senoidales
En el dashboard 1 de nuestro `main.py`:
- **Construcción:** Sumamos un seno de 5Hz + un seno de 12Hz + Ruido y generamos `y_continuous`.
- **Análisis Visual:** En el gráfico inferior que muestra la FFT, vas a notar exactamente **dos picos agudos**, uno sobre $X=5$ y otro sobre $X=12$. De esta forma, el análisis espectral corta a través del ruido del dominio temporal y revela los picos limpios y puros ocultos en la señal general.

---

## 3. Pulsos Rectangulares y su Respuesta en Frecuencia

Un **pulso rectangular** (o compuerta $rect(t)$) se caracteriza por tener una amplitud constante durante un intervalo de tiempo y ser cero en el resto.
Es muy interesante matemáticamente porque representa un cambio repentino. Una regla clave en DSP dice: *Cuanto más corta/rápida sea una transición en el tiempo, más bandas de frecuencias requiere para poder formarse.*

Por esto, la Transformada de Fourier de un pulso rectangular toma la forma de una de las funciones más célebres en señales: la **Función Sinc** ($\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$). El espectro no es un simple delta; se esparce con un lóbulo principal ancho alrededor del nivel DC (0 Hz) y lóbulos secundarios que oscilan tendiendo a cero en el infinito.

### 🔗 Vínculo con el Proyecto: Simulación del Pulso Sinc
En el archivo `utils.py` y `main.py` recreamos este fenómeno de laboratorio:
1. **Generación:** En la función `generate_pulse` dentro de `utils.py`, forzamos matemáticamente el vector de amplitudes a ser `1.0` solo en un marco contenido dentro de `t_start` y `t_end`.
2. **Visualización:** Al ejecutar el segundo Dashboard de `main.py` (en la función `plot_pulse_fft()`), Plotly te renderizará de lado izquierdo el ancho del pulso temporal, y en el derecho el espectro en magnitud absoluto. Podrás observar visualmente que el espectro decae con rebotes formando la copa de la "Sinc". En lugar de tener picos discretos, un evento irrepetible (aperiódico) genera un **espectro continuo** (una huella frecuencial corrida por todos los anchos de banda).
