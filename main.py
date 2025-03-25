import tkinter
import tkinter.messagebox
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter import filedialog as fd
from tkinter import simpledialog
import customtkinter

import ClasificadorResultados
from utilities.vistas import ResultadoVista

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot  as plt


# instalar librerias
# pip3 install NombreLibreria
# python -m pip install nombre

# pyinstaller --onefile --console --debug=all --distpath ./desk --name "Evaluación de competencias" --add-data "utilities\\saves;utilities\\saves" --icon=utilities/academico.ico --hidden-import=xlsxwriter --hidden-import=customtkinter --hidden-import=pandas --hidden-import=numpy --hidden-import=matplotlib main.py
# pyinstaller --onefile --console --debug=all --distpath ./desk --name "Evaluación de competencias" --icon=utilities/academico.ico --hidden-import=xlsxwriter --hidden-import=customtkinter --hidden-import=pandas --hidden-import=numpy --hidden-import=matplotlib main.py
# pyinstaller --onefile --noconsule --distpath ./release --name "Evaluación de competencias" --icon=utilities/academico.ico --hidden-import=xlsxwriter --hidden-import=customtkinter --hidden-import=pandas --hidden-import=numpy --hidden-import=matplotlib main.py
# pyinstaller --onefile --console --name "Evaluación de competencias"  --icon=utilities/academico.ico --hidden-import=customtkinter --hidden-import=pandas --hidden-import=numpy --hidden-import=matplotlib main.py


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 940
    HEIGHT = 680
    GRADO = "6-1"
    max_chars = 7  # Límite máximo de caracteres
    
    check_cont = 0
    
    check_var = dict()
    checkbox = dict()
    ResultadoFront = dict()

    def get_grado(self):
        return self.GRADO

    def set_grado(self, grado):
        self.GRADO = grado

    def __init__(self):
        super().__init__()

        self.title("Evaluación de competencias de PC")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(9, weight=1)  # empty row as spacing
        #self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Resultados de Aprendizaje"
                                              )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        ## Nombre grado
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Nombre del grupo")
        self.label_mode.grid(row=11, column=0, pady=0, padx=20, sticky="w")
        # ingreso de texto
        self.text_field = customtkinter.CTkTextbox(master=self.frame_left, width=140, height=20)
        self.text_field.grid(row=12, column=0, pady=0, padx=20)
        self.text_field.insert("1.0", self.GRADO)
        self.text_field.bind("<KeyRelease>", self.validate_text_length)
        
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Tipos de Graficos")
        self.label_mode.grid(row=13, column=0, pady=0, padx=20, sticky="w")

        ## BOTONES DE GRAFICOS
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Boxplot",
                                                command=self.boxplot)
        #self.button_1.configure(state="disabled")
        self.button_1.grid(row=14, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Countplot Inicial",
                                                command=self.countplot_inicial)
        #self.button_2.configure(state="disabled")
        self.button_2.grid(row=15, column=0, pady=10, padx=20)
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Countplot Final",
                                                command=self.countplot_final)
        #self.button_3.configure(state="disabled")
        self.button_3.grid(row=16, column=0, pady=10, padx=20)
        
        
        ## CRUD
        
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Resultado de Aprendizaje")
        self.label_mode.grid(row=17, column=0, pady=0, padx=20, sticky="w")
        
        self.button_crud_crear = customtkinter.CTkButton(master=self.frame_left,
                                                text="Crear ",
                                                command=self.createTab)
        self.button_crud_crear.grid(row=18, column=0, pady=10, padx=20)
        
        ## FIN CRUD
        

        
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Apariencia:")
        self.label_mode.grid(row=19, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=20, column=0, pady=10, padx=20, sticky="w")

        
        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        #print(self.frame_right.cget("fg_color"))
        
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============
        
        # Panel
        self.panel = tk.Canvas(
            master=self.frame_info,
            height=600,
            width=400,
            highlightthickness=0,
            bg=self.frame_info.cget("fg_color")[1]
        )
        self.panel.grid(row=0, column=0, sticky="nsew")

        # Vincula el área desplazable con el contenido
        self.panel.bind(
            "<Configure>",
            lambda e: self.panel.configure(
                scrollregion=self.panel.bbox("all")
            )
        )

        # Subframe dentro del Canvas
        self.content_frame = tk.Frame(self.panel, bg=self.frame_info.cget("fg_color")[1])
        self.panel.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Configuración del Scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(
            master=self.frame_info,
            command=self.panel.yview,
            button_color=self.frame_info.cget("fg_color")[0],
            button_hover_color=self.frame_info.cget("fg_color")[1]
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Vincula el scrollbar con el Canvas
        self.panel.configure(yscrollcommand=self.scrollbar.set)

        # Configuración dinámica del tamaño del subframe
        self.content_frame.bind(
            "<Configure>",
            lambda e: self.panel.configure(
                scrollregion=self.panel.bbox("all")
            )
        )

        # Asegura que el contenedor principal pueda expandirse
        self.frame_info.grid_rowconfigure(0, weight=1)
        self.frame_info.grid_columnconfigure(0, weight=1)
        
        # Frame
        self.frame = tk.Frame(self.panel, bg=self.frame_info.cget("fg_color")[1])
        self.panel.create_window((0, 0), window=self.frame, anchor="nw")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self.frame, height=720)
        self.tabview.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="nsew")
        
        ## ========= Resultados Tab =========

        self.crearDefaults("Interiorización")
        self.crearDefaults("Coordinación")
        self.crearDefaults("Encapsulación")
        self.crearDefaults("Generalización")

    def validate_text_length(self, event):
        self.text_field.configure(state="normal")
        current_text = self.text_field.get("1.0",
                                           "end-1c")  # "1.0" es el inicio, "end-1c" es el final menos un carácter (el salto de línea)
        print("TEXTO", current_text, " LEN ", len(current_text))
        # Si el texto excede el límite, truncarlo
        if len(current_text) > self.max_chars:
            self.text_field.delete("1.0 + {} chars".format(self.max_chars), "end")  # Eliminar caracteres adicionales
            print("Limitador")
        else:
            texto = self.text_field.get("1.0", "end-1c")
            print("Texto introducido:", texto)
            self.set_grado(texto)

    ###
    def crearDefaults(self, nombre):
        self.tabview.add(nombre)
        self.tabview.tab(nombre).grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.check_var[nombre] = customtkinter.StringVar(master=self.frame_left,value="off")
        self.checkbox[nombre] = customtkinter.CTkCheckBox(master=self.frame_left, text=nombre,
                                    variable=self.check_var[nombre], onvalue="on", offvalue="off", state="disabled")
        # Asegurar alineación uniforme usando `sticky` en grid
        self.checkbox[nombre].grid(
            row=2 + self.check_cont,
            column=0,
            pady=(5, 5),  # Ajusta el espacio vertical
            padx=(20, 20),  # Ajusta el espacio horizontal
            sticky="w"  # Alinea los checkboxes a la izquierda
        )
    
        self.check_cont = self.check_cont + 1       
        # Se crea contenido del tab
        self.ResultadoFront[nombre] = ResultadoVista.Vista(self.tabview, nombre, self.check_var, self.checkbox, self.frame_left, self.ResultadoFront, self.check_cont)

    ### === Eventos CRUD
    def createTab(self):
        USER_INP = simpledialog.askstring(title="Creador Resultado",
                                        prompt="Ingrese nombre resultado:")
        try:
            if len(self.checkbox) != 8 and USER_INP != None and self.check_var.get(USER_INP) == None:
                
                self.check_var[USER_INP] = customtkinter.StringVar(master=self.frame_left,value="off")
                
                self.checkbox[USER_INP] = customtkinter.CTkCheckBox(master=self.frame_left, text=USER_INP,
                                            variable=self.check_var[USER_INP], onvalue="on", offvalue="off", state="disabled")
                
                self.checkbox[USER_INP].grid(row=2+self.check_cont, column=0, pady=10, padx=20)
                self.check_cont = self.check_cont + 1

                self.tabview.add(USER_INP)
                self.ResultadoFront[USER_INP] = ResultadoVista.Vista(self.tabview, USER_INP, self.check_var, self.checkbox, self.frame_left, self.ResultadoFront, self.check_cont)
            else:
                showerror(
                    title='Error',
                    message= 'Se dejó vacío el ingreso de un nombre o se superó el número máximo de resultados'
                )
        except NameError:
            print(NameError)
            showerror(
                    title='Error',
                    message= 'Resultado de aprendizaje con el mismo nombre'
            )
    
    # Para cambiar el la visualizacion de la apariencia
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            self.frame.configure(bg=self.frame_info.cget("fg_color")[1])
            self.panel.configure(bg=self.frame_info.cget("fg_color")[1])
        elif new_appearance_mode == "Light":
            self.frame.configure(bg=self.frame_info.cget("fg_color")[0])
            self.panel.configure(bg=self.frame_info.cget("fg_color")[0])

    # Evento para cerrar la ventana
    def on_closing(self, event=0):
        self.destroy()
    
    ### Eventos generales para cada uno de los TABs
    
    # Grafica boxplot 
    def boxplot(self):
        calificacion = pd.DataFrame()
        
        # Se verifica si se calculo todos los resultados
        for key in self.check_var:
           if self.check_var[key].get() == "off":
                showerror(
                    title='Error',
                    message= 'Calcula primero todos los resultados'
                )
                return
        
        # Se crear un dataframe que contenga con todas las calificaciones de cada estudiante por resultado
        for key in self.ResultadoFront:
            calificacion[key] = self.ResultadoFront[key].getPandasResultadoInicial().getTabla()['Puntuación del cuestionario']
        
        # Muestra cuadricula de fondo en la figura
        sns.set_style("whitegrid")

        # Se crea la figura con 2 filas y 1 columna
        fig, ax = plt.subplots(2, 1, figsize=(8, 7))
        fig.subplots_adjust(hspace=0.6, wspace=0.6)
        fig.suptitle('Comparativo de Resultados de Aprendizaje')

        # Se insertan los datos de dataframe
        sns.boxplot(
            data = calificacion,
            ax=ax[0],
            whis=[5, 95]
        ).set (
            ylabel='Puntuación',
            # Titulo del grafico boxplot
            title='Diagnóstico Inicial '+self.GRADO
        )

        # Se crea segundo dataframe para cada calificacion final de los estudiante por resultado
        calificacion2 = pd.DataFrame()
        for key in self.ResultadoFront:
            calificacion2[key] = self.ResultadoFront[key].getPandasResultadoFinal().getTabla()['Puntuación del cuestionario']

        # Se insertan los datos
        sns.boxplot(
            data = calificacion2,
            ax=ax[1],
            whis=[5, 95]
        ).set (
            ylabel='Puntuación',
            # Titulo del grafico boxplot
            title='Diagnóstico Final '+self.GRADO
        )
        plt.show()

    def decimal_a_binario(self, decimal):
        if decimal <= 0:
            return "0"
        binario = ""
        while decimal > 0:
            residuo = int(decimal % 2)
            decimal = int(decimal / 2)
            binario = str(residuo) + binario
        return binario

    def countplot_inicial(self):

        # Verificar si los resultados fueron calculados
        for key in self.check_var:
           if self.check_var[key].get() == "off":
                showerror(
                    title='Error',
                    message= 'Calcula primero todos los resultados'
                )
                return

        # Grafico contar cantidad por nivel (A, I, B)

        # Coloco los subplots

        fig, axs = plt.subplots(2,2)
        fig.subplots_adjust(hspace=0.6, wspace=0.6)

        fig.suptitle('Diagnóstico prueba inicial')

        conteo = pd.DataFrame()
        contador = 0

        for key in self.ResultadoFront:
            conteo[key] = self.ResultadoFront[key].getPandasResultadoInicial().getTabla()['Nivel_del_RA']

            binario = int(self.decimal_a_binario(contador))
            left = int(binario / 10)
            right = int(binario % 10)

            sns.countplot(
                            data=conteo,
                            x=key,
                            order=["B","I","A"],
                            ax=axs[left,right]
            ).set(
                    title=key+' Grupo '+self.GRADO,
                    ylabel='Cantidad de Estudiantes',
                    #xlabel='Resultados prueba inicial',
            )
            contador = contador + 1

        ## Colocar Cantidad
        for i in range(2):
                for j in range(2):
                        for container in axs[i,j].containers:
                                axs[i,j].bar_label(container, label_type='center')

        plt.show()


    def countplot_final(self):
        # Verificar si los resultados fueron calculados
        for key in self.check_var:
           if self.check_var[key].get() == "off":
                showerror(
                    title='Error',
                    message= 'Calcula primero todos los resultados'
                )
                return
        # Grafico contar cantidad por nivel (A, I, B)

        # Coloco los subplots

        fig, axs = plt.subplots(2,2)
        fig.subplots_adjust(hspace=0.6, wspace=0.6)

        fig.suptitle('Diagnóstico prueba final')

        conteo = pd.DataFrame()
        contador = 0
        for key in self.ResultadoFront:
            conteo[key] = self.ResultadoFront[key].getPandasResultadoFinal().getTabla()['Nivel_del_RA']
            binario = int(self.decimal_a_binario(contador))
            left = int(binario / 10)
            right = int(binario % 10)
            sns.countplot(
                            data=conteo,
                            x=key,
                            order=["B","I","A"],
                            ax=axs[left,right]
            ).set(
                    title=key+' Grupo '+self.GRADO,
                    ylabel='Cantidad de Estudiantes',
                    #xlabel='Resultados prueba final',
            )
            contador = contador + 1


        ## Colocar Cantidad
        for i in range(2):
                for j in range(2):
                        for container in axs[i,j].containers:
                                axs[i,j].bar_label(container, label_type='center')
        
        plt.show()

# MAIN
if __name__ == "__main__":
    app = App()
    app.mainloop()