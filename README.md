# Proyecto de Evaluación de Compentencias

Este proyecto utiliza una interfaz gráfica de usuario (GUI) construida con `tkinter` y `customtkinter` para clasificar y visualizar las competencias. Además, se utilizan bibliotecas como `pandas`, `numpy`, `seaborn`, y `matplotlib` para el análisis y la visualización de datos.

## Pre-requisitos

Antes de ejecutar este proyecto, asegúrate de tener instalado lo siguiente:

1. **Python 3.8 o superior**:  
   El proyecto está desarrollado en Python. Puedes verificar tu versión de Python ejecutando:
   ```bash
   python --version
   ```
   Si no lo tienes instalado, descárgalo desde [python.org](https://www.python.org/).

## Dependencias

Asegúrate de tener instaladas las siguientes bibliotecas de Python antes de ejecutar el proyecto:

- `tkinter` (generalmente incluido en la instalación estándar de Python)
- `customtkinter`
- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
- `xlsxwriter`

Puedes instalar las dependencias necesarias utilizando 'pip':

```bash
pip install customtkinter pandas numpy seaborn matplotlib
```

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `ClasificadorResultados.py`: Módulo principal que contiene la lógica de clasificación de resultados.
- `graficas/GraficasGenerales.py`: Módulo que contiene las clases y funciones relacionadas con las graficas.
- `utilities/ResultadoVista.py`: Módulo que contiene las clases y funciones relacionadas con la interfaz gráfica.
- `main.py`: Punto de entrada del programa que inicializa la GUI y ejecuta la aplicación.

## Cómo Ejecutar el Proyecto

1. Clona este repositorio o descarga los archivos del proyecto.
2. Navega al directorio del proyecto:

   ```bash
   cd ruta/al/proyecto
   ```
3. Instala las dependencias necesarias (si no las tienes ya instaladas):
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el archivo `main.py` para iniciar la aplicación:
   ```bash
   python main.py
   ```
## Cómo Compilar el proyecto

1. ### Instalar pyinstaller
   ```bash
   python -m pip install pyinstaller
   ```
   o
   ```bash
   pip install pyinstaller
   ```
2. ### Ejecutar comando
   ```bash
   pyinstaller --onefile  --distpath ./release --name "Evaluación de competencias" --icon=utilities/academico.ico --hidden-import=xlsxwriter --hidden-import=customtkinter --hidden-import=pandas --hidden-import=numpy --hidden-import=matplotlib main.py
   ```
   ### Errores de creación ejecutable

   Para los errores de compilación de tipo
   
   ```shell
   IndexError: tuple index out of range 
   ```

   Este error se puede corregir agregando la siguiente linea de código en el archivo dis.py en la linea 431
   ubicado `Python\Python310\Lib`
   ```python 431
   extended_arg = 0  
   ```
   
## Autores ✒️

* **Yuri Mercedes Bermudez Mazuera** - *Documentación y Desarrollo de software* - [example](https://github.com/example)
