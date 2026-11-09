# Práctica 05 — Generador Congruencial Lineal (LCG) en Python y Java

## Descripción

Esta práctica implementa desde cero el **Generador Congruencial Lineal (LCG)** en
Python y Java, utilizando exactamente los mismos parámetros y la misma
aritmética modular. El objetivo es comprobar que ambas implementaciones producen
la misma secuencia de 10 000 valores, analizar sus propiedades básicas y
visualizar su comportamiento.

No se utiliza ninguna función de números aleatorios de las bibliotecas estándar
para sustituir al LCG: la fórmula se implementa manualmente en ambos lenguajes.

---

## Objetivos

### Objetivo general

Comprender el funcionamiento de un generador pseudoaleatorio mediante la
implementación y el análisis del método LCG en Python y Java.

### Objetivos específicos

1. Implementar un generador LCG en Python.
2. Implementar el mismo algoritmo en Java respetando la aritmética modular de
   32 bits.
3. Comparar automáticamente las secuencias generadas y verificar su igualdad.
4. Analizar el período del generador y sus condiciones teóricas.
5. Visualizar la secuencia, su distribución y la relación entre valores
   consecutivos.
6. Estudiar el efecto de cambiar la semilla inicial.

---

## Fundamento matemático

El Generador Congruencial Lineal se define mediante la relación recursiva:

```text
X(n+1) = (a · X(n) + c) mod m
```

Los valores normalizados en el intervalo `[0, 1)` se obtienen mediante:

```text
U(n) = X(n) / m
```

Donde:

- `X(0)` es la semilla inicial.
- `a` es el multiplicador.
- `c` es el incremento.
- `m` es el módulo.
- `X(n)` es un estado entero en el intervalo `[0, m - 1]`.
- `U(n)` es el valor pseudoaleatorio normalizado.

Para el módulo `m = 2^32`, la operación `mod m` equivale a conservar los 32 bits
menos significativos del resultado. En Java se utiliza un `long` junto con la
máscara `0xFFFFFFFFL` para evitar el desbordamiento con signo de `int` y
reproducir exactamente el comportamiento de Python, cuyos enteros tienen
precisión arbitraria.

---

## Parámetros utilizados

| Parámetro | Valor |
|---|---:|
| Multiplicador `a` | `1 664 525` |
| Incremento `c` | `1 013 904 223` |
| Módulo `m` | `2^32 = 4 294 967 296` |
| Semilla principal `X0` | `12 345` |
| Semilla alternativa | `54 321` |
| Cantidad de valores por secuencia | `10 000` |

Las dos implementaciones generan `X(1), X(2), ..., X(10 000)`, es decir, 10 000
valores posteriores a la semilla. El CSV tiene 10 001 líneas contando el
encabezado.

---

## Estructura del proyecto

```text
practica5/
│
├── python/
│   ├── main.py
│   ├── generador_lcg.py
│   ├── analisis.py
│   ├── graficas.py
│   ├── graficas/
│   │   ├── secuencia_x.png
│   │   ├── valores_u.png
│   │   ├── histograma_u.png
│   │   ├── dispersion_u.png
│   │   └── comparacion_semillas.png
│   └── resultados/
│       ├── secuencia_python.csv
│       └── secuencia_python_semilla_54321.csv
│
├── java/
│   ├── src/
│   │   ├── Main.java
│   │   └── GeneradorLCG.java
│   ├── out/                         # Clases compiladas (se crea al compilar)
│   ├── graficas/
│   │   ├── secuencia_x.png
│   │   ├── valores_u.png
│   │   ├── histograma_u.png
│   │   ├── dispersion_u.png
│   │   └── comparacion_semillas.png
│   └── resultados/
│       ├── secuencia_java.csv
│       └── secuencia_java_semilla_54321.csv
│
├── comparacion/
│   ├── comparar.py
│   └── resultados/
│       ├── comparacion_20.csv
│       └── comparacion_semillas_20.csv
│
├── README.md
└── requirements.txt
```

