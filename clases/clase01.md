# Clase 01: Fundamentos de DSP y Series Temporales

En este apunte se desglosan los 10 conceptos teóricos fundamentales de la Clase 1, analizando sus implicancias matemáticas, aclarando las dudas conceptuales más comunes y mostrando en qué parte exacta de nuestro proyecto de código (`main.py` y `serie_temporal_real.py`) fueron aplicados. 

---

## 1. Sistema de Procesamiento de Señales
Un sistema de procesamiento es un operador matemático, equipo físico o conjunto de algoritmos $\mathcal{H}$ que **transforma** una señal de entrada $x(t)$ o $x[n]$ en una señal de salida $y(t)$ o $y[n]$. No solo "analiza", sino que altera la señal para extraer información o limpiar ruido.
$$y[n] = \mathcal{H}\{x[n]\}$$

**En el código:** Todo nuestro proyecto actúa como un sistema digital. Por ejemplo, en `serie_temporal_real.py`, la entrada $x[n]$ es el precio caótico y volátil del Bitcoin. El sistema $\mathcal{H}$ es nuestro Filtro de Media Móvil, y la salida $y[n]$ es la Tendencia suave y limpia. Transformamos el caos en orden.

## 2. Digitalización: El Pipeline de Datos
El mundo físico es infinito y continuo. Las computadoras tienen memoria finita. Por ende, debemos digitalizar. Pero es crucial entender de dónde vienen los datos:
1. **Pipeline Analógico-Digital (Ej. Clima):** La temperatura en el mundo real no pega saltos, es continua ($x(t)$). Un sensor físico la lee, la muestrea y la cuantiza. Lo que llega a Python ya es el producto final digitalizado ($x[n]$).
2. **Nativos Digitales (Ej. Finanzas):** El precio de una acción o de BTC no existe en el "aire". Nace a partir de transacciones digitales discretas. El pipeline aquí ignora el mundo analógico y empieza directamente en el análisis digital.

**En el código (`main.py`):** Simulamos el "mundo ideal y continuo" generando una señal con muchísima resolución temporal (`t_continuous`). Acto seguido, aplicamos la digitalización en sus dos etapas: Discretización Temporal (Muestreo) y Discretización en Amplitud (Cuantización).

## 3. Teorema del Muestreo y Cuantización (El concepto de $\Delta$)

### Muestreo en el Tiempo (Teorema de Nyquist-Shannon)
Para no perder información (y evitar el destructivo fenómeno del *Aliasing*, donde frecuencias altas se disfrazan de bajas), la frecuencia de muestreo $F_s$ debe ser estrictamente mayor al doble de la máxima frecuencia original ($f_{max}$):
$$F_s > 2 \cdot f_{max}$$
**En el código:** Nuestra señal compuesta tiene frecuencias de $5\text{ Hz}$ y $12\text{ Hz}$. Como $f_{max} = 12\text{ Hz}$, Nyquist exige incondicionalmente $F_s > 24\text{ Hz}$. Definimos `fs_sampling = 50.0`, cumpliendo la regla de sobra.

### Muestreo en Amplitud (Cuantización Matemática y $\Delta$)
Si almacenamos amplitud usando *b* bits, el número máximo de niveles posibles será $L = 2^b$. La distancia o tamaño del "escalón" entre niveles se llama **Resolución o Delta ($\Delta$)**:
$$\Delta = \frac{V_{max} - V_{min}}{2^b - 1}$$
*Metáfora:* Imagina medir personas con una regla que solo marca "cada 10 cm". Ese salto de 10 cm es tu $\Delta$. Si alguien mide 174 cm, el sistema lo obliga a redondear a 170 cm. Esa diferencia obligada es el **Error de Cuantización**.

## 4. Aplicaciones
El procesamiento de señales es el corazón de la era cibernética:
- Telecomunicaciones (WiFi, 5G, GPS).
- Ingeniería de Sonido (mp3, cancelación de ruido en micrófonos).
- Biomedicina (purificación de electrocardiogramas).
- Trading algorítmico estadístico.

**En el código:** Decidimos aplicar la teoría desarrollando un analizador para la métrica financiera del Bitcoin.

## 5. Métodos de Análisis Computacional
Las señales pueden ser escrutadas desde dos "ventanas" distintas:
1. **Dominio del Tiempo (Hoy):** Vemos "Cuándo" pasa algo. El eje X es el reloj. Es ideal para ver transientes, retrasos o tendencias. Es como leer una partitura de principio a fin.
2. **Dominio de la Frecuencia (Próximamente):** Ignoramos el reloj. Usando la Transformada de Fourier, vemos "Qué" componentes (energía/frecuencias) forman la señal. Es como mirar el ecualizador del estéreo para ver cuántos graves o agudos tiene la canción en total.

## 6. Descripción de una Serie Temporal
Una Serie Temporal es una colección secuencial de datos estocásticos (aleatorios), tomados de manera espaciada y uniforme a lo largo del tiempo ($t_n = n \cdot T_s$):
$$\{ y[0], y[1], y[2], y[3], \dots, y[N] \}$$

## 7. Ejemplo Práctico de Serie Temporal
Puede ser el registro meteorológico cada 6 horas o el valor de cierre de la bolsa.
**En el código:** Descargamos la Serie Temporal empírica `BTC-USD` usando `yfinance`, con una Tasa de Muestreo fija de: $1\text{ muestra}/\text{día}$.

## 8. Detalle Estructural de la Serie Temporal (Modelo Aditivo)
Asumimos que toda señal compleja es la suma de tres capas fundamentales:
$$Y[n] = T[n] + S[n] + R[n]$$

1. **Tendencia ($T[n]$ - Filtro de Media Móvil):** Extraemos el movimiento macro a largo plazo promediando los datos pasados según una "ventana" ($W$). Si $W=30$, cada nuevo punto es el promedio de los últimos 30 días, lo que "plancha" los picos rápidos y dibuja la tendencia real.
$$T[n] = \frac{1}{W} \sum_{k=0}^{W-1} Y[n-k]$$
2. **Estacionalidad ($S[n]$):** Patrones cíclicos fijos (ej. sube todos los veranos). **Importante:** En nuestro código de Bitcoin asumimos que $S[n] = 0$, ya que los activos financieros especulativos no tienen ciclos naturales garantizados.
3. **Ruido ($R[n]$):** Lo que no podemos explicar. Lo obtenemos restando la tendencia a la señal original.
$$R[n] = Y[n] - T[n] - S[n]$$

## 9. Dominio del Tiempo Extenso
Es el plano gráfico donde el eje libre es el avance ininterrumpido cronológico. Trabajar aquí nos permite computar tiempos de respuesta o caídas. 
**En el código:** Utilizamos gráficas dinámicas implementadas en **Plotly** para hacer zoom y explorar estos datos libremente en el eje temporal.

## 10. Generación de la Línea del Tiempo
Todo entorno de simulación (Python) necesita matrices explícitas de tiempo:
- **Paso Continuo Simulado:** `np.linspace(0, duration, 1000)`. Crea un arreglo denso.
- **Paso Muestreado:** `t_continuous[::paso_muestreo]`. Extracción saltando índices para simular el ADC.
- **Fechas Reales:** Al usar `yfinance`, trascendimos los números puros ($1, 2, 3$) y pasamos a usar `pd.date_range()`, manejando Datetimes formales.