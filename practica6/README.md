# APE 006 - Validación estadística de números pseudoaleatorios

**Asignatura:** Simulación  
**Unidad:** U2 - Generación de números pseudoaleatorios y generación de variables aleatorias  
**Tema:** Validación de uniformidad mediante Chi-cuadrado y Kolmogorov-Smirnov, con implementaciones independientes en Python y Java.

## Objetivo

Evaluar la calidad estadística de una secuencia de números pseudoaleatorios generada con el método congruencial lineal (LCG), aplicando las pruebas de bondad de ajuste Chi-cuadrado y Kolmogorov-Smirnov para decidir si los valores son compatibles con una distribución uniforme en `[0,1)`, y comparar los resultados de las implementaciones en Python y Java.

## Método LCG

El generador implementado sigue la fórmula:

```text
X(n+1) = (a * X(n) + c) mod m
U(n+1) = X(n+1) / m
```

Parámetros usados en **ambos lenguajes**:

| Parámetro | Valor |
|---|---:|
| Semilla (`X0`) | 12345 |
| Multiplicador (`a`) | 1664525 |
| Incremento (`c`) | 1013904223 |
| Módulo (`m`) | 2^32 = 4294967296 |

Con `a ≡ 1 (mod 4)` y `c` impar, este LCG tiene período completo `2^32` para el estado de 32 bits. En Java se usa `long` y la operación `% 2^32` para evitar desbordamientos. La normalización se hace con `X / 4294967296.0`, que produce exactamente los mismos valores `double` que Python.

La secuencia de 10 000 valores tiene SHA-256 de estados:

```text
23f2d027746be27c5723900296c8d6dd058da69f6fb8ebbf65c1822819dbd696
```

Ese hash coincide en Python y Java.

## Prueba Chi-cuadrado

Hipótesis:

- `H0`: los números siguen una distribución uniforme `U(0,1)`.
- `H1`: los números no siguen una distribución uniforme `U(0,1)`.

Configuración: 10 000 datos, 10 intervalos de amplitud 0.1, frecuencia esperada 1000 por intervalo, grados de libertad `10 - 1 = 9`, `α = 0.05`.

Procedimiento:

1. Se recorre la secuencia y se asigna cada valor al intervalo `[i/10, (i+1)/10)`; el último intervalo es cerrado por la derecha.
2. Se cuentan las frecuencias observadas `Oi`.
3. Se calcula `χ² = Σ ((Oi - Ei)² / Ei)`.
4. El valor p es la cola superior de la distribución Chi-cuadrado con 9 grados de libertad.
5. Se rechaza `H0` si `p < 0.05`.

El valor p se calcula con la función gamma incompleta regularizada `Q(gl/2, χ²/2)`, implementada con serie y fracción continua en Python y Java, sin depender de una biblioteca estadística externa. Esto garantiza el mismo procedimiento en ambos lenguajes.

## Prueba Kolmogorov-Smirnov

Se ordenan los datos y se compara la función de distribución empírica `Fn(x)` con la teórica `F(x) = x` para `U(0,1)`:

```text
D+ = max_i ( i/n - x_(i) )
D- = max_i ( x_(i) - (i-1)/n )
D  = max(D+, D-)
```

El valor p se obtiene con la distribución asintótica de Kolmogorov aplicando la corrección de Stephens (1970):

```text
λ = (sqrt(n) + 0.12 + 0.11/sqrt(n)) * D
p = P(K > λ)
```

Se documenta explícitamente que se usa una aproximación asintótica, adecuada para `n = 10 000`. Para `λ` pequeño se evalúa la serie de la CDF para evitar cancelación numérica; para `λ` grande se usa la serie alternante de la cola superior. La misma fórmula se implementa en Python y Java.

## Estructura del proyecto

```text
practica6/
├── Python/
│   ├── main.py
│   ├── lcg.py
│   ├── statistics_utils.py
│   ├── chi_square.py
│   ├── kolmogorov_smirnov.py
│   ├── plots.py
│   ├── tests_validacion.py
│   ├── requirements.txt
│   └── resultados/
│       ├── graficas/
│       └── datos/
├── Java/
│   ├── src/ape006/
│   │   ├── Main.java
│   │   ├── Lcg.java
│   │   ├── StatisticalFunctions.java
│   │   ├── ChiSquareTest.java
│   │   ├── KolmogorovSmirnovTest.java
│   │   ├── ExportUtils.java
│   │   ├── ResultsComparator.java
│   │   └── ValidationTests.java
│   ├── out/                  (clases compiladas, generadas)
│   └── resultados/
│       ├── datos/
│       └── graficas/
├── comparacion_resultados.py
└── README.md
```

## Requisitos

### Python

- Python 3.14.6 (probado).
- NumPy 2.5.4, Matplotlib 3.11.2, Pandas 3.1.1.
- Instalación:

```powershell
py -m pip install -r Python/requirements.txt
```

En este equipo el comando `python` apunta al alias de Microsoft Store y no funciona directamente; por eso los ejemplos usan el lanzador `py`. Si `python` está disponible en el sistema, puede usarse indistintamente.

### Java

- JDK 26.0.1 (probado).
- No requiere bibliotecas externas; solo la biblioteca estándar.
- Compilación:

```powershell
javac -encoding UTF-8 -d Java\out Java\src\ape006\*.java
```

Si PowerShell no expande el comodín, use:

```powershell
$fuentes = Get-ChildItem Java\src\ape006\*.java | ForEach-Object { $_.FullName }
javac -encoding UTF-8 -d Java\out $fuentes
```

## Comandos de ejecución

### Python