Responsabilidades:

- `generador_lcg.py`: implementación matemática del LCG y validación de
  parámetros.
- `analisis.py`: estadísticas descriptivas, búsqueda de repeticiones y
  verificación de las condiciones de período máximo.
- `graficas.py`: generación de las cinco gráficas con Matplotlib.
- `main.py`: orquesta la generación, el guardado de CSV, el análisis y las
  gráficas de Python en `python/graficas/`.
- `GeneradorLCG.java`: implementación Java del mismo algoritmo.
- `Main.java`: genera los CSV de Java y muestra los primeros valores.
- `comparar.py`: compara Python contra Java, compara las dos semillas, genera
  las tablas de comparación y produce las gráficas de Java en `java/graficas/`
  a partir de los CSV propios de Java (usando Matplotlib).

---

## Requisitos e instalación

### Requisitos

- Python 3.10 o superior.
- Matplotlib 3.7 o superior.
- JDK 17 o superior (`javac` y `java` disponibles).

### Instalación de dependencias de Python

Desde la carpeta `practica5`:

```powershell
python -m pip install -r requirements.txt
```

Si en Windows el comando `python` abre Microsoft Store o no está en el `PATH`,
puede utilizarse la ruta completa. En este equipo la instalación disponible está
en:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" -m pip install -r requirements.txt
```

Las dependencias de Java no requieren instalación adicional; basta con tener el
JDK configurado.

---

## Ejecución

Los comandos deben ejecutarse desde la carpeta raíz `practica5`.

### 1. Ejecutar la implementación Python

```powershell
python python/main.py
```

Alternativa si Python no está en el `PATH`:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" python\main.py
```

Esta ejecución:

1. Genera 10 000 valores con semilla `12 345`.
2. Guarda `python/resultados/secuencia_python.csv`.
3. Genera otros 10 000 valores con semilla `54 321`.
4. Guarda `python/resultados/secuencia_python_semilla_54321.csv`.
5. Calcula estadísticas descriptivas y analiza el período.
6. Crea las cinco gráficas de Python en `python/graficas/`.

### 2. Compilar y ejecutar Java

```powershell
javac -encoding UTF-8 -d java/out java/src/GeneradorLCG.java java/src/Main.java
java -cp java/out Main
```

La ejecución sin argumentos genera:

- `java/resultados/secuencia_java.csv` con semilla `12 345`.
- `java/resultados/secuencia_java_semilla_54321.csv` con semilla `54 321`.

También es posible generar una secuencia personalizada:

```powershell
java -cp java/out Main 999 java/resultados/secuencia_personalizada.csv
```

### 3. Comparar las secuencias

```powershell
python comparacion/comparar.py
```

