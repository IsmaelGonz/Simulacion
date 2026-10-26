# Práctica 2 — Simulación de modelos de crecimiento poblacional

## 1. Descripción del proyecto

Esta práctica consiste en implementar y comparar diferentes modelos matemáticos de crecimiento poblacional mediante Python. El programa permite analizar cómo evoluciona una población a lo largo del tiempo utilizando cuatro enfoques: determinístico, discreto, estocástico y continuo mediante el método numérico de Euler.

La simulación utiliza una población inicial de 1000 individuos y una tasa de crecimiento de 0.05. El modelo estocástico incorpora variaciones aleatorias para representar situaciones en las que el crecimiento no es completamente predecible.

### Objetivos

- Comprender el comportamiento de distintos modelos de crecimiento poblacional.
- Implementar modelos matemáticos y métodos numéricos en Python.
- Analizar la influencia de la aleatoriedad en el crecimiento.
- Comparar gráficamente los resultados obtenidos mediante los cuatro enfoques.

### Modelos matemáticos

**Modelo determinístico:**

\[
P(t)=P_0e^{rt}
\]

Representa el crecimiento exponencial de la población.

**Modelo discreto:**

\[
P_{t+1}=P_t+rP_t
\]

Calcula el crecimiento mediante incrementos sucesivos en períodos definidos.

**Modelo estocástico:**

\[
P_{t+1}=P_t+rP_t+\varepsilon_t
\]

Incluye un término aleatorio que representa las variaciones del crecimiento.

**Modelo continuo mediante Euler:**

\[
P_{t+\Delta t}=P_t+\Delta t(rP_t)
\]

Aproxima numéricamente la evolución del modelo continuo utilizando pasos de tiempo.

Donde \(P_0\) es la población inicial, \(r\) es la tasa de crecimiento, \(t\) representa el tiempo y \(\varepsilon_t\) es una perturbación aleatoria.

## 2. Tecnologías utilizadas

| Tecnología o herramienta | Uso |
| --- | --- |
| Python 3 | Implementación de los modelos. |
| NumPy | Cálculos numéricos, arreglos y generación de valores aleatorios. |
| Matplotlib | Representación gráfica y comparación de resultados. |
| SciPy | Biblioteca científica incluida en las dependencias del entorno. |
| Pandas | Herramientas para el manejo de datos, disponible como dependencia. |
| Visual Studio Code u otro editor | Edición y ejecución del código. |
| Git | Control de versiones, si se utiliza. |

Las bibliotecas NumPy y Matplotlib son las principales para el cálculo y la visualización de los modelos implementados.

## 3. Instalación

### Requisitos previos

- Python 3 instalado.
- Terminal o editor de código.
- Acceso a internet para instalar las dependencias.

Ingresar a la carpeta de la práctica:

```bash
cd practica2
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

Instalar las dependencias definidas en el proyecto:

```bash
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las versiones especificadas de las bibliotecas utilizadas en el entorno de la práctica.

## 4. Uso y ejecución

Ejecutar el programa desde la carpeta `practica2`:

```bash
python main.py
```

Durante la ejecución, el programa:

1. Muestra los parámetros de la simulación.
2. Ejecuta el modelo determinístico.
3. Ejecuta el modelo discreto.
4. Ejecuta el modelo estocástico.
5. Ejecuta el modelo continuo mediante Euler.
6. Genera una gráfica comparativa con las cuatro curvas.

La gráfica se presenta mediante Matplotlib. Para conservarla, se puede guardar desde la ventana de la gráfica; el programa actual no define una ruta automática para guardar esta comparación.

### Parámetros utilizados

| Parámetro | Valor | Descripción |
| --- | ---: | --- |
| Población inicial (P0) | 1000 | Valor inicial de la población. |
| Tasa de crecimiento (R) | 0.05 | Tasa de crecimiento utilizada en los modelos. |
| Variabilidad (SIGMA) | 20 | Desviación estándar del componente aleatorio. |
| Tiempo total (TIEMPO) | 6 | Número de períodos analizados. |
| Paso de Euler (DT) | 1 | Tamaño del paso del método numérico. |

Los valores se encuentran definidos en `config/parametros.py`.

## 5. Estructura del proyecto

```text
practica2/
├── main.py
├── config/
│   ├── __init__.py
│   └── parametros.py
├── modelos/
│   ├── __init__.py
│   ├── deterministico.py
│   ├── discreto.py
│   ├── estocastico.py
│   └── continuo.py
├── graficos/
│   ├── __init__.py
│   └── graficador.py
├── resultados/
│   └── .gitkeep
├── documento/
├── requirements.txt
└── README.md
```

### Descripción de los componentes

- **`main.py`:** coordina la ejecución de los modelos y la presentación de los parámetros.
- **`config/parametros.py`:** centraliza los datos iniciales, la tasa de crecimiento, la variabilidad, el tiempo total y el paso de Euler.
- **`modelos/deterministico.py`:** implementa el crecimiento exponencial.
- **`modelos/discreto.py`:** calcula el crecimiento por períodos sucesivos.
- **`modelos/estocastico.py`:** incorpora variaciones aleatorias al crecimiento.
- **`modelos/continuo.py`:** aproxima el modelo continuo mediante Euler.
- **`graficos/graficador.py`:** genera la gráfica comparativa de los cuatro modelos.
- **`resultados/`:** carpeta destinada a los resultados que se incorporen al proyecto.
- **`documento/`:** contiene la documentación de la práctica.
- **`requirements.txt`:** especifica las dependencias del entorno.

## 6. Resultados y funcionalidades

La principal salida del programa es una gráfica que permite comparar el crecimiento de la población en función del tiempo.

Cada curva representa un modelo distinto:

- El modelo determinístico presenta una evolución exponencial.
- El modelo discreto calcula el crecimiento mediante incrementos sucesivos.
- El modelo estocástico presenta variaciones debido a la incorporación de ruido aleatorio.
- El modelo continuo mediante Euler aproxima el comportamiento del crecimiento utilizando un paso numérico.

La comparación permite reconocer similitudes y diferencias entre los enfoques y comprender cómo la elección del modelo influye en los resultados.

El modelo estocástico puede producir resultados diferentes entre ejecuciones porque no se fija una semilla aleatoria en su implementación actual.

## 7. Información adicional

### Configuración

Para modificar las condiciones de la simulación, se pueden cambiar los valores de `P0`, `R`, `SIGMA`, `TIEMPO` y `DT` en `config/parametros.py`.

Es recomendable mantener un paso de Euler adecuado para el intervalo analizado y comprobar que los parámetros utilizados sean coherentes con el escenario que se desea estudiar.

### Posibles mejoras

- Incorporar una semilla aleatoria configurable para reproducir los resultados estocásticos.
- Guardar automáticamente las gráficas y los datos en archivos CSV.
- Añadir métricas que permitan comparar las diferencias entre modelos.
- Permitir la modificación de parámetros desde la terminal o una interfaz gráfica.

### Autoría

**Asignatura:** Simulación  
**Práctica:** APE 2 — Modelos de crecimiento poblacional