```powershell
# Menu interactivo
py Python\main.py

# Todos los resultados y graficas de Python
py Python\main.py --all

# Opciones individuales
py Python\main.py --generate 10000
py Python\main.py --chi
py Python\main.py --ks
py Python\main.py --compare
```

### Java

```powershell
# Compilar
javac -encoding UTF-8 -d Java\out Java\src\ape006\*.java

# Menu interactivo
java -cp Java\out ape006.Main

# Todos los resultados de Java
java -cp Java\out ape006.Main --all

# Opciones individuales
java -cp Java\out ape006.Main --generate 10000
java -cp Java\out ape006.Main --chi
java -cp Java\out ape006.Main --ks
java -cp Java\out ape006.Main --compare
```

### Comparación automática

```powershell
# Ejecuta realmente Python y Java y compara los resultados
py Python\comparacion_resultados.py

# Reutiliza resultados ya generados
py Python\comparacion_resultados.py --reuse
```

La comparación verifica parámetros, secuencia completa mediante SHA-256 y CSV, frecuencias observadas, estadísticos, grados de libertad, valores p y decisiones de Chi-cuadrado y Kolmogorov-Smirnov. El resultado se muestra en consola. Java también puede ejecutar su propia comparación con `ape006.Main --compare`.

### Pruebas controladas

```powershell
py Python\tests_validacion.py
java -cp Java\out ape006.ValidationTests
```

Las pruebas incluyen secuencias con frecuencias perfectas, límites exactos de intervalos (`0.1`, `0.9`, `0.999...`), valores conocidos de `D+`, `D-` y `D`, y valores críticos conocidos de Chi-cuadrado.

## Resultados obtenidos

### Chi-cuadrado (10 000 datos, 10 intervalos)

| Intervalo | Observado | Esperado | Diferencia |
|---|---:|---:|---:|
| [0.0, 0.1) | 1016 | 1000.0 | +16.0 |
| [0.1, 0.2) | 993 | 1000.0 | -7.0 |
| [0.2, 0.3) | 1049 | 1000.0 | +49.0 |
| [0.3, 0.4) | 940 | 1000.0 | -60.0 |
| [0.4, 0.5) | 949 | 1000.0 | -51.0 |
| [0.5, 0.6) | 1063 | 1000.0 | +63.0 |
| [0.6, 0.7) | 1014 | 1000.0 | +14.0 |
| [0.7, 0.8) | 1016 | 1000.0 | +16.0 |
| [0.8, 0.9) | 984 | 1000.0 | -16.0 |
| [0.9, 1.0] | 976 | 1000.0 | -24.0 |

- Estadístico: `χ² = 14.1600000000`
- Grados de libertad: `9`
- Valor p: `0.1167464640`
- Decisión: **no se rechaza H0** (`p = 0.116746 >= 0.05`).

### Kolmogorov-Smirnov

- `D+ = 0.0059602059`
- `D- = 0.0054111072`
- `D = 0.0059602059`
- Valor p: `0.8685666387`
- Decisión: **no se rechaza H0** (`p = 0.868567 >= 0.05`).

## Comparación Python vs Java

La comparación automática terminó con **todas las verificaciones en OK**:

- Misma secuencia de 10 000 estados (SHA-256 idéntico `23f2d0...b696`).
- Mismos 10 000 estados y valores `U` en los CSV.
- Mismas frecuencias observadas y mismo estadístico `χ² = 14.16`.
- Mismos `D+`, `D-`, `D` y valores p de KS.
- Mismas decisiones estadísticas.

## Gráficas

Ambas implementaciones generan sus propias graficas:

Python (`Python/resultados/graficas/`):
- `python_histograma.png`: histograma de los 10 000 valores frente a la densidad uniforme.
- `python_chi_cuadrado.png`: frecuencias observadas vs esperadas.
- `python_kolmogorov_smirnov.png`: ECDF vs `F(x) = x`.

Java (`Java/resultados/graficas/`):
- `java_histograma.png`: histograma de los 10 000 valores frente a la densidad uniforme.
- `java_chi_cuadrado.png`: frecuencias observadas vs esperadas.
- `java_kolmogorov_smirnov.png`: ECDF vs `F(x) = x`.

## Datos generados

- `Python/resultados/datos/python_secuencia_10000.csv`: secuencia completa de Python con estado y valor `U`.
- `Java/resultados/datos/java_secuencia_10000.csv`: secuencia completa de Java con estado y valor `U`.
- `Python/resultados/datos/python_chi_cuadrado.csv` y `Java/resultados/datos/java_chi_cuadrado.csv`: tablas de frecuencias.
- `Python/resultados/datos/python_resultados.json` y `Java/resultados/datos/java_resultados.json`: resultados completos para comparación automática.

## Limitaciones y supuestos

- Un resultado favorable en Chi-cuadrado o KS **no demuestra aleatoriedad verdadera**; solo indica que no se encontró evidencia suficiente de no uniformidad en la muestra analizada.
- El LCG es determinista. Con los parámetros usados tiene período `2^32`, pero presenta estructura de retículo y correlaciones propias de los generadores lineales.
- Solo se evaluó uniformidad univariada. No se aplicaron pruebas de independencia, rachas, autocorrelación, intervalos, poker, espectro, etc.
- El valor p de KS usa la aproximación asintótica con corrección de Stephens, documentada en el código.

## Entorno de ejecución

- Windows, Python 3.14.6, NumPy 2.5.4, Pandas 3.1.1, Matplotlib 3.11.2.
- JDK 26.0.1 (javac 26.0.1, Java HotSpot 64-bit).