Alternativa:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" comparacion\comparar.py
```

La comparación debe ejecutarse después de Python y Java. El script:

- Verifica los 10 000 valores de la semilla principal en ambos lenguajes.
- Compara las primeras 20 observaciones y crea
  `comparacion/resultados/comparacion_20.csv`.
- Compara las secuencias de semillas `12 345` y `54 321` y crea
  `comparacion/resultados/comparacion_semillas_20.csv`.
- Verifica también la semilla `54 321` entre Python y Java.
- Genera las cinco gráficas de Java en `java/graficas/` a partir de los CSV de
  Java, usando Matplotlib.
- Devuelve un código de salida distinto de cero si encuentra alguna diferencia.

---

## Archivos generados

### Archivos CSV

| Archivo | Contenido |
|---|---|
| `python/resultados/secuencia_python.csv` | 10 000 valores de Python con semilla 12 345 |
| `python/resultados/secuencia_python_semilla_54321.csv` | 10 000 valores de Python con semilla 54 321 |
| `java/resultados/secuencia_java.csv` | 10 000 valores de Java con semilla 12 345 |
| `java/resultados/secuencia_java_semilla_54321.csv` | 10 000 valores de Java con semilla 54 321 |
| `comparacion/resultados/comparacion_20.csv` | Comparación Python/Java de las primeras 20 observaciones |
| `comparacion/resultados/comparacion_semillas_20.csv` | Comparación de semillas de las primeras 20 observaciones |

Los CSV de secuencias tienen el formato:

```csv
iteracion,X,U
1,87628868,0.020402685739
2,71072467,0.016547848238
...
```

La columna `U` se escribe con 12 decimales para mantener una representación
común y legible en ambos lenguajes.

### Gráficas

Cada lenguaje tiene su propia carpeta de gráficas: `python/graficas/` y
`java/graficas/`. Las gráficas de Java se generan con Matplotlib a partir de los
CSV producidos por Java, de modo que cada carpeta contiene las gráficas de sus
propios resultados.

| Archivo | Descripción |
|---|---|
| `python/graficas/secuencia_x.png` y `java/graficas/secuencia_x.png` | `X(n)` frente al número de iteración |
| `python/graficas/valores_u.png` y `java/graficas/valores_u.png` | Valores normalizados `U(n)` |
| `python/graficas/histograma_u.png` y `java/graficas/histograma_u.png` | Histograma de `U(n)` con la densidad uniforme esperada |
| `python/graficas/dispersion_u.png` y `java/graficas/dispersion_u.png` | Dispersión de pares `(U(n), U(n+1))` |
| `python/graficas/comparacion_semillas.png` y `java/graficas/comparacion_semillas.png` | Comparación de las primeras 100 observaciones con ambas semillas |

---

## Resultados obtenidos

Los resultados siguientes fueron producidos por la ejecución real del proyecto.

### Primeros cinco valores

| `n` | `X(n)` Python | `X(n)` Java | `U(n)` |
|---:|---:|---:|---:|
| 1 | 87 628 868 | 87 628 868 | 0.020402685739 |
| 2 | 71 072 467 | 71 072 467 | 0.016547848238 |
| 3 | 2 332 836 374 | 2 332 836 374 | 0.543155794498 |
| 4 | 2 726 892 157 | 2 726 892 157 | 0.634904056089 |
| 5 | 3 908 547 000 | 3 908 547 000 | 0.910029513761 |

### Comparación Python contra Java

- Coincidencias exactas de `X`: **10 000 de 10 000**.
- Diferencia máxima absoluta entre los valores `U`: **0.000e+00**.
- Discrepancias: **0**.
- Los archivos CSV completos coinciden línea por línea y tienen el mismo hash
  SHA-256:
  `ACFA4457407484EFB52C1CB8560B563F5CD2954261FA9C3F6EEEBF05E406819E`.
- Conclusión: las secuencias de Python y Java son idénticas para la semilla
  principal.

La misma verificación se realizó con la semilla `54 321`: **10 000 de 10 000**
coincidencias exactas y diferencia máxima `0.000e+00`.

### Estadísticas descriptivas de `U(n)` con semilla 12 345

| Medida | Valor observado | Valor esperado para `U(0,1)` |
|---|---:|---:|
| Media | 0.498769847970 | 0.500000000000 |
| Desviación estándar | 0.288117626755 | 0.288675134595 |
| Mínimo | 0.000059082638 | 0.000000000000 |
| Máximo | 0.999925965443 | cercano a 1 |
| Mediana | 0.504595871898 | 0.500000000000 |

Estos valores son descriptivos y coherentes con una distribución uniforme en
`[0, 1)`. El histograma permite observar esa aproximación. No se realizó una
prueba formal de uniformidad porque no formaba parte de las actividades
solicitadas.

---

## Análisis del período

El **período** de un generador es la cantidad de estados que se generan antes de
que un valor vuelva a repetirse y comience un nuevo ciclo. Cuando el período es
`P`, se cumple `X(n + P) = X(n)` para todo `n` suficientemente grande.

En esta práctica se generaron 10 000 valores. Al buscar repeticiones del estado
`X` dentro de esa muestra:

- Se obtuvieron **10 000 estados distintos**.
- **No se encontró ninguna repetición** dentro de los 10 000 valores.
- Por lo tanto, puede afirmarse únicamente que el período observado es **mayor
  que 10 000**. No es correcto afirmar que se comprobó el período completo.

Sin embargo, los parámetros cumplen las condiciones de Hull-Dobell para un
módulo de la forma `m = 2^k`:

1. `m = 2^32` es una potencia de 2.
2. `c = 1 013 904 223` es impar, por lo que es coprimo con `m`.
3. `a = 1 664 525` es congruente con `1` módulo `4`, ya que
   `1 664 525 mod 4 = 1`.

En consecuencia, el **período máximo teórico es `m = 2^32 = 4 294 967 296`**.
Con 10 000 valores no es posible comprobarlo experimentalmente; para ello sería
necesario generar miles de millones de estados.

---

## Cambio de semilla

Al cambiar la semilla de `12 345` a `54 321` y generar otros 10 000 valores:

- Las primeras 20 observaciones son diferentes en ambas secuencias.
- En las 10 000 posiciones comparadas, las coincidencias exactas de `X` fueron
  **0 de 10 000**.
- Ambas secuencias usan la misma recurrencia y los mismos parámetros, pero
  parten de un estado inicial distinto.
- Como el generador tiene período máximo teórico, ambas semillas recorren el
  mismo ciclo de estados, pero en posiciones diferentes del ciclo.
- La semilla no cambia el período ni la distribución teórica; solo cambia el
  punto de partida y, por tanto, la secuencia concreta observada.

Las gráficas `python/graficas/comparacion_semillas.png` y
`java/graficas/comparacion_semillas.png` muestran las diferencias entre las
primeras 100 observaciones de ambas semillas.

---

## Interpretación de los resultados

1. La implementación manual del LCG produce los mismos valores en Python y Java
   cuando se usan los mismos parámetros.
2. La aritmética de Java con `long` y la máscara de 32 bits reproduce
   correctamente el comportamiento modular de `2^32` sin desbordamientos con
   signo.
3. La secuencia normalizada ocupa el intervalo `[0, 1)` y su histograma es
   compatible con una distribución uniforme.
4. El gráfico de dispersión de pares consecutivos no muestra una estructura
   evidente para la muestra generada, lo cual es deseable en un generador
   pseudoaleatorio.
5. El análisis de período solo permite afirmar que no hubo repeticiones en los
   10 000 valores generados; el período máximo de `2^32` es una conclusión
   teórica basada en las condiciones de Hull-Dobell, no una comprobación
   exhaustiva.
6. El cambio de semilla produce una secuencia diferente sin modificar el
   algoritmo ni la calidad teórica del generador.

---

## Limitaciones

- No se generaron los `4 294 967 296` estados necesarios para comprobar
  experimentalmente el período completo.
- El análisis estadístico es descriptivo; no se aplicaron pruebas de
  uniformidad, independencia ni bondad de ajuste.
- La comparación de los valores `U` se realiza con una tolerancia de `1e-9`
  sobre los valores escritos con 12 decimales. La verificación decisiva es la
  igualdad exacta de los enteros `X`, que fue total.
- La implementación Java está orientada a módulos potencia de 2, que es el caso
  de esta práctica (`2^32`). El código incluye una rama con `%` para otros
  módulos, pero no se utiliza en los resultados presentados.

---

## Comandos completos de ejecución

```powershell
# 1. Instalar dependencias
python -m pip install -r requirements.txt

# 2. Ejecutar Python
python python/main.py

# 3. Compilar y ejecutar Java
javac -encoding UTF-8 -d java/out java/src/GeneradorLCG.java java/src/Main.java
java -cp java/out Main

# 4. Comparar las secuencias y generar las tablas
python comparacion/comparar.py
```

En un equipo donde `python` no esté disponible en el `PATH`, sustituir los
comandos de Python por:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" python\main.py
& "$env:LOCALAPPDATA\Python\bin\python.exe" comparacion\comparar.py
```
