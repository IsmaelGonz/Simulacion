# APE 006 - Validación estadística de números pseudoaleatorios

![Python](https://img.shields.io/badge/Python-3.14.6-3776AB?logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-26.0.1-ED8B00?logo=openjdk&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.5.4-013243?logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.1.1-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-11557C)
![Asignatura](https://img.shields.io/badge/Simulacion-U2-blue)

**Asignatura:** Simulación  
**Unidad:** U2 - Generación de números pseudoaleatorios y generación de variables aleatorias  
**Tema:** Validación de uniformidad mediante Chi-cuadrado y Kolmogorov-Smirnov, con implementaciones independientes en Python y Java.

---

## Tabla de contenidos

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Tecnologías utilizadas](#2-tecnologías-utilizadas)
3. [Instalación](#3-instalación)
4. [Configuración del proyecto](#4-configuración-del-proyecto)
5. [Uso del proyecto](#5-uso-del-proyecto)
6. [Estructura del proyecto](#6-estructura-del-proyecto)
7. [Información adicional](#7-información-adicional)

---

## 1. Descripción del proyecto

**Nombre:** APE 006 - Validación estadística de números pseudoaleatorios.

Este proyecto implementa, de forma independiente en **Python** y **Java**, un generador congruencial lineal (LCG) y dos pruebas de bondad de ajuste para evaluar si una secuencia de números pseudoaleatorios es compatible con una distribución uniforme en `[0,1)`:

- **Chi-cuadrado** sobre frecuencias por intervalos.
- **Kolmogorov-Smirnov** de una muestra contra `U(0,1)`.

El propósito principal es **verificar la calidad estadística de la secuencia generada** y **demostrar que ambas implementaciones producen exactamente los mismos resultados**. Para ello se comparan parámetros, secuencias completas mediante SHA-256, frecuencias, estadísticos, valores p y decisiones.

El problema que aborda es la necesidad de validar un generador pseudoaleatorio antes de usarlo en simulación. Un resultado favorable no demuestra aleatoriedad verdadera, pero permite descartar evidencia suficiente de no uniformidad en la muestra analizada.

### Objetivos principales

- Implementar un LCG reproducible con parámetros idénticos en Python y Java.
- Aplicar las pruebas de Chi-cuadrado y Kolmogorov-Smirnov con el mismo procedimiento en ambos lenguajes.
- Calcular los valores p sin depender de bibliotecas estadísticas externas.
- Exportar resultados en CSV y JSON, y generar gráficas de apoyo.
- Comparar automáticamente las salidas de Python y Java.
- Incluir pruebas controladas con valores conocidos.

### Funcionalidades principales

- Generación de secuencias pseudoaleatorias de tamaño configurable.
- Menú interactivo y ejecución por argumentos de línea de comandos.
- Prueba Chi-cuadrado con 10 intervalos y `α = 0.05` por defecto.
- Prueba Kolmogorov-Smirnov con aproximación asintótica y corrección de Stephens.
- Exportación de secuencias, tablas de frecuencia y resultados completos.
- Generación de histogramas, gráficas de Chi-cuadrado y de ECDF vs `F(x) = x`.
- Comparación Python vs Java y pruebas de validación en ambos lenguajes.

---

## 2. Tecnologías utilizadas

| Categoría | Tecnología | Uso en el proyecto |
|---|---|---|
| Lenguaje | Python 3.14.6 | Implementación principal, análisis estadístico, gráficas y comparación |
| Lenguaje | Java 26.0.1 | Segunda implementación independiente con la biblioteca estándar |
| Biblioteca | NumPy 2.5.4 | Cálculo numérico y datos para gráficas |
| Biblioteca | pandas 3.1.1 | Exportación de secuencias y tablas a CSV |
| Biblioteca | Matplotlib 3.11.2 | Generación de gráficas PNG en Python |
| Biblioteca estándar Java | Java2D / ImageIO / `java.security` | Gráficas PNG y cálculo de SHA-256 en Java |
| Formato de datos | CSV | Secuencias y tablas de frecuencias |
| Formato de datos | JSON | Resultados completos para comparación automática |
| Formato de imagen | PNG | Gráficas de resultados |
| Control de versiones | Git | Gestión del repositorio |

### Aclaraciones

- **No se utiliza base de datos.** Los resultados se almacenan en archivos CSV, JSON y PNG.
- **No existe frontend web ni backend HTTP.** La interfaz es de línea de comandos (menú interactivo o argumentos).
- **No se utilizan servicios externos ni llamadas de red** durante la ejecución.
- **No se requieren bibliotecas estadísticas externas.** Los valores p se calculan con implementaciones propias de la gamma incompleta regularizada y de la distribución asintótica de Kolmogorov.

---

## 3. Instalación

### Requisitos previos

| Herramienta | Versión probada | Notas |
|---|---:|---|
| Python | 3.14.6 | Usar `py` en Windows o `python3` en Linux/macOS |
| pip | Incluido con Python | Necesario para instalar dependencias |
| NumPy | 2.5.4 | `requirements.txt` declara `numpy>=2.0` |
| pandas | 3.1.1 | `requirements.txt` declara `pandas>=2.0` |
| Matplotlib | 3.11.2 | `requirements.txt` declara `matplotlib>=3.8` |
| JDK | 26.0.1 (Oracle) | Se requieren `javac` y `java` en el `PATH` |
| Git | No especificada | Solo necesaria para clonar el repositorio |

> El proyecto fue probado en **Windows 11**. Los comandos para Linux/macOS se incluyen cuando aplica. Las versiones indicadas corresponden al entorno registrado en los resultados del repositorio.

### 1. Clonar el repositorio

```bash
git clone https://github.com/IsmaelGonz/Simulacion.git
cd Simulacion/practica6
```

> Ejecute todos los comandos desde la raíz de `practica6`, porque la implementación Java resuelve las rutas de salida a partir del directorio de trabajo.

### 2. Crear y activar un entorno virtual (recomendado para Python)

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias de Python

**Windows:**

```powershell
py -m pip install -r Python\requirements.txt
```

**Linux / macOS:**

```bash
python -m pip install -r Python/requirements.txt
```

Si el entorno virtual está activo, puede usar `python` en lugar de `py`.

> En el equipo donde se probó el proyecto, el comando `python` de Windows apuntaba al alias de Microsoft Store y no funcionaba directamente; por eso los ejemplos usan el lanzador `py`.

### 4. Compilar Java (opcional, para la implementación Java)

**Windows:**

```powershell
javac -encoding UTF-8 -d Java\out Java\src\ape006\*.java
```

Si PowerShell no expande el comodín, ejecute:

```powershell
$fuentes = Get-ChildItem Java\src\ape006\*.java | ForEach-Object { $_.FullName }
javac -encoding UTF-8 -d Java\out $fuentes
```

**Linux / macOS:**

```bash
javac -encoding UTF-8 -d Java/out Java/src/ape006/*.java
```

### 5. Preparación de datos y resultados

No existe una base de datos ni una migración inicial. Los directorios de salida se crean automáticamente la primera vez que se ejecuta cada implementación:

- `Python/resultados/datos/` y `Python/resultados/graficas/`
- `Java/resultados/datos/` y `Java/resultados/graficas/`

---

## 4. Configuración del proyecto

El proyecto **no utiliza variables de entorno** ni archivos `.env`. Tampoco requiere credenciales, tokens ni claves de API.

### Archivos de configuración

| Archivo | Función |
|---|---|
| `Python/requirements.txt` | Declara las dependencias de Python (`numpy`, `matplotlib`, `pandas`) |
| `.gitignore` | Excluye `__pycache__/`, `*.pyc`, `Java/out/` y `*.class` |

### Parámetros del generador LCG

Los parámetros están definidos en `Python/lcg.py` y `Java/src/ape006/Lcg.java`. Ambos deben coincidir para que las secuencias sean idénticas.

| Parámetro | Valor | Descripción |
|---|---:|---|
| Semilla (`X0`) | `12345` | Estado inicial del generador |
| Multiplicador (`a`) | `1664525` | Multiplicador del LCG |
| Incremento (`c`) | `1013904223` | Constante aditiva |
| Módulo (`m`) | `4294967296` (`2^32`) | Rango del estado |

### Parámetros de ejecución

| Parámetro | Valor por defecto | Dónde se define |
|---|---:|---|
| Cantidad de números | `10000` | `DEFAULT_N` en `main.py` / `Main.java` |
| Intervalos de Chi-cuadrado | `10` | Llamada a `run_chi_square` / `ChiSquareTest.run` |
| Nivel de significancia (`α`) | `0.05` | Llamada a las pruebas en ambos lenguajes |
| Intervalos del histograma | `20` | `plots.py` y `Plots.java` |

> Los parámetros son valores por defecto en el código. Si necesita modificarlos, debe editar la fuente correspondiente; el proyecto no los expone mediante variables de entorno.

### Configuraciones de seguridad

- No se almacenan ni solicitan contraseñas, tokens o claves.
- No se realizan conexiones a servicios externos.
- Los resultados generados no contienen datos personales ni credenciales.

---

## 5. Uso del proyecto

La aplicación se ejecuta desde la **raíz del proyecto**. Sin argumentos, cada implementación muestra un menú interactivo.

### Python

```powershell
# Menú interactivo
py Python\main.py

# Generar todos los resultados y gráficas de Python
py Python\main.py --all

# Opciones individuales
py Python\main.py --generate 10000
py Python\main.py --chi
py Python\main.py --ks
py Python\main.py --compare
```

En Linux/macOS, reemplace `py` por `python` y use `/` en las rutas:

```bash
python Python/main.py --all
```

Opciones disponibles:

| Opción | Descripción |
|---|---|
| Sin argumentos | Menú interactivo |
| `--all` | Genera secuencia, ejecuta ambas pruebas, exporta CSV/JSON y crea gráficas |
| `--generate N` | Genera una secuencia de `N` números (por defecto `10000`) |
| `--chi` | Ejecuta la prueba Chi-cuadrado sobre la secuencia de 10 000 datos |
| `--ks` | Ejecuta la prueba Kolmogorov-Smirnov sobre la secuencia de 10 000 datos |
| `--compare` | Ejecuta la comparación Python vs Java |

### Java

```powershell
# Compilar
javac -encoding UTF-8 -d Java\out Java\src\ape006\*.java

# Menú interactivo
java -cp Java\out ape006.Main

# Generar todos los resultados de Java
java -cp Java\out ape006.Main --all

# Opciones individuales
java -cp Java\out ape006.Main --generate 10000
java -cp Java\out ape006.Main --chi
java -cp Java\out ape006.Main --ks
java -cp Java\out ape006.Main --compare
```

Opciones disponibles:

| Opción | Descripción |
|---|---|
| Sin argumentos | Menú interactivo |
| `--all` | Genera secuencia, ejecuta ambas pruebas, exporta CSV/JSON y crea gráficas |
| `--generate N` | Genera una secuencia de `N` números (por defecto `10000`) |
| `--chi` | Ejecuta la prueba Chi-cuadrado |
| `--ks` | Ejecuta la prueba Kolmogorov-Smirnov |
| `--compare` | Compara los JSON de Python y Java ya generados |
| `--help` | Muestra la ayuda de la línea de comandos |

> `ape006.Main --compare` **no ejecuta Python**; solo compara archivos de resultados existentes. Para generar ambos y comparar, use el script de comparación.

### Comparación automática

```powershell
# Ejecuta realmente Python y Java, y luego compara los resultados
py Python\comparacion_resultados.py

# Reutiliza resultados ya generados
py Python\comparacion_resultados.py --reuse

# Omitir la ejecución de una implementación
py Python\comparacion_resultados.py --skip-python
py Python\comparacion_resultados.py --skip-java
```

Este script compila y ejecuta Java por su cuenta, por lo que `javac` y `java` deben estar disponibles en el `PATH`. La comparación verifica:

- Parámetros del LCG.
- Secuencia completa de 10 000 estados mediante SHA-256.
- Estados y valores `U` completos en los CSV.
- Frecuencias observadas y esperadas de Chi-cuadrado.
- Estadístico, grados de libertad, valor p y decisión de Chi-cuadrado.
- `D+`, `D-`, `D`, valor p y decisión de Kolmogorov-Smirnov.

### Pruebas controladas

```powershell
# Pruebas de Python
py Python\tests_validacion.py

# Pruebas de Java (requiere compilar primero)
java -cp Java\out ape006.ValidationTests
```

Las pruebas incluyen secuencias con frecuencias perfectas, límites exactos de intervalos, valores conocidos de `D+`, `D-` y `D`, valores críticos de Chi-cuadrado, SHA-256 esperado y validación de valores fuera de `[0,1)`.

### Salidas generadas

| Implementación | Datos | Gráficas |
|---|---|---|
| Python | `Python/resultados/datos/` | `Python/resultados/graficas/` |
| Java | `Java/resultados/datos/` | `Java/resultados/graficas/` |

Archivos principales:

- `*_secuencia_10000.csv`: secuencia completa con índice, estado y valor `U`. Para un tamaño `N` distinto, el archivo se nombra `*_secuencia_<N>.csv`.
- `*_chi_cuadrado.csv`: frecuencias observadas, esperadas y diferencias.
- `*_resultados.json`: resultados completos usados por la comparación.
- `muestra_*.txt`: muestra legible de los primeros 10 valores.
- `*_histograma.png`, `*_chi_cuadrado.png`, `*_kolmogorov_smirnov.png`: gráficas.

### Acceso a la aplicación

No hay una URL ni un servidor web. La interacción se realiza por **consola** y los resultados se consultan en los archivos generados.

---

## 6. Estructura del proyecto

```text
practica6/
├── Python/
│   ├── main.py
│   ├── lcg.py
│   ├── statistics_utils.py
│   ├── chi_square.py
│   ├── kolmogorov_smirnov.py
│   ├── plots.py
│   ├── comparacion_resultados.py
│   ├── tests_validacion.py
│   ├── requirements.txt
│   └── resultados/
│       ├── datos/
│       │   ├── muestra_python.txt
│       │   ├── python_chi_cuadrado.csv
│       │   ├── python_resultados.json
│       │   └── python_secuencia_10000.csv
│       └── graficas/
│           ├── python_chi_cuadrado.png
│           ├── python_histograma.png
│           └── python_kolmogorov_smirnov.png
├── Java/
│   ├── src/ape006/
│   │   ├── Main.java
│   │   ├── Lcg.java
│   │   ├── StatisticalFunctions.java
│   │   ├── ChiSquareTest.java
│   │   ├── KolmogorovSmirnovTest.java
│   │   ├── ExportUtils.java
│   │   ├── Plots.java
│   │   ├── ResultsComparator.java
│   │   └── ValidationTests.java
│   ├── out/                     # clases compiladas (generado, ignorado por git)
│   └── resultados/
│       ├── datos/
│       │   ├── java_chi_cuadrado.csv
│       │   ├── java_resultados.json
│       │   ├── java_secuencia_10000.csv
│       │   └── muestra_java.txt
│       └── graficas/
│           ├── java_chi_cuadrado.png
│           ├── java_histograma.png
│           └── java_kolmogorov_smirnov.png
├── .gitignore
└── README.md
```

### Responsabilidad de cada componente

| Archivo / carpeta | Responsabilidad |
|---|---|
| `Python/main.py` | Punto de entrada, menú interactivo, argumentos CLI y orquestación de resultados |
| `Python/lcg.py` | Generador congruencial lineal reproducible |
| `Python/statistics_utils.py` | Gamma incompleta regularizada y valor p de Kolmogorov-Smirnov |
| `Python/chi_square.py` | Prueba Chi-cuadrado, informe y filas exportables |
| `Python/kolmogorov_smirnov.py` | Prueba KS y puntos de la ECDF |
| `Python/plots.py` | Histograma y gráficas de ambas pruebas con Matplotlib |
| `Python/comparacion_resultados.py` | Ejecuta Python y Java, y compara sus resultados |
| `Python/tests_validacion.py` | Pruebas controladas con `unittest` |
| `Python/requirements.txt` | Dependencias de Python |
| `Python/resultados/` | Salidas generadas por la implementación Python |
| `Java/src/ape006/Main.java` | Punto de entrada, menú, argumentos CLI y orquestación |
| `Java/src/ape006/Lcg.java` | Generador congruencial lineal en Java |
| `Java/src/ape006/StatisticalFunctions.java` | Gamma incompleta y valor p de KS |
| `Java/src/ape006/ChiSquareTest.java` | Prueba Chi-cuadrado y su informe |
| `Java/src/ape006/KolmogorovSmirnovTest.java` | Prueba KS y su informe |
| `Java/src/ape006/ExportUtils.java` | Exportación CSV/JSON, SHA-256 y utilidades |
| `Java/src/ape006/Plots.java` | Gráficas PNG con Java2D, sin dependencias externas |
| `Java/src/ape006/ResultsComparator.java` | Compara los JSON de Python y Java |
| `Java/src/ape006/ValidationTests.java` | Pruebas controladas de la implementación Java |
| `Java/out/` | Clases compiladas; se genera y no se versiona |
| `Java/resultados/` | Salidas generadas por la implementación Java |

---

## 7. Información adicional

### Metodología

#### Generador congruencial lineal

```text
X(n+1) = (a * X(n) + c) mod m
U(n+1) = X(n+1) / m
```

Con `a ≡ 1 (mod 4)` y `c` impar, el LCG tiene período completo `2^32` para el estado de 32 bits. En Java se usa `long` y la operación `% 2^32` para evitar desbordamientos. La normalización `X / 4294967296.0` produce los mismos valores `double` que Python.

La secuencia de 10 000 estados tiene el siguiente SHA-256, idéntico en Python y Java:

```text
23f2d027746be27c5723900296c8d6dd058da69f6fb8ebbf65c1822819dbd696
```

#### Prueba Chi-cuadrado

Hipótesis:

- `H0`: los números siguen una distribución uniforme `U(0,1)`.
- `H1`: los números no siguen una distribución uniforme `U(0,1)`.

Configuración: 10 000 datos, 10 intervalos de amplitud 0.1, frecuencia esperada 1000 por intervalo, grados de libertad `10 - 1 = 9`, `α = 0.05`.

Procedimiento:

1. Asignar cada valor al intervalo `[i/10, (i+1)/10)`; el último intervalo es cerrado por la derecha.
2. Contar las frecuencias observadas `Oi`.
3. Calcular `χ² = Σ ((Oi - Ei)² / Ei)`.
4. Obtener el valor p como la cola superior de la distribución Chi-cuadrado con 9 grados de libertad.
5. Rechazar `H0` si `p < 0.05`.

El valor p se calcula con la función gamma incompleta regularizada `Q(gl/2, χ²/2)`, implementada con serie y fracción continua en Python y Java, sin bibliotecas estadísticas externas.

#### Prueba Kolmogorov-Smirnov

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

Se usa una aproximación asintótica, adecuada para `n = 10 000`. Para `λ` pequeño se evalúa la serie de la CDF para evitar cancelación numérica; para `λ` grande se usa la serie alternante de la cola superior.

### Resultados obtenidos

#### Chi-cuadrado (10 000 datos, 10 intervalos)

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

#### Kolmogorov-Smirnov

- `D+ = 0.0059602059`
- `D- = 0.0054111072`
- `D = 0.0059602059`
- Valor p: `0.8685666387`
- Decisión: **no se rechaza H0** (`p = 0.868567 >= 0.05`).

### Comparación Python vs Java

Según los resultados incluidos en el repositorio, la comparación automática terminó con **todas las verificaciones en OK**:

- Misma secuencia de 10 000 estados (SHA-256 idéntico `23f2d0...b696`).
- Mismos 10 000 estados y valores `U` en los CSV.
- Mismas frecuencias observadas y mismo estadístico `χ² = 14.16`.
- Mismos `D+`, `D-`, `D` y valores p de KS.
- Mismas decisiones estadísticas.

### Gráficas generadas

Python (`Python/resultados/graficas/`):

- [python_histograma.png](Python/resultados/graficas/python_histograma.png): histograma de los 10 000 valores frente a la densidad uniforme.
- [python_chi_cuadrado.png](Python/resultados/graficas/python_chi_cuadrado.png): frecuencias observadas vs esperadas.
- [python_kolmogorov_smirnov.png](Python/resultados/graficas/python_kolmogorov_smirnov.png): ECDF vs `F(x) = x`.

Java (`Java/resultados/graficas/`):

- [java_histograma.png](Java/resultados/graficas/java_histograma.png): histograma de los 10 000 valores frente a la densidad uniforme.
- [java_chi_cuadrado.png](Java/resultados/graficas/java_chi_cuadrado.png): frecuencias observadas vs esperadas.
- [java_kolmogorov_smirnov.png](Java/resultados/graficas/java_kolmogorov_smirnov.png): ECDF vs `F(x) = x`.

### Pruebas y validaciones

- **Python:** `py Python\tests_validacion.py` (basado en `unittest`).
- **Java:** `java -cp Java\out ape006.ValidationTests`.
- **Comparación completa:** `py Python\comparacion_resultados.py`.

Las pruebas verifican el LCG, los límites de los intervalos, los estadísticos de ambas pruebas, los valores críticos conocidos y la tolerancia numérica entre implementaciones.

### Documentación de API y endpoints

El proyecto **no expone una API HTTP ni endpoints**. La interfaz es la línea de comandos y los resultados se comunican mediante archivos CSV, JSON y PNG.

### Limitaciones y supuestos

- Un resultado favorable en Chi-cuadrado o KS **no demuestra aleatoriedad verdadera**; solo indica que no se encontró evidencia suficiente de no uniformidad en la muestra analizada.
- El LCG es determinista. Con los parámetros usados tiene período `2^32`, pero presenta estructura de retículo y correlaciones propias de los generadores lineales.
- Solo se evaluó uniformidad univariada. No se aplicaron pruebas de independencia, rachas, autocorrelación, intervalos, póker o espectro.
- El valor p de KS usa la aproximación asintótica con corrección de Stephens, documentada en el código.

### Guía de contribución

1. Cree una rama a partir de `master`.
2. Realice los cambios manteniendo el mismo comportamiento en Python y Java cuando corresponda.
3. Ejecute las pruebas controladas de ambos lenguajes.
4. Ejecute la comparación automática para verificar equivalencia numérica.
5. Abra un pull request describiendo el cambio y los resultados de las pruebas.

### Licencia

No se encontró un archivo de licencia en el repositorio. **Licencia pendiente de confirmar con el autor.**

### Autor y enlaces

- **Autor:** IsmaelGonz
- **Repositorio:** <https://github.com/IsmaelGonz/Simulacion>
- **Asignatura:** Simulación
- **Unidad:** U2 - Generación de números pseudoaleatorios y generación de variables aleatorias

### Entorno de ejecución registrado

- Windows 11.
- Python 3.14.6, NumPy 2.5.4, pandas 3.1.1, Matplotlib 3.11.2.
- JDK 26.0.1 (Oracle Corporation).
