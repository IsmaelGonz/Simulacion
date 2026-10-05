# APE 1 - Construcción y Simulación Computacional de un Modelo Matemático

## Descripción

Este proyecto corresponde a la **Actividad Práctico-Experimental (APE) Nro. 001** de la asignatura **Simulación**.

La práctica consiste en construir e implementar un modelo matemático para simular el comportamiento de la atmósfera durante diferentes horas del día y determinar la posibilidad de lluvia mediante un índice calculado a partir de la humedad, nubosidad y temperatura.

El modelo utilizado es:

```text
I = 0.5H + 0.3N + 0.2Tf
```

Donde:

* `H` = Humedad normalizada.
* `N` = Nubosidad normalizada.
* `Tf` = Factor de temperatura.
* `I` = Índice de posibilidad de lluvia.

---

## Objetivos

### Objetivo general

Comprender el proceso de construcción de un modelo matemático y analizar su comportamiento mediante Python.

### Objetivos específicos

1. Identificar variables, parámetros y relaciones matemáticas de un sistema.
2. Implementar un modelo matemático en Python.
3. Analizar gráficamente la influencia de los parámetros.

---

##  Modelo matemático

El índice de posibilidad de lluvia se calcula mediante la siguiente ecuación:

```text
I = 0.5H + 0.3N + 0.2Tf
```

### Factor de temperatura

| Temperatura |   Tf |
| ----------- | ---: |
| ≤ 10 °C     | 1.00 |
| 12 °C       | 0.90 |
| 14 °C       | 0.80 |
| 16 °C       | 0.70 |
| 18 °C       | 0.60 |
| 20 °C       | 0.50 |
| 22 °C       | 0.40 |
| 24 °C       | 0.30 |
| 26 °C       | 0.20 |
| ≥ 28 °C     | 0.10 |

### Reglas de clasificación

| Índice I          | Estado           |
| ----------------- | ---------------- |
| `I < 0.40`        | Sin lluvia       |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable  |
| `I ≥ 0.75`        | Lluvia           |

---

## Datos utilizados

Los datos proporcionados en la práctica son:

| Hora  | Humedad (%) | Nubosidad (%) | Temperatura (°C) |
| ----- | ----------: | ------------: | ---------------: |
| 06:00 |          65 |            40 |               14 |
| 08:00 |          70 |            50 |               16 |
| 10:00 |          68 |            45 |               18 |
| 12:00 |          60 |            30 |               22 |
| 14:00 |          75 |            70 |               20 |
| 16:00 |          85 |            85 |               18 |
| 18:00 |          92 |            95 |               16 |
| 20:00 |          88 |            90 |               17 |
| 22:00 |          80 |            75 |               15 |

La humedad y la nubosidad se normalizan dividiendo sus valores porcentuales para 100.

Por ejemplo:

```text
H = 65 / 100 = 0.65
N = 40 / 100 = 0.40
```

---

## Arquitectura del proyecto

El proyecto está organizado en diferentes módulos para separar las responsabilidades:

```text
practica1/
│
├── main.py
│
├── modelo/
│   └── modelo.py
│
├── vista/
│   └── graficas.py
│
├── graficas/
│   ├── grafica_indices.png
│   └── grafica_variables.png
│
├── venv/
├── venv_linux/
│
├── requirements.txt
└── README.md
```

### `main.py`

Es el punto de entrada del programa. Se encarga de ejecutar el modelo y utilizar las funciones necesarias para generar los resultados y las gráficas.

### `modelo/modelo.py`

Contiene la lógica principal del modelo matemático, incluyendo:

* Datos de entrada.
* Normalización de variables.
* Factor de temperatura.
* Cálculo del índice `I`.
* Clasificación de la posibilidad de lluvia.

### `vista/graficas.py`

Contiene las funciones encargadas de generar las representaciones gráficas de los resultados obtenidos.

### `graficas/`

Almacena las gráficas generadas por el programa.

---

## Tecnologías utilizadas

* **Python 3**
* **NumPy**
* **Matplotlib**

La guía de la práctica también indica el uso de Java como parte de las herramientas solicitadas.

---

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Ingresar a la carpeta del proyecto:

```bash
cd practica1
```

Crear un entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

En Linux:

```bash
source venv_linux/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución

Para ejecutar el programa:

```bash
python main.py
```

El programa procesa los datos definidos, calcula el índice de posibilidad de lluvia y genera las gráficas correspondientes.

---

##  Resultados

El programa permite obtener el índice de posibilidad de lluvia para cada una de las horas analizadas.

Las gráficas generadas permiten observar el comportamiento de:

* Humedad.
* Nubosidad.
* Temperatura.
* Índice de posibilidad de lluvia.

Los resultados gráficos se almacenan en la carpeta:

```text
graficas/
```

### Gráfica de índices

![Gráfica de índices](graficas/grafica_indices.png)

### Gráfica de variables

![Gráfica de variables](graficas/grafica_variables.png)

---

##  Ejemplo de cálculo

Para los siguientes valores:

```text
Humedad = 90 %
Nubosidad = 80 %
Temperatura = 18 °C
```

Se normalizan los valores:

```text
H = 0.90
N = 0.80
Tf = 0.60
```

Aplicando el modelo:

```text
I = 0.5(0.90) + 0.3(0.80) + 0.2(0.60)
```

Resultado:

```text
I = 0.81
```

Por lo tanto:

```text
I ≥ 0.75
```

El modelo determina:

```text
Lluvia
```

---

##  Preguntas de control

### 1. ¿Qué es un modelo matemático?

Es una representación de un fenómeno o sistema mediante variables y relaciones matemáticas que permiten analizar su comportamiento.

### 2. ¿Cuál es la diferencia entre variable y parámetro?

Una **variable** puede cambiar durante el análisis, mientras que un **parámetro** es un valor que define o controla las características del modelo.

### 3. ¿Qué representa P₀?

Representa el valor inicial utilizado por el modelo exponencial.

### 4. ¿Qué ocurre cuando r < 0?

Cuando `r < 0`, el modelo exponencial representa un comportamiento decreciente.

### 5. ¿Qué limitaciones tiene el modelo exponencial?

El modelo exponencial simplifica el comportamiento de un fenómeno y puede no representar correctamente situaciones donde existen límites, cambios bruscos o factores adicionales que influyen en el sistema.

---

##  Bibliografía

* Diapositivas de la Semana 1 de la asignatura Simulación.
* Guía de Actividades Práctico-Experimentales Nro. 001.

---

##  Autor

**Estudiante:** Ismael González
**Carrera:** Computación
**Asignatura:** Simulación
**Práctica:** APE Nro. 001
**Fecha:** Octubre de 2026
