# APE N.º 007 — Estimación de resultados mediante el método de Monte Carlo

[![Python](https://img.shields.io/badge/Python-3.14.6-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-26.0.1-ED8B00?logo=openjdk&logoColor=white)](https://www.oracle.com/java/)
[![NumPy](https://img.shields.io/badge/NumPy-2.5.4-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-3.1.1-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-11557C?logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Asignatura](https://img.shields.io/badge/Simulaci%C3%B3n-U2-blue)](https://github.com/IsmaelGonz/Simulacion)

**Asignatura:** Simulación  
**Unidad / tema:** Semana 6 — Estimación de resultados mediante el método de Monte Carlo  
**Estudiante:** Ismael González  
**Fecha de ejecución:** 12 de noviembre de 2026  
**Entorno probado:** Windows 11, Python 3.14.6, Java 26.0.1

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

**Nombre del proyecto:** APE N.º 007 — Estimación de resultados mediante el método de Monte Carlo.

**Descripción general:**  
Este proyecto implementa, de forma independiente en **Python** y **Java**, un experimento de estimación del valor de π utilizando el método de Monte Carlo. Se generan puntos pseudoaleatorios `(x, y)` distribuidos uniformemente en el cuadrado unitario `[0, 1) × [0, 1)` y se cuentan los que cumplen la condición `x² + y² ≤ 1` (puntos dentro del cuarto de círculo unitario, denotados `Nc`). A partir de la proporción `Nc / N` se aproxima π mediante la fórmula:

```text
π ≈ 4 × (Nc / N)
```

**Propósito principal:**  
Demostrar la aplicación del método Monte Carlo para estimar resultados numéricos, analizar la influencia del tamaño de muestra sobre el error absoluto y comparar el comportamiento de dos implementaciones independientes en Python y Java bajo condiciones experimentales equivalentes.

**Objetivos principales:**

1. Implementar un experimento de estimación de π mediante Monte Carlo en Python y en Java.
2. Analizar la influencia del tamaño de muestra sobre el error absoluto de la estimación.
3. Comparar los resultados y los tiempos de ejecución obtenidos en Python y Java, garantizando condiciones experimentales equivalentes.

**Funcionalidades más importantes:**

- Generación de números pseudoaleatorios con el generador **SplitMix64** (semilla fija `12345`), idéntico en ambos lenguajes.
- Ejecución de cuatro experimentos con tamaños de muestra: `1 000`, `10 000`, `100 000` y `1 000 000` puntos.
- Cálculo de π estimado, error absoluto `|π real − π̂|` y tiempo de ejecución del núcleo del algoritmo.
- Medición de tiempos con `time.perf_counter_ns()` en Python y `System.nanoTime()` en Java.
- Exportación de resultados a archivos CSV y generación de gráficos con Matplotlib.
- Verificación de reproducibilidad mediante SHA-256 sobre los valores IEEE 754 de la secuencia generada.

---

## 2. Tecnologías utilizadas

| Categoría | Tecnología | Versión probada | Uso en el proyecto |
|---|---|---:|---|
| Lenguaje | Python | 3.14.6 | Implementación principal, procesamiento de datos y generación de gráficos |
| Lenguaje | Java | 26.0.1 | Segunda implementación independiente con la biblioteca estándar |
| Biblioteca | NumPy | 2.5.4 | Procesamiento numérico y apoyo en la comparación de resultados |
| Biblioteca | pandas | 3.1.1 | Organización de resultados y exportación a CSV |
| Biblioteca | Matplotlib | 3.11.2 | Generación de gráficos PNG (estimación, error, tiempos y puntos) |
| Biblioteca estándar Java | `System.nanoTime()` | — | Medición de tiempos de ejecución en Java |
| Biblioteca estándar Java | `MessageDigest`, `ByteBuffer` | — | Verificación SHA-256 de la secuencia pseudoaleatoria |
| Formato de datos | CSV | — | Resultados detallados, tabla combinada y verificación |
| Formato de imagen | PNG | — | Gráficos de resultados |
| Sistema operativo | Windows 11 | 10.0.26300 | Entorno de ejecución registrado |

**Notas técnicas:**

- No se utilizan bases de datos, servicios externos, llamadas de red ni bibliotecas estadísticas externas.
- El generador SplitMix64 y el experimento Monte Carlo están implementados directamente en ambos lenguajes.
- Las versiones indicadas corresponden al entorno donde se ejecutaron y verificaron los experimentos.

---

## 3. Instalación

### Requisitos previos

| Herramienta | Versión necesaria | Notas |
|---|---:|---|
| Python | 3.14 o superior | Con `pip` incluido |
| NumPy | 2.0 o superior | Declarado en `python/requirements.txt` |
| pandas | 2.0 o superior | Declarado en `python/requirements.txt` |
| Matplotlib | 3.8 o superior | Declarado en `python/requirements.txt` |
| JDK | 26 o superior | Con `javac` y `java` disponibles en el `PATH` |
| Git | No especificada | Solo necesaria para clonar el repositorio |

### 1. Clonar el repositorio

Desde la raíz del repositorio `Simulacion/`:

```bash
cd practica7
```

Todos los comandos de esta documentación deben ejecutarse desde la carpeta `practica7/`.

### 2. Instalar dependencias de Python

**Windows (PowerShell):**

```powershell
py -m pip install -r python\requirements.txt
```

**Linux / macOS:**

```bash
python3 -m pip install -r python/requirements.txt
```

Si se crea un entorno virtual, activarlo antes de instalar:

**Windows:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> En Windows, si el comando `python` apunta al alias de Microsoft Store, utilice el lanzador `py`.

### 3. Compilar Java (opcional, solo para la implementación Java)

Hay que compilar todas las subcarpetas del paquete `ape007/`.

**Windows PowerShell:**

```powershell
$fuentes = Get-ChildItem java\src\ape007 -Recurse -Filter *.java | ForEach-Object { $_.FullName }
javac -encoding UTF-8 -d java\out $fuentes
```

**Linux / macOS:**

```bash
javac -encoding UTF-8 -d java/out $(find java/src/ape007 -name '*.java')
```

La carpeta `java/out/` se genera automáticamente y no es necesario versionarla (está excluida mediante `.gitignore`).

---

## 4. Configuración del proyecto

El proyecto **no utiliza variables de entorno** ni archivos `.env`. Tampoco requiere credenciales, tokens ni claves de API. Todos los parámetros están definidos en el código fuente.

### Parámetros del experimento

| Parámetro | Valor | Dónde se define |
|---|---:|---|
| Semilla SplitMix64 | `12345` | `python/model/splitmix64.py` y `java/src/ape007/model/SplitMix64.java` |
| Constante gamma | `0x9E3779B97F4A7C15` | Mismo archivo del generador en ambos lenguajes |
| Constante mix1 | `0xBF58476D1CE4E5B9` | Mismo archivo del generador en ambos lenguajes |
| Constante mix2 | `0x94D049BB133111EB` | Mismo archivo del generador en ambos lenguajes |
| Tamaños de muestra | `1 000`, `10 000`, `100 000`, `1 000 000` | `python/model/monte_carlo.py` y `java/src/ape007/model/MonteCarlo.java` |
| Repeticiones cronometradas | `3` | `python/model/monte_carlo.py` y `java/src/ape007/model/MonteCarlo.java` |
| Calentamiento global | `2 × 1 000 000` puntos | `python/controller/experiment_controller.py` y `java/src/ape007/controller/ExperimentController.java` |
| Calentamiento por tamaño | `1` repetición | `python/model/monte_carlo.py` y `java/src/ape007/model/MonteCarlo.java` |
| Pares para verificación SHA-256 | `1 000` pares (`2 000` dobles) | `python/model/monte_carlo.py` y `java/src/ape007/model/SplitMix64.java` |

### Parámetros de ejecución

No se exponen mediante variables de entorno. Para modificarlos es necesario editar el archivo fuente correspondiente y recompilar/ejeuctar de nuevo.

### Configuraciones de seguridad

- No se almacenan ni solicitan contraseñas, tokens o claves.
- No se realizan conexiones a servicios externos.
- Los resultados generados no contienen datos personales ni credenciales.

---

## 5. Uso del proyecto

La aplicación se ejecuta desde la **raíz del proyecto** (`practica7/`). No hay interfaz web ni servidor; la interacción es por consola y los resultados se consultan en los archivos generados.

### Python

**Ejecutar los cuatro experimentos:**

```powershell
py python\main.py
```

El programa:

1. Ejecuta un calentamiento global de `2 × 1 000 000` puntos.
2. Ejecuta los cuatro tamaños de muestra.
3. Realiza un calentamiento por tamaño y tres repeticiones cronometradas.
4. Cronometra únicamente el núcleo Monte Carlo (generación de puntos y conteo).
5. Exporta `resultados/resultados_python.csv` y `resultados/verificacion_python.csv`.
6. Muestra en consola `N`, `Nc`, π estimado, error absoluto y tiempo mediano.

**Comparar con Java y generar la tabla combinada y los gráficos:**

```powershell
py python\main.py --comparar
```

Este comando requiere que antes se hayan ejecutado Python y Java, porque lee `resultados/resultados_python.csv` y `resultados/resultados_java.csv`.

### Java

**Compilar y ejecutar:**

```powershell
$fuentes = Get-ChildItem java\src\ape007 -Recurse -Filter *.java | ForEach-Object { $_.FullName }
javac -encoding UTF-8 -d java\out $fuentes
java -cp java\out ape007.Main
```

El programa:

1. Ejecuta un calentamiento global de `2 × 1 000 000` puntos para que la JVM compile el método antes de medir.
2. Ejecuta los cuatro tamaños de muestra.
3. Realiza un calentamiento por tamaño y tres repeticiones cronometradas.
4. Mide con `System.nanoTime()` únicamente el núcleo Monte Carlo.
5. Exporta `resultados/resultados_java.csv` y `resultados/verificacion_java.csv`.
6. Muestra en consola `N`, `Nc`, π estimado, error absoluto y tiempo mediano.

**Comparar con Python y generar la tabla combinada y los gráficos:**

```powershell
py python\main.py --comparar
```

### Flujo completo recomendado

Desde la raíz de `practica7/`:

```powershell
# 1. Ejecutar Python
py python\main.py

# 2. Compilar y ejecutar Java
$fuentes = Get-ChildItem java\src\ape007 -Recurse -Filter *.java | ForEach-Object { $_.FullName }
javac -encoding UTF-8 -d java\out $fuentes
java -cp java\out ape007.Main

# 3. Comparar resultados y generar gráficos
py python\main.py --comparar
```

---

## 6. Estructura del proyecto

```text
practica7/
├── python/
│   ├── main.py
│   ├── requirements.txt
│   ├── model/
│   │   ├── __init__.py
│   │   ├── splitmix64.py
│   │   ├── monte_carlo.py
│   │   └── results_repository.py
│   ├── view/
│   │   ├── __init__.py
│   │   ├── console_view.py
│   │   ├── report_view.py
│   │   └── plots.py
│   └── controller/
│       ├── __init__.py
│       ├── experiment_controller.py
│       └── comparison_controller.py
├── java/
│   └── src/
│       └── ape007/
│           ├── Main.java
│           ├── model/
│           │   ├── ExperimentRow.java
│           │   ├── MonteCarlo.java
│           │   ├── ResultsRepository.java
│           │   └── SplitMix64.java
│           ├── view/
│           │   └── ConsoleView.java
│           └── controller/
│               └── ExperimentController.java
│           └── out/              # clases compiladas (generado, no versionado)
├── resultados/
│   ├── resultados.csv            # tabla comparativa combinada
│   ├── resultados_python.csv     # resultados detallados de Python
│   ├── resultados_java.csv       # resultados detallados de Java
│   ├── verificacion.txt          # informe de reproducibilidad
│   ├── verificacion_python.csv   # primeros pares y hash de Python
│   ├── verificacion_java.csv     # primeros pares y hash de Java
│   ├── estimacion_pi.png
│   ├── error_absoluto.png
│   ├── tiempos_ejecucion.png
│   ├── monte_carlo_puntos_1000.png
│   ├── monte_carlo_puntos_10000.png
│   ├── monte_carlo_puntos_100000.png
│   └── monte_carlo_puntos_1000000.png
├── informe/
│   └── informe.md
├── .gitignore
└── README.md
```

### Responsabilidad de los componentes principales

| Componente | Capa | Responsabilidad |
|---|---|---|
| `python/model/splitmix64.py` | Modelo | Generador SplitMix64, conversión a `double` y verificación SHA-256 |
| `python/model/monte_carlo.py` | Modelo | Experimento Monte Carlo, tamaños de muestra y cálculo de error |
| `python/model/results_repository.py` | Modelo | Lectura y escritura de archivos CSV de resultados y verificación |
| `python/view/console_view.py` | Vista | Presentación de resultados en consola |
| `python/view/report_view.py` | Vista | Informe de texto de verificación de reproducibilidad |
| `python/view/plots.py` | Vista | Gráficos académicos en PNG |
| `python/controller/experiment_controller.py` | Controlador | Orquestación de experimentos, medición de tiempos y exportación |
| `python/controller/comparison_controller.py` | Controlador | Verificación Python vs Java, tabla combinada e informe de reproducibilidad |
| `python/main.py` | Controlador | Punto de entrada y despacho de argumentos |
| `java/src/ape007/model/SplitMix64.java` | Modelo | Generador SplitMix64 y verificación SHA-256 en Java |
| `java/src/ape007/model/MonteCarlo.java` | Modelo | Experimento Monte Carlo y cálculo de error en Java |
| `java/src/ape007/model/ExperimentRow.java` | Modelo | Fila de resultados de un experimento |
| `java/src/ape007/model/ResultsRepository.java` | Modelo | Escritura de archivos CSV de resultados y verificación en Java |
| `java/src/ape007/view/ConsoleView.java` | Vista | Presentación de resultados en consola en Java |
| `java/src/ape007/controller/ExperimentController.java` | Controlador | Orquestación de experimentos y cronometraje en Java |
| `java/src/ape007/Main.java` | Controlador | Punto de entrada Java y resolución de rutas |

### Arquitectura MVC

El proyecto sigue el patrón **Modelo-Vista-Controlador**:

- **Modelo:** lógica de simulación y acceso a datos (`SplitMix64`, `MonteCarlo`, `ExperimentRow`, `ResultsRepository`). No imprime ni grafica.
- **Vista:** presentación de resultados (`ConsoleView`, `console_view`, `report_view`, `plots`). No contiene lógica de negocio.
- **Controlador:** orquestación de experimentos, cronometraje, comparación y despacho (`ExperimentController`, `experiment_controller`, `comparison_controller`, `Main`).

---

## 7. Información adicional

### Resultados experimentales obtenidos

Los tiempos corresponden a la mediana de tres repeticiones cronometradas, después de un calentamiento global y un calentamiento por tamaño. Solo se mide el bucle Monte Carlo; no se incluyen lectura/escritura de archivos, impresión ni gráficos. Las ejecuciones de Python y Java se realizaron de forma consecutiva para reducir diferencias de condiciones. Aun así, los tiempos pueden variar entre corridas por la carga del sistema, la frecuencia del procesador y el entorno de ejecución; por eso se reporta la mediana de tres repeticiones y no un único valor aislado.

| N | Nc | π estimado | Error absoluto | Tiempo Python (ms) | Tiempo Java (ms) | Factor Python/Java |
|---:|---:|---:|---:|---:|---:|---:|
| 1 000 | 798 | 3.1920000000 | 0.0504073464 | 2.1338 | 0.0042 | ≈ 508.0× |
| 10 000 | 7 815 | 3.1260000000 | 0.0155926536 | 27.3360 | 0.0285 | ≈ 959.2× |
| 100 000 | 78 644 | 3.1457600000 | 0.0041673464 | 177.2680 | 0.2905 | ≈ 610.2× |
| 1 000 000 | 786 510 | 3.1460400000 | 0.0044473464 | 1908.5674 | 2.7869 | ≈ 684.8× |

**Valor real de π:** `3.141592653589793`.  
**Mejor aproximación de esta ejecución:** `N = 100 000`, con error absoluto `0.0041673464`.

Los resultados detallados, incluidas las tres repeticiones, los promedios, los mínimos y las desviaciones estándar, están en:

- `resultados/resultados_python.csv`
- `resultados/resultados_java.csv`

La tabla combinada se encuentra en `resultados/resultados.csv`.

### Verificación de reproducibilidad

Se generaron `1 000` pares `(x, y)` con la misma semilla y se calculó SHA-256 sobre los `2 000` valores `double` en formato IEEE 754 little-endian. El resultado fue idéntico en Python y Java:

```text
SHA-256: 05765a7a2b04f628206012cba5e5185f930b28b161aec840806a81beaf261004
```

También se verificó que los primeros 10 pares coinciden bit a bit y que `Nc` y π coinciden en los cuatro experimentos. El informe se guarda en `resultados/verificacion.txt`.

Por tanto, en esta práctica **no se observaron diferencias numéricas** entre Python y Java: las diferencias son únicamente de tiempo de ejecución.

### Visualizaciones generadas

| Gráfico | Archivo | Descripción |
|---|---|---|
| Estimación de π | `resultados/estimacion_pi.png` | Aproximación de π para los cuatro tamaños de muestra y línea del valor real |
| Error absoluto | `resultados/error_absoluto.png` | Error absoluto en escala logarítmica según `N` |
| Tiempos de ejecución | `resultados/tiempos_ejecucion.png` | Comparación de tiempos Python vs Java en escala logarítmica |
| Puntos Monte Carlo (1 000) | `resultados/monte_carlo_puntos_1000.png` | Puntos dentro/fuera del cuarto de círculo para `N = 1 000` |
| Puntos Monte Carlo (10 000) | `resultados/monte_carlo_puntos_10000.png` | Puntos dentro/fuera del cuarto de círculo para `N = 10 000` |
| Puntos Monte Carlo (100 000) | `resultados/monte_carlo_puntos_100000.png` | Puntos dentro/fuera del cuarto de círculo para `N = 100 000` |
| Puntos Monte Carlo (1 000 000) | `resultados/monte_carlo_puntos_1000000.png` | Puntos dentro/fuera del cuarto de círculo para `N = 1 000 000` |

En las gráficas de puntos, los puntos azules cumplen `x² + y² ≤ 1` y se cuentan como `Nc`; los rojos quedan fuera. La frontera verde es el cuarto de círculo unitario.

### Limitaciones

- Los tiempos dependen del hardware, del sistema operativo, de la carga del equipo y de la versión de la JVM o del intérprete. No son valores universales.
- Cada tamaño de muestra se ejecutó con una sola semilla. Para caracterizar la distribución del error sería conveniente repetir el experimento con muchas semillas.
- El experimento es de un solo hilo y no explora paralelización, vectorización ni optimizaciones específicas de hardware.
- La verificación cubre 1 000 pares y los cuatro valores de `Nc`; es una comprobación fuerte de equivalencia para este experimento, pero no constituye una prueba formal de la calidad estadística de todo el período del generador.

### Bibliografía

- Material de clase de la asignatura **Simulación**, semana 6: *Estimación de resultados mediante el método de Monte Carlo*. Diapositivas proporcionadas por la asignatura.
- Guía de práctica **APE N.º 007: Estimación de resultados mediante el método de Monte Carlo**. Material de la asignatura.

---

**Autor:** Ismael González  
**Repositorio:** <https://github.com/IsmaelGonz/Simulacion>  
**Asignatura:** Simulación — APE N.º 007