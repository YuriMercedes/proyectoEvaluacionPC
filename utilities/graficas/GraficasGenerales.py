import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import customtkinter
import ClasificadorResultados
from utilities.vistas import ResultadoVista

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot  as plt

# El archivo Graficas Generales contiene las funciones de las graficas de pila de cada resultado
# Adiccionalmente esta los eventos de los botones Seleccionar de los Tab de cada resultado


# Eventos de de los botones Seleccionar de las rubricas
def buttonEvent_SeleccionarConfig():
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    ruta = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    
    showinfo(
        title='Selected File',
        message= ruta
    )
    
    return ruta

# Eventos de de los botones Seleccionar de Prueba Inicial y Final
def buttonEvent_Seleccionar(ResultadoAprendizaje, tipo):

    ## Seleccionar File
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    ruta = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    
    if tipo == "inicial": ResultadoAprendizaje.setRutaInicial(ruta)
    else: ResultadoAprendizaje.setRutaFinal(ruta)
    
    showinfo(
        title='Selected File',
        message= ResultadoAprendizaje.getRutaInicial() if tipo == "inicial" else ResultadoAprendizaje.getRutaFinal()
    )

    return ResultadoAprendizaje

# Sirve para exportar en excel los resultados generados
def download(data1, data2):
    data1.exportarTabla(data1.getNombre()+" Inicial");
    data2.exportarTabla(data2.getNombre()+" Final");
    showinfo(
        title='Descarga'+data1.getNombre(),
        message='Se han generado los archivos en el escritorio'
    )

def modificar_ruta_descarga(data1, data2, nueva_ruta):
    data1.modificar_ruta_descarga(nueva_ruta)
    data2.modificar_ruta_descarga(nueva_ruta)
    showinfo(
        title='La ruta ha sido actualizada',
        message='Nueva ruta: ' + nueva_ruta
    )

def bar_label_center(plt_bar, data, bottom=None):

    if bottom is None:
        bottom = np.zeros_like(data)

    for bar, value, b in zip(plt_bar, data, bottom):
        if value != 0:  # Solo agregar etiqueta si el valor no es cero
            y_position = b + value / 2
            plt.text(bar.get_x() + bar.get_width() / 2, y_position,
                     f'{value}', ha='center', va='center')

# Funciones "graficar_stackbar" sirve para grafica el stackbar de los criterios especificos y generales
def graficar_stackbar(data1, data2, select):

    if select == "Criterio Eva. 1":
        busquedaCriterio = "CE1"
    elif select == "Criterio Eva. 2":
        busquedaCriterio = "CE2"
    elif select == "Criterio Eva. 3":
        busquedaCriterio = "CE3"
    elif select == "Criterio Eva. 4":
        busquedaCriterio = "CE4"
    else:
        showinfo(
            title='Error',
            message='Selecciona un criterio'
        )
        return
    
    ## Grafica de barra apilado

    # Se define una nueva grafica
    fig, ax = plt.subplots()

    plt.legend(loc='upper left')
    # se trae el conteo de las calificaciones
    conteoInt = data1.getCualitativoCriterioGeneral(busquedaCriterio)

    #Se crean variables para cada una de las calificiones

    dataB = np.array(conteoInt.iloc[0,:len(conteoInt.columns)-1])
    dataI = np.array(conteoInt.iloc[1,:len(conteoInt.columns)-1])
    dataA = np.array(conteoInt.iloc[2,:len(conteoInt.columns)-1])

    # Se crea la estructura de la grafica; labels y cantidad de barras necesarias
    positions = []
    coordinates = []
    space = 0.8
    temp = 1
    # Se crea el conteo del criterio especifico
    dim_indicado_logro = busquedaCriterio.replace('CE', 'IL')
    for n in range(len(conteoInt.columns)-1):
            # Por cada iteracion se necesita 2 barras con la posicion y coordenadas
            positions.append(dim_indicado_logro+"-"+str(n+1)+" I")
            positions.append(dim_indicado_logro+"-"+str(n+1)+" F")
            
            coordinates.append(n+temp+(space*n)   if n != 0 else n+temp)
            coordinates.append(n+temp+1+(space*n) if n != 0 else n+temp+1)
            temp = 1 + temp 

    # Se crean las coordenadas de cada columna

    coordIni = []
    coordFin = []
    for n in range(int(len(coordinates)/2)):
            coordIni.append(coordinates[n*2])
            coordFin.append(coordinates[n*2+1])

    print("Testing Create Arrays")
    print(" Pos ", positions, len(positions))
    print(" Coo ", coordinates)
    print(" CooI ", coordIni)
    print(" CooF ", coordFin)

    # Limite maximo en el eje Y necesario para la visualizacion de los legends
    limMaxY = conteoInt[busquedaCriterio].sum()+12
    
    plt.ylim(0,limMaxY)
    plt.xlim(coordIni[0]-2,coordFin[len(coordFin)-1]+2)
    
    # Barra Inicial
    B = plt.bar(coordIni,dataB,label="Básico", width= 1, edgecolor = 'black')
    bar_label_center(B, dataB)
    # plt.bar_label(B, label_type='center')
    I = plt.bar(coordIni,dataI,bottom=dataB,label="Intermedio",width=1, edgecolor = 'black')
    bar_label_center(I, dataI, bottom=dataB)
    # plt.bar_label(I, label_type='center')
    A = plt.bar(coordIni,dataA,bottom=dataI + dataB,label="Avanzado",width=1, edgecolor = 'black')
    bar_label_center(A, dataA, bottom=dataI + dataB)
    # plt.bar_label(A, label_type='center')

    
    conteoInt2 = data2.getCualitativoCriterioGeneral(busquedaCriterio)
    
    dataB = np.array(conteoInt2.iloc[0,:len(conteoInt2.columns)-1])
    dataI = np.array(conteoInt2.iloc[1,:len(conteoInt2.columns)-1])
    dataA = np.array(conteoInt2.iloc[2,:len(conteoInt2.columns)-1])


    # Bar Final
    B = plt.bar(coordFin,dataB,width=1, color='tab:blue', 
                edgecolor = 'black')
    bar_label_center(B, dataB)
    # plt.bar_label(B, label_type='center')
    I = plt.bar(coordFin,dataI,bottom=np.array(dataB),width=1, color='tab:orange',
            edgecolor = 'black')
    bar_label_center(I, dataI, bottom=dataB)
    # plt.bar_label(I, label_type='center')
    A = plt.bar(coordFin,dataA,bottom=np.array(dataI)+np.array(dataB),width=1, color='tab:green', 
                edgecolor = 'black')
    bar_label_center(A, dataA, bottom=dataI + dataB)
    # plt.bar_label(A, label_type='center')


    plt.xticks(coordinates,labels=positions)
    #for tick in ax.get_xticklabels():
        #tick.set_rotation(90)
    

    plt.legend(loc="upper left")
    plt.title("Comparación Cualitativa Inicial y Final Criterio "+busquedaCriterio)

    plt.show()

