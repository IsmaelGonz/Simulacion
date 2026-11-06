# Práctica 1 — Modelo matemático de posibilidad de lluvia

## 1. Descripción del proyecto

Este proyecto corresponde a la primera Actividad Práctico-Experimental (APE) de la asignatura Simulación. Su objetivo es construir un modelo matemático que permita analizar las condiciones atmosféricas durante diferentes horas del día y estimar la posibilidad de lluvia a partir de la humedad, la nubosidad y la temperatura.

El programa utiliza Python para procesar los datos, calcular un índice de posibilidad de lluvia y clasificar los resultados en cuatro categorías: sin lluvia, baja posibilidad, lluvia probable y lluvia.

El modelo matemático empleado es:

\[
I = 0.5H + 0.3N + 0.2Tf
\]

Donde:

- **H:** humedad normalizada entre 0 y 1.
- **N:** nubosidad normalizada entre 0 y 1.
- **Tf:** factor de temperatura.
- **I:** índice de posibilidad de lluvia.

La humedad y la nubosidad se normalizan dividiendo sus valores porcentuales para 100. El factor de temperatura se obtiene mediante una tabla de valores y, cuando es necesario, interpolación lineal.

### Objetivos

- Implementar un modelo matemático utilizando Python.
- Identificar las variables que influyen en la posibilidad de lluvia.
- Calcular y clasificar el índice obtenido en diferentes horas del día.
- Representar gráficamente el comportamiento de las variables y los resultados.

## 2. Tecnologías utilizadas

| Tecnología o herramienta | Uso |
| --- | --- |
| Python 3 | Lenguaje de programación principal. |
| NumPy | Manejo de arreglos y operaciones numéricas. |
| Matplotlib | Elaboración de gráficas. |
| Visual Studio Code u otro editor | Edición y ejecución del código. |
| Git | Control de versiones, si se utiliza. |

## 3. Instalación

### Requisitos previos

- Tener Python 3 instalado.
- Disponer de una terminal o un editor de código.
- Contar con conexión a internet para instalar las dependencias.

### Preparación del entorno

Ingresar a la carpeta de la práctica:

```bash
cd practica1
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows:

```bash
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar las bibliotecas necesarias:

```bash
python -m pip install numpy matplotlib
```

**Nota:** La carpeta de esta práctica no incluye un archivo `requirements.txt`, por lo que las dependencias se instalan directamente mediante el comando anterior.

## 4. Uso y ejecución

Una vez instaladas las dependencias, ejecutar el programa desde la carpeta `practica1`:

```bash
python main.py
```

El programa realiza las siguientes operaciones:

1. Carga los datos de humedad, nubosidad, temperatura y hora.
2. Normaliza la humedad y la nubosidad.
3. Calcula el factor correspondiente a cada temperatura.
4. Aplica la fórmula del índice de posibilidad de lluvia.
5. Clasifica el resultado obtenido para cada hora.
6. Muestra una tabla de resultados en la terminal.
7. Genera las gráficas de las variables y del índice calculado.

### Clasificación del índice

| Valor del índice | Interpretación |
| --- | --- |
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

## 5. Estructura del proyecto

```text
practica1/
├── main.py
├── modelo/
│   └── modelo.py
├── vista/
│   └── graficas.py
├── graficas/
│   ├── 1_variables_original.png
│   └── 2_indice_original.png
├── documento/
├── README.md
└── .venv/
```

### Descripción de los archivos

- **`main.py`:** punto de entrada del programa. Ejecuta el modelo, presenta los resultados y solicita la generación de las gráficas.
- **`modelo/modelo.py`:** contiene los datos de entrada, la normalización de variables, el cálculo del factor de temperatura, la fórmula del índice y las reglas de clasificación.
- **`vista/graficas.py`:** contiene las funciones encargadas de representar gráficamente las variables y el índice de posibilidad de lluvia.
- **`graficas/`:** almacena las imágenes generadas durante la ejecución.
- **`documento/`:** carpeta destinada a los documentos de la práctica.
- **`README.md`:** proporciona las instrucciones y la documentación del proyecto.

## 6. Resultados y funcionalidades

El programa permite observar cómo cambian las variables atmosféricas durante las horas analizadas y cómo influyen en el índice calculado.

Se generan dos gráficas principales:

- **Gráfica de variables:** muestra la evolución de la humedad normalizada, la nubosidad normalizada y el factor de temperatura.
- **Gráfica del índice:** presenta el índice de posibilidad de lluvia y los límites utilizados para clasificarlo.

Las gráficas se guardan en la carpeta `graficas/` con los nombres `1_variables_original.png` y `2_indice_original.png`.

Los resultados dependen de los datos de entrada y de las reglas definidas en el modelo. El índice es una estimación académica y no sustituye un pronóstico meteorológico oficial.

## 7. Información adicional

### Consideraciones

- Los datos de entrada están definidos en el archivo `modelo/modelo.py`.
- Para analizar otras condiciones atmosféricas, se pueden modificar los valores de humedad, nubosidad, temperatura y hora.
- Los resultados gráficos se actualizan al ejecutar nuevamente el programa.
- La carpeta `.venv/` corresponde al entorno virtual local y no es necesaria para distribuir el código fuente.

### Posibles mejoras

- Permitir el ingreso de datos mediante archivos CSV.
- Incorporar validaciones para los datos de entrada.
- Comparar los resultados con información meteorológica real.
- Mejorar la presentación de las gráficas y los reportes.

### Autoría

**Asignatura:** Simulación  
**Práctica:** APE 1 — Modelo matemático de posibilidad de lluvia

