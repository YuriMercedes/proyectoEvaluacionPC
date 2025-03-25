import os
import sys
import tkinter
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno
from tkinter import simpledialog
from tkinter import filedialog as fd
import customtkinter

from utilities.graficas import GraficasGenerales
import ClasificadorResultados
from utilities.vistas import ResultadoVista
from utilities.objetos import Objetos

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot  as plt

# El archivo ResultadoVista contiene:
# Todos los elementos que se visualizan en el TAB del resultado
# Todos los eventos de los botones del TAB del resultado

# Clase Vista de ser inicializada con los siguientes parametros
# tabViewMain (CTkTabview), NombreResultado (String), check (dict (StringVar)), checkbox (dict (CTkCheckBox)), 
# frameleft(tk.Frame), front(dict (Vista)), cont(dict (Number))

class Vista:

    ResultadoRuta = Objetos.ResultadoAprendizaje()
    CalculoResultadoInicial = None
    CalculoResultadoFinal = None
    
    def getPandasResultadoInicial(self):
        return self.CalculoResultadoInicial
    
    def getPandasResultadoFinal(self):
        return self.CalculoResultadoFinal
    
    def getNombreResultado(self):
        return self.NombreResultado
    
    
    RutaConfigCriterioPregunta = None
    RutaConfigRubricaGeneral = None
    RutaConfigRubricaEspecifica = None
    
    def __init__(self, tabViewMain, nombre, check, checkbox, frameleft, front, cont):
        
        self.tabview = tabViewMain
        self.NombreResultado = nombre
        self.check_var = check
        self.checkbox = checkbox
        self.frame_left = frameleft
        self.ResultadoFront = front
        self.check_cont = cont
        
        self.label_seleccion_csv_i_int = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Prueba inicial - Seleccione un archivo CSV ",
                                              fg_color=("white", "gray38"),
                                              width=350)  # font name and size in px
        
        self.label_seleccion_csv_i_int.grid(row=1, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=2)
        
        self.button_select_file_i_int = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Seleccionar",
                                                    command=self.button_select_int_1)
        self.button_select_file_i_int.grid(row=1, column=2, pady=10, padx=20)
        
        self.label_seleccion_csv_f_int = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Prueba final - Seleccione un archivo CSV ",
                                              fg_color=("white", "gray38"),
                                              width=350)  # font name and size in px
        
        self.label_seleccion_csv_f_int.grid(row=2, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=2)
        
        self.button_select_file_f_int = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Seleccionar",
                                                    command=self.button_select_int_2)
        self.button_select_file_f_int.grid(row=2, column=2, pady=10, padx=20)
        
        self.button_calc_int = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Calcular",
                                                    command=self.calcular_int)
        self.button_calc_int.configure(state="disabled")
        self.button_calc_int.grid(row=3, column=2, pady=10, padx=20)
        
        self.button_download_int = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Descargar",
                                                    command=self.download_int)
        self.button_download_int.configure(state="disabled")
        self.button_download_int.grid(row=4, column=2, pady=10, padx=20)
        
        self.combobox_graficas_int = customtkinter.CTkComboBox(self.tabview.tab(self.NombreResultado),
                                                    values=["Selecciona..","Criterio N"])
        
        self.combobox_graficas_int.grid(row=3, column=1, padx=20, pady=(10,10))
        self.combobox_graficas_int.configure(state="disabled",hover=False)
        
        self.button_grafica_int = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                text="Graficar Indicador de Logro",
                                                command=self.graficar_stackbar_int)
        self.button_grafica_int.grid(row=4, column=1, pady=10, padx=20)
        self.button_grafica_int.configure(state="disabled")
        
        self.label_grafica = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Grafica por Criterios de Evaluación",
                                              width=150)  # font name and size in px
        
        self.label_grafica.grid(row=3, column=0, sticky="nwe", ipadx=5, padx=15, pady=15)
        
        self.button_grafica_int_2 = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                text="Graficar",
                                                command=self.graficar_stackbar_criterios_int)
        self.button_grafica_int_2.grid(row=4, column=0, pady=10, padx=20)
        self.button_grafica_int_2.configure(state="disabled")
        
        
        ## ZONA DE CONFIGURACION RUBRICAS
        
        self.label_configuracion = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Configuración rúbrica de "+self.NombreResultado,
                                              #fg_color=("white", "gray38"),
                                              font=("Roboto",20),
                                              width=350)  # font name and size in px.
        
        self.label_configuracion.grid(row=5, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=3)
        
        # SELECCIONAR CRITERIO PREGUNTA
        
        self.label_seleccion_csv_criterio_pregunta = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Criterio Pregunta - Seleccione un archivo CSV ",
                                              fg_color=("white", "gray38"),
                                              width=350)  # font name and size in px
        
        self.label_seleccion_csv_criterio_pregunta.grid(row=6, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=2)
        
        self.button_select_file_criterio_pregunta = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Seleccionar",
                                                    command=self.button_criterio_pregunta)
        self.button_select_file_criterio_pregunta.grid(row=6, column=2, pady=10, padx=20)
        
        # SELECCIONAR RUBRICA GENERAL
        
        self.label_seleccion_csv_rubrica_general = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Rúbrica General - Seleccione un archivo CSV ",
                                              fg_color=("white", "gray38"),
                                              width=350)  # font name and size in px
        
        self.label_seleccion_csv_rubrica_general.grid(row=7, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=2)
        
        self.button_select_file_rubrica_general = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Seleccionar",
                                                    command=self.button_rubrica_general)
        self.button_select_file_rubrica_general.grid(row=7, column=2, pady=10, padx=20)
        
        
        # SELECCIONAR RUBRICA ESPECIFICA
        
        self.label_seleccion_csv_rubrica_especifica = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Rúbrica Especifica - Seleccione un archivo CSV ",
                                              fg_color=("white", "gray38"),
                                              width=350)  # font name and size in px
        
        self.label_seleccion_csv_rubrica_especifica.grid(row=8, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=2)
        
        self.button_select_file_rubrica_especifica = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Seleccionar",
                                                    command=self.button_rubrica_especifica)
        self.button_select_file_rubrica_especifica.grid(row=8, column=2, pady=10, padx=20)
        
        # GUARDAR Y CARGAR
        
        self.button_save_load_config = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Guardar y Cargar rutas",
                                                    command=self.button_load_config)
        self.button_save_load_config.configure(state="disabled")
        self.button_save_load_config.grid(row=9, column=2, pady=10, padx=20)
        
        # LOAD SYSTEM
        self.button_load_config = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Cargar datos",
                                                    command=self.button_load_file_path)
        #self.button_load_config.configure(state="disabled")
        self.button_load_config.grid(row=9, column=0, pady=10, padx=20)
        
        # Configuracion de resultado
        
        self.label_configuracion = customtkinter.CTkLabel(self.tabview.tab(self.NombreResultado),
                                              text="Configuración Resultado de Aprendizaje "+self.NombreResultado,
                                              #fg_color=("white", "gray38"),
                                              font=("Roboto",20),
                                              width=350)  # font name and size in px.
        self.label_configuracion.grid(row=10, column=0, sticky="nwe", ipadx=5, padx=15, pady=15, columnspan=3)
        
        # BORRAR
        
        self.button_load_config = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Eliminar Resultado",
                                                    command=self.button_eliminar_resultado)
        self.button_load_config.grid(row=11, column=0, pady=10, padx=20)
        
        # Modificar nombre
        
        self.button_load_config = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Modificar nombre Resultado",
                                                    command=self.button_modificar_resultado)
        self.button_load_config.grid(row=11, column=1, pady=15, padx=20)

        # Modificar ruta de descarga

        self.button_load_config = customtkinter.CTkButton(self.tabview.tab(self.NombreResultado),
                                                    text="Modificar ruta de descarga",
                                                    command=self.button_modificar_ruta_descarga)
        self.button_load_config.grid(row=11, column=2, pady=15, padx=20)
        
        
    ### Eventos interiorizacion
    def button_modificar_resultado(self):
        answer = askyesno(title='Confirmacion',
                    message='Estas seguro de modificar nombre del resultado?')
        if answer:
            USER_INP = simpledialog.askstring(title="Creador Resultado",
                                        prompt="Ingrese nombre resultado:")
            self.tabview.delete(self.NombreResultado)
            
            self.check_var.pop(self.NombreResultado)
            self.check_var[USER_INP] = customtkinter.StringVar(master=self.frame_left,value="off")
            self.checkbox.update({USER_INP:self.checkbox[self.NombreResultado]})
            self.checkbox[USER_INP].configure(text=USER_INP, variable=self.check_var[USER_INP])

            self.ResultadoFront.pop(self.NombreResultado)
            self.NombreResultado = USER_INP
            self.tabview.add(self.NombreResultado)
            self.ResultadoFront[USER_INP] = Vista(self.tabview, 
                                                  USER_INP, 
                                                  self.check_var, 
                                                  self.checkbox, 
                                                  self.frame_left, 
                                                  self.ResultadoFront,
                                                  self.check_cont)

    def button_modificar_ruta_descarga(self):
        if not self.CalculoResultadoInicial is None or not self.CalculoResultadoFinal is None:
            ruta = filedialog.askdirectory()
            if ruta:
                print("Ruta seleccionada:", ruta)
                GraficasGenerales.modificar_ruta_descarga(self.CalculoResultadoInicial, self.CalculoResultadoFinal,
                                                          ruta)
        else:
            showinfo(
                title='Error en la actualización de ruta',
                message='No se puede actualizar la ruta sin calcular los resultados'
            )


    def button_eliminar_resultado(self):
        answer = askyesno(title='Confirmacion',
                    message='Estas seguro de eliminar el tab?')
        if answer:
            self.tabview.delete(self.NombreResultado)
            self.check_var.pop(self.NombreResultado)
            self.checkbox[self.NombreResultado].destroy()
            self.checkbox.pop(self.NombreResultado)
            self.ResultadoFront.pop(self.NombreResultado)
            self.check_cont = self.check_cont - 1
            showinfo(
                    title='Exito',
                    message= 'Resultado eliminado con exito'
            )
    
    def button_criterio_pregunta(self):
        self.RutaConfigCriterioPregunta = GraficasGenerales.buttonEvent_SeleccionarConfig()
        self.label_seleccion_csv_criterio_pregunta.configure(text=self.limitadorCaracteres(self.RutaConfigCriterioPregunta))

    def button_rubrica_general(self):
        self.RutaConfigRubricaGeneral = GraficasGenerales.buttonEvent_SeleccionarConfig()
        self.label_seleccion_csv_rubrica_general.configure(text=self.limitadorCaracteres(self.RutaConfigRubricaGeneral))

    def button_rubrica_especifica(self):
        self.RutaConfigRubricaEspecifica= GraficasGenerales.buttonEvent_SeleccionarConfig()
        self.label_seleccion_csv_rubrica_especifica.configure(text=self.limitadorCaracteres(self.RutaConfigRubricaEspecifica))
        
        if self.RutaConfigRubricaEspecifica!="" and self.RutaConfigRubricaGeneral != "" and self.RutaConfigCriterioPregunta:
            self.button_save_load_config.configure(state="enabled")
    
    
    def limitadorCaracteres(self, text):
        limite = 50
        return (text[:limite] + '..') if len(text) > limite else text

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def button_load_config(self):
        ## Seleccionar File
        #if self.RutaConfigCriterioPregunta != None and self.RutaConfigRubricaGeneral != None and self.RutaConfigRubricaEspecifica != None:
            self.ResultadoCriterioPregunta = pd.read_csv(self.RutaConfigCriterioPregunta, delimiter=";")
            self.ResultadoRubricaGeneral = pd.read_csv(self.RutaConfigRubricaGeneral, delimiter=";")
            self.ResultadoRubricaEspecifica = pd.read_csv(self.RutaConfigRubricaEspecifica, delimiter=";")
            # Se crea un archivo de guardado
            try:
                ruta_base = os.path.join(os.getenv("APPDATA"), "Evaluación de competencias de PC", "saves")
                print("RUTA BASE",ruta_base)
                if not os.path.exists(ruta_base):
                    print("NO existe ruta se crea")
                    os.makedirs(ruta_base, exist_ok=True)

                ruta_archivo = os.path.join(ruta_base, self.NombreResultado + ".txt")
                f = open(ruta_archivo,mode="w" , encoding="utf-8", errors='ignore')
                f.write(self.ResultadoRuta.getRutaInicial()+"\n")
                f.write(self.ResultadoRuta.getRutaFinal()+"\n")
                f.write(self.RutaConfigCriterioPregunta+"\n")
                f.write(self.RutaConfigRubricaGeneral+"\n")
                f.write(self.RutaConfigRubricaEspecifica+"\n")
                f.close()
                
                showinfo(
                    title='Guardado con Exito',
                    message= 'Las rutas de los documentos fueron guardado con exito'
                )
            except NameError:
                print(NameError)
                showinfo(
                    title='Error',
                    message= 'Error al cargar el archivo'
                )

        
    def button_load_file_path(self):
        try:
            # ruta_archivo = self.resource_path('utilities\\saves\\' + self.NombreResultado + '.txt')
            ruta_base = os.path.join(os.getenv("APPDATA"), "Evaluación de competencias de PC", "saves")
            print("RUTA BASE", ruta_base)
            if not os.path.exists(ruta_base):
                print("NO existe ruta se crea")
                os.makedirs(ruta_base, exist_ok=True)

            ruta_archivo = os.path.join(ruta_base, self.NombreResultado + ".txt")

            f = open(ruta_archivo, "r")
            
            mylist = f.read().splitlines()
            
            self.ResultadoRuta.setRutaInicial(mylist[0])
            self.label_seleccion_csv_i_int.configure(text=self.limitadorCaracteres(self.ResultadoRuta.getRutaInicial()))
            self.ResultadoRuta.setRutaFinal(mylist[1])
            self.label_seleccion_csv_f_int.configure(text=self.limitadorCaracteres(self.ResultadoRuta.getRutaFinal()))
            self.RutaConfigCriterioPregunta = mylist[2]
            self.label_seleccion_csv_criterio_pregunta.configure(text=self.limitadorCaracteres(self.RutaConfigCriterioPregunta))
            self.RutaConfigRubricaGeneral = mylist[3]
            self.label_seleccion_csv_rubrica_general.configure(text=self.limitadorCaracteres(self.RutaConfigRubricaGeneral))
            self.RutaConfigRubricaEspecifica = mylist[4]
            self.label_seleccion_csv_rubrica_especifica.configure(text=self.limitadorCaracteres(self.RutaConfigRubricaEspecifica))
            
            self.ResultadoCriterioPregunta = pd.read_csv(self.RutaConfigCriterioPregunta, delimiter=";")
            self.ResultadoRubricaGeneral = pd.read_csv(self.RutaConfigRubricaGeneral, delimiter=";")
            self.ResultadoRubricaEspecifica = pd.read_csv(self.RutaConfigRubricaEspecifica, delimiter=";")
            
            self.button_save_load_config.configure(state="enabled")
            if self.ResultadoRuta.getRutaInicial()!="" and self.ResultadoRuta.getRutaFinal() != "":
                self.button_calc_int.configure(state="enabled")
            
            showinfo(
                title='Cargardo',
                message= 'Se cargaron la rutas con exito'
            )
            
        except:
            showinfo(
                title='Error',
                message= 'Error al cargar los datos o los datos no existen'
            )
            
     
    def button_select_int_1(self):
        self.seleccionarArchivo("inicial")
    
    def button_select_int_2(self):
        self.seleccionarArchivo("final")
        
    def seleccionarArchivo(self, tipo):
        #Se guarda las rutas obtenidas
        self.ResultadoRuta = GraficasGenerales.buttonEvent_Seleccionar(self.ResultadoRuta, tipo)
        
        # Se escribe ruta del documento seleccionado
        if tipo == "inicial": 
            self.label_seleccion_csv_i_int.configure(text=self.limitadorCaracteres(self.ResultadoRuta.getRutaInicial()))
        else: 
            self.label_seleccion_csv_f_int.configure(text=self.limitadorCaracteres(self.ResultadoRuta.getRutaFinal()))
        
        # Se verifica que se tenga la ruta del documento inicial y final antes de habilitar el calculo
        if self.ResultadoRuta.getRutaInicial()!="" and self.ResultadoRuta.getRutaFinal() != "":
            self.button_calc_int.configure(state="enabled")
    
    
    def calcular_int(self):
        # Interiorizacion
        self.CalculoResultadoInicial = ClasificadorResultados.DefinirResultado(
                                                nombreRuta=self.ResultadoRuta.getRutaInicial(), 
                                                criterioPregunta=self.ResultadoCriterioPregunta,
                                                rubricaGeneral= self.ResultadoRubricaGeneral, 
                                                rubricaEspecifica=self.ResultadoRubricaEspecifica)

        self.CalculoResultadoInicial.iniciar()
        
        self.CalculoResultadoFinal = ClasificadorResultados.DefinirResultado(
                                                nombreRuta=self.ResultadoRuta.getRutaFinal(), 
                                                criterioPregunta=self.ResultadoCriterioPregunta,
                                                rubricaGeneral= self.ResultadoRubricaGeneral, 
                                                rubricaEspecifica=self.ResultadoRubricaEspecifica)

        self.CalculoResultadoFinal.iniciar()
        print(self.CalculoResultadoFinal.getTabla())
        
        self.button_download_int.configure(state="enabled")
        
        #llenar el comboBox
        listaCriterios = []
        for i in range(len(self.ResultadoRubricaGeneral['CriterioE'])):
            listaCriterios.append("Criterio Eva. "+str(i+1))
        print(listaCriterios)
        #self.combobox_graficas.set(listaCriterios)
        self.combobox_graficas_int.configure(state="normal",values=listaCriterios)
        
        self.button_grafica_int.configure(state="enabled")
        self.button_grafica_int_2.configure(state="enabled")
        
        ##ARREGLAR
        self.check_var[self.NombreResultado].set("on")
        
        #self.comprobarResultados()
        
        showinfo(
            title='Calculó con exito',
            message='Se ha calculado con exito'
        )
        
    def download_int(self):
        GraficasGenerales.download(self.CalculoResultadoInicial, self.CalculoResultadoFinal)
    def graficar_stackbar_int(self):
        GraficasGenerales.graficar_stackbar(self.CalculoResultadoInicial, self.CalculoResultadoFinal, self.combobox_graficas_int.get())
    def graficar_stackbar_criterios_int(self):
        GraficasGenerales.graficar_stackbar_criterios(self.CalculoResultadoInicial, self.CalculoResultadoFinal)
    
    ### Eventos Interiorizacion fin