def graficar_stackbar_criterios(data1, data2):
    ## Grafica de barra apilado

    # Se define una nueva grafica
    fig, ax = plt.subplots()
    plt.legend(loc='upper left')
    #plt.figure()

    # se trae el conteo de las calificaciones
    conteoInt = data1.getCualitativoCriterios()

    #Se crean variables para cada una de las calificiones
    print(conteoInt.iloc[0])
    dataB = np.array(conteoInt.iloc[0])
    dataI = np.array(conteoInt.iloc[1])
    dataA = np.array(conteoInt.iloc[2])

    # Se crea la estructura de la grafica; labels y cantidad de barras necesarias
    positions = []
    coordinates = []
    space = 0.5
    temp = 1
    # Se crea el conteo del criterio especifico
    for n in range(len(conteoInt.columns)):
            # Por cada iteracion se necesita 2 barras con la posicion y coordenadas
            positions.append("CE"+str(n+1)+" I")
            positions.append("CE"+str(n+1)+" F")
            
            coordinates.append(n+temp+(space*n)   if n != 0 else n+temp)
            coordinates.append(n+temp+1+(space*n) if n != 0 else n+temp+1)
            temp = 1 + temp 
    # Se crean las coordenadas de cada columna

    coordIni = []
    coordFin = []
    for n in range(int(len(coordinates)/2)):
            coordIni.append(coordinates[n*2])
            coordFin.append(coordinates[n*2+1])

    print("Testing Creating Arrays")
    print(" Pos ", positions)
    print(" Coo ", coordinates)
    print(" CooI ", coordIni)
    print(" CooF ", coordFin)

    # Limite maximo en el eje Y necesario para la visualizacion de los legends
    limMaxY = conteoInt["CE1"].sum()+12

    plt.ylim(0,limMaxY)

    # Barra Inicial
    B = plt.bar(coordIni, dataB, label="Básico", width=1.0, edgecolor='black')
    bar_label_center(B, dataB)

    I = plt.bar(coordIni, dataI, bottom=dataB, label="Intermedio", width=1.0, edgecolor='black')
    bar_label_center(I, dataI, bottom=dataB)

    A = plt.bar(coordIni, dataA, bottom=dataI + dataB, label="Avanzado", width=1.0, edgecolor='black')
    bar_label_center(A, dataA, bottom=dataI + dataB)


    conteoInt2 = data2.getCualitativoCriterios()
    dataB = np.array(conteoInt2.iloc[0])
    dataI = np.array(conteoInt2.iloc[1])
    dataA = np.array(conteoInt2.iloc[2])
    print(conteoInt2)
    print(dataA)
    print(dataI)
    print(dataB)
    # dataB = np.array(1)
    # dataI = np.array(1)
    # dataA = np.array(1)


    # Bar Final
    # Barra conteo basico
    B = plt.bar(coordFin, dataB, width=1.0, color='tab:blue', edgecolor='black')
    bar_label_center(B, dataB)

    # Barra conteo intermedio
    I = plt.bar(coordFin, dataI, bottom=dataB, width=1.0, color='tab:orange', edgecolor='black')
    bar_label_center(I, dataI, bottom=dataB)

    # Barra conteo avanzado
    A = plt.bar(coordFin, dataA, bottom=dataI + dataB, width=1.0, color='tab:green',
                edgecolor='black')
    bar_label_center(A, dataA, bottom=dataI + dataB)


    plt.xticks(coordinates,labels=positions)


    plt.legend(loc="upper left")
    plt.title("Comparación por Criterios prueba Inicial y Final")

    plt.show()
    