import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot  as plt
import warnings

import os
from xlsxwriter import Workbook

CRITERIO_EVALUACION = 'CriterioE'
INDICADOR_LOGRO = 'Indicador_L'
DIM_CRITERIO = 'CE'
DIM_INDICADOR = 'IL'
PORC_AVANZADO = 81
PORC_BASICO   = 40

def calcularNivelBasicoGeneral(rubricaGeneral):
  
  """
  Esta funcion se encargar de calcular el nivel basicos
  de los resultados de aprendizaje por medio de los 
  criterios generales.   

  Args:
      rubricaGeneral (DataFrame): 
      Documento de criterio general cargado previamente.

  Returns:
      resultado (DataFrame): 
      Calculo de nivel basico para el RA.
  """
  
  print("Funcion calcularNivelBasicoGeneral")
  print("Argumento -> \n",rubricaGeneral)
  
  resultado       = pd.DataFrame()
  valorIntermedio = 0
  valorBasico     = 0
  valorAvanzado   = 0
  sumaDesempate   = 0
  sumaAvanzado    = 0
  indiceCriterio  = -1

  # Verifico y guardo el criterio con mas peso
  for m in range(len(rubricaGeneral.index)):
    sumaAvanzado    = sumaAvanzado + rubricaGeneral.iloc[m]['Valor_A']
    if rubricaGeneral.iloc[m]['Valor_A'] > valorAvanzado:
      valorAvanzado   = rubricaGeneral.iloc[m]['Valor_A']
      sumaDesempate = rubricaGeneral['Valor_I'].sum() - rubricaGeneral.iloc[m]['Valor_I'] + rubricaGeneral.iloc[m]['Valor_B']
      indiceCriterio  = m

    sumaIntermedio = rubricaGeneral['Valor_I'].sum() - rubricaGeneral.iloc[m]['Valor_I'] + rubricaGeneral.iloc[m]['Valor_B']

    if rubricaGeneral.iloc[m]['Valor_A'] == valorAvanzado and sumaIntermedio > sumaDesempate:
      sumaDesempate = sumaIntermedio
      indiceCriterio  = m
  
  # Asigno el valor basico del criterio con mas peso
  valorBasico = rubricaGeneral.iloc[indiceCriterio]['Valor_B']
  # Sumo todos los demas criterios de menor peso
  for i in range(len(rubricaGeneral.index)):
    if i != indiceCriterio :
      valorIntermedio = valorIntermedio + rubricaGeneral.iloc[i]['Valor_I']
  
  # Se insertan columnas con los Niveles Basicos y Avanzado de cada criterio
  resultado['C'] = [valorIntermedio+valorBasico, sumaAvanzado]

  return resultado

def calcularNivelBasicoEspecifico(rubricaEspecifica, rubricaGeneral):
  """
  Esta funcion se encargar de calcular el nivel basicos
  especifico de los resultados de aprendizaje por medio de los 
  criterios generales y criterios especificos.   

  Args:
      rubricaEspecifica (DataFrame):
      Documento de criterio especifico cargado previamente.
      
      rubricaGeneral (DataFrame):
      Documento de criterio general cargado previamente.

  Returns:
      DataFrame:
      Calculo de nivel basico especifico para el RA.
  """
  resultado       = pd.DataFrame()
  cantCriterios   = len(rubricaGeneral[CRITERIO_EVALUACION])
  # Se recorre cada criterio para calcular el nivel con los sub-criterios
  for i in range(cantCriterios):
    valorIntermedio = 0
    valorBasico     = 0
    valorAvanzado   = 0
    sumaAvanzado    = 0
    sumaDesempate  = 0
    indiceCriterio  = -1
    seleccionCriterio = rubricaEspecifica[INDICADOR_LOGRO].str.contains(DIM_INDICADOR+str(i+1))
    criterio = rubricaEspecifica[seleccionCriterio]
    
    # Verifico y guardo el criterio con mas peso
    for m in range(len(criterio.index)):
      sumaAvanzado    = sumaAvanzado + criterio.iloc[m]['Valor_A']
      if criterio.iloc[m]['Valor_A'] > valorAvanzado:
        valorAvanzado   = criterio.iloc[m]['Valor_A']
        sumaDesempate = criterio['Valor_I'].sum() - criterio.iloc[m]['Valor_I'] + criterio.iloc[m]['Valor_B']
        indiceCriterio  = m

      sumaIntermedio = criterio['Valor_I'].sum() - criterio.iloc[m]['Valor_I'] + criterio.iloc[m]['Valor_B']

      if criterio.iloc[m]['Valor_A'] == valorAvanzado and sumaIntermedio > sumaDesempate:
        sumaDesempate = sumaIntermedio
        indiceCriterio  = m

    # Asigno el valor basico del criterio con mas peso
    valorBasico = criterio.iloc[indiceCriterio]['Valor_B']
    # Sumo todos los demas criterios de menor peso
    for j in range(len(criterio.index)):
      if j != indiceCriterio :
        valorIntermedio = valorIntermedio + criterio.iloc[j]['Valor_I']
    
    # Se insertan columnas con los Niveles Basicos y Avanzado de cada criterio
    resultado['CE'+str(i+1)] = [valorIntermedio+valorBasico, sumaAvanzado]
  # Fin
  return resultado

def sumadorCalificacionesEspecificas(dataCSV, preguntaCriterio , nombreCriterioEspecifico):
  """
  Esta funcion se encarga de sumar los puntajes de las preguntas que estan relacionadas
  bajo un determinado criterio especifico.
  
  Args:
      dataCSV (DataFrame):
      Documento de calificaciones de los estudiantes cargado previamente.
      
      preguntaCriterio (DataFrame):
      Documento de criterio general especifico cargado previamente.
      
      nombreCriterioEspecifico (String): 
      Nombre del criterio especifico (Ejemplo: 'C1_1')

  Returns:
      DataFrame: 
      Retorna una lista calificaciones con suma acumulada por criterio especifico de cada
      estudiante.
  """
  cont = 0
  sumador = 0
  nombre = "/"
  resultado = pd.DataFrame()
  
  while(cont < len(preguntaCriterio['Pregunta'])):
    if(preguntaCriterio[INDICADOR_LOGRO][cont] == nombreCriterioEspecifico):
      sumador = sumador + dataCSV[preguntaCriterio['Pregunta'][cont]]
      nombre = nombre + " + "+preguntaCriterio['Pregunta'][cont]

    cont = cont + 1
    
  resultado[nombre+" / "] = sumador
  return resultado

def calificarTipoCualitativoEspecifico(listaNotas, rubricaEspecifica, nombreCriterioEspecifico):
  """
  Esta funcion se encarga de clasificar y asignar una nota de tipo cualitativo.

  Args:
      listaNotas (DataFrame (array)): 
      lista de notas por criterio especifico.
      
      rubricaEspecifica (DataFrame): 
      Documento de criterio especifico especifico cargado previamente.
      
      nombreCriterioEspecifico (String): 
      Nombre del criterio especifico (Ejemplo: 'IL1_1')

  Returns:
      DataFrame: retorna una lista de calificaciones con la asignacion de valor cualitativo.
  """
  notaCualitativa = []
  notas = listaNotas.to_numpy()
  seleccionCriterio = rubricaEspecifica[INDICADOR_LOGRO] == nombreCriterioEspecifico

  for n in range(len(notas)):
    if notas[n] <= (rubricaEspecifica[seleccionCriterio]['Valor_A'].iloc[0] * PORC_BASICO / 100) : notaCualitativa.append("B")
    elif notas[n] >= (rubricaEspecifica[seleccionCriterio]['Valor_A'].iloc[0] * PORC_AVANZADO / 100 ): notaCualitativa.append("A")
    else: notaCualitativa.append("I")
  
  resultado = pd.DataFrame()
  resultado['Puntuación_'+nombreCriterioEspecifico] = listaNotas
  resultado['Nivel_'+nombreCriterioEspecifico] = pd.Series(notaCualitativa)
  return resultado

def calificarTipoNumericoEspecifico(listaNotas, rubricaEspecifica, nombreCriterioEspecifico):
  """
  Esta funcion se encarga de clasificar y asignar una nota de tipo Numerico.

  Args:
      listaNotas (DataFrame (array)): 
      lista de notas por criterio especifico.
      
      rubricaEspecifica (DataFrame): 
      Documento de criterio especifico especifico cargado previamente.
      
      nombreCriterioEspecifico (String): 
      Nombre del criterio especifico (Ejemplo: 'C1_1')

  Returns:
      DataFrame: retorna una lista de calificaciones con la asignacion de valor tipo numerico.
  """
  notaNumerica = []

  notas = listaNotas.to_numpy()
  mask = rubricaEspecifica[INDICADOR_LOGRO] == nombreCriterioEspecifico

  for n in range(len(notas)):
    # Prueba evaluacion de pre basico - para tener en cuenta trabajo futuro para manejar nivel pre basico
    if notas[n] == 0:
      notaNumerica.append(0)
    elif notas[n] <= (rubricaEspecifica[mask]['Valor_A'].iloc[0] * PORC_BASICO / 100):
      notaNumerica.append(rubricaEspecifica[mask]['Valor_B'].iloc[0])
    elif notas[n] >= (rubricaEspecifica[mask]['Valor_A'].iloc[0] * PORC_AVANZADO / 100):
      notaNumerica.append(rubricaEspecifica[mask]['Valor_A'].iloc[0])
    else: 
      notaNumerica.append(rubricaEspecifica[mask]['Valor_I'].iloc[0])
  
  resultado = pd.DataFrame()
  resultado['V_Cuantitativo_'+nombreCriterioEspecifico] = pd.Series(notaNumerica)
  return resultado

def calificarCriterioGeneral(listaNotas, nivelesEspecificos, rubricaGeneral, nombreCriterioGeneral):
  """
  Esta función se encarga de clasificar y asignar una nota de tipo Cuantitativo y Cualitativo
  a los criterios evaluación.

  Args:
      listaNotas (DataFrame (array)): 
      lista de notas por criterio general.
      
      nivelesEspecificos (DataFrame): 
      Matriz generada por la funcion calcularNivelBasicoEspecifico.
      
      rubricaGeneral (DataFrame): 
      Documento de criterio general cargado previamente.
      
      nombreCriterioGeneral (String):
      Nombre del criterio general  (Ejemplo: 'C1')

  Returns:
      DataFrame: retorna una matriz de calificaciones con la asignacion de valor cualitativo y numerico.
  """
  notaCualitativa = []
  notaNumerica = []

  notas = listaNotas.to_numpy()
  filtroCriterioGeneral = rubricaGeneral[CRITERIO_EVALUACION] == nombreCriterioGeneral

  filtroSeleccionCriterio = nivelesEspecificos.columns == nombreCriterioGeneral
  filtroIndiceCriterio = nivelesEspecificos.columns[filtroSeleccionCriterio]

  for n in range(len(notas)):
    # Prueba evaluacion de pre basico - para tener en cuenta trabajo futuro para manejar nivel pre basico
    if notas[n] == 0:
      notaCualitativa.append("B")
      notaNumerica.append(0)
    elif notas[n] <= (nivelesEspecificos[filtroIndiceCriterio].iloc[1,0] * PORC_BASICO / 100):
      notaCualitativa.append("B")
      notaNumerica.append(rubricaGeneral[filtroCriterioGeneral]['Valor_B'].iloc[0])
    elif notas[n] >= (nivelesEspecificos[filtroIndiceCriterio].iloc[1,0] * PORC_AVANZADO / 100):
      notaCualitativa.append("A")
      notaNumerica.append(rubricaGeneral[filtroCriterioGeneral]['Valor_A'].iloc[0])
    else: 
      notaCualitativa.append("I")
      notaNumerica.append(rubricaGeneral[filtroCriterioGeneral]['Valor_I'].iloc[0])
  
  resultado = pd.DataFrame()
  resultado['Puntuación_'+nombreCriterioGeneral] = listaNotas
  resultado['V_Cuantitativo_'+nombreCriterioGeneral] = pd.Series(notaNumerica)
  resultado['Nivel_'+nombreCriterioGeneral] = pd.Series(notaCualitativa)
  return resultado

def calificarResultadoAprendizaje(listaNotas, nivelesGenerales):
  """
  Este metodo se encarga de tomar las notas de los criterios geneles y los niveles generales
  y asignar una clasificacion al estudiante dentro del resultado de aprendizaje.
  
  Se toma como guia la 2da propuesta definida para la calificacion de los resultados de aprendizajes.
  
  Args:
      listaNotas (DataFrame (array)): 
      lista de notas por criterio general.
      
      nivelesGenerales (DataFrame): 
      Matriz generada por la funcion calcularNivelBasicoGeneral.

  Returns:
      DataFrame: retorna una matriz de calificaciones con la asignacion de valor cualitativo y numerico.
  """
  notaCualitativa = []
  notaNumerica = []

  notas = listaNotas.to_numpy()

  for n in range(len(notas)):
    if notas[n] <= (nivelesGenerales["C"][1] * PORC_BASICO / 100):
      notaCualitativa.append("B")
      notaNumerica.append(nivelesGenerales["C"][0])
    elif notas[n] >= (nivelesGenerales["C"][1] * PORC_AVANZADO / 100):
      notaCualitativa.append("A")
      notaNumerica.append(nivelesGenerales["C"][1])
    else: 
      notaCualitativa.append("I")
  
  resultado = pd.DataFrame()
  resultado['V_Cuantitativo_RA'] = listaNotas
  resultado['Nivel_del_RA'] = pd.Series(notaCualitativa)
  return resultado

def calcularResultado(rubricaGeneral, rubricaEspecifica, criterioPregunta, dataCSV, nivelesGenerales, 
                      nivelesEspecificos):
  
  cantCriterios   = len(rubricaGeneral[CRITERIO_EVALUACION])
  resultado       = pd.DataFrame()
  resultado['Apellidos']  = dataCSV['Apellido(s)']
  resultado['Nombre']     = dataCSV['Nombre']
  
  for i in range(cantCriterios):
    seleccionCriterioEspecifico = rubricaEspecifica[INDICADOR_LOGRO].str.contains(DIM_INDICADOR+str(i+1))
    cantCriteriosEspecificos = len(rubricaEspecifica[seleccionCriterioEspecifico][INDICADOR_LOGRO])

    # Calificador especifico
    for n in range(cantCriteriosEspecificos):
      etiquetaCriterio = DIM_INDICADOR+str(i+1)+'_'+str(n+1)
      listaNotas = sumadorCalificacionesEspecificas(dataCSV, criterioPregunta, etiquetaCriterio)
      print(" listaNotas ")
      print( listaNotas )
      notasCualitativa = calificarTipoCualitativoEspecifico(listaNotas, rubricaEspecifica, etiquetaCriterio)
      print(" notasCualitativa ")
      print( notasCualitativa )
      notasNumerica = calificarTipoNumericoEspecifico(listaNotas,rubricaEspecifica, etiquetaCriterio) 
      print(" notasNumerica ")
      print( notasNumerica )
      # unir resultados 
      resultado = pd.concat([resultado,notasCualitativa], axis=1)
      resultado = pd.concat([resultado,notasNumerica], axis=1)

    # Se suman notas clasificadas anteriormente de tipo numero por criterio general
    notasCriterioGeneralAcumulado = 0
    for n in range(cantCriteriosEspecificos):
      etiquetaCriterio = DIM_INDICADOR+str(i+1)+'_'+str(n+1)
      notasCriterioGeneralAcumulado = notasCriterioGeneralAcumulado + resultado['V_Cuantitativo_'+etiquetaCriterio]
    
    # Calificador de Criterios General con Niveles Basicos Especificos
    calificado = calificarCriterioGeneral(notasCriterioGeneralAcumulado,nivelesEspecificos,rubricaGeneral,"CE"+str(i+1))
    resultado = pd.concat([resultado, calificado], axis=1)
    #print(resultado.head())
  
  # Se suman todas la notas de los criterios general para una calificacion final
  notasGeneralesAcumuladas = 0
  for n in range(cantCriterios):
    notasGeneralesAcumuladas = notasGeneralesAcumuladas + resultado['V_Cuantitativo_CE'+str(n+1)]

  # Calificador Resultado
  resul = calificarResultadoAprendizaje(notasGeneralesAcumuladas,nivelesGenerales)
  resultado = pd.concat([resultado,resul], axis=1)
  return resultado

class DefinirResultado():
  nombreRuta = "calificacionss.csv"
  criterioPregunta = pd.DataFrame()
  rubricaGeneral = pd.DataFrame()
  rubricaEspecifica = pd.DataFrame()
  # Parametros Iniciales
  inicioPreguntas = 0
  RUTA_DESCARGA = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

  #Salida de datos
  tablaResultado = pd.DataFrame()

  def __init__(self, nombreRuta, criterioPregunta, rubricaGeneral, rubricaEspecifica):
    self.nombreRuta = nombreRuta
    self.criterioPregunta = criterioPregunta
    self.rubricaGeneral = rubricaGeneral
    self.rubricaEspecifica = rubricaEspecifica
    self.inicioPreguntas = 3                      # Apartir de esta columna se inicia las preguntas

  def iniciar(self):
    # DEPURACION DE LOS DATOS
    
    df = pd.read_csv(self.nombreRuta, delimiter=";")

    inicioPreguntas = self.inicioPreguntas
    cantPreguntas = len(df.columns)-inicioPreguntas
    columnas = []

    # Renombra columnas
    for i in range(len(df.columns)-inicioPreguntas):
      df = df.rename(columns={df.columns[3+i]:'P. '+str(i+1)})

    df['Calificación/100.00'] = df['Calificación/100.00'].replace('-','0')
    df['Calificación/100.00'] = df['Calificación/100.00'].replace(',','.')
    df['Calificación/100.00'] = df['Calificación/100.00'].astype(float)
    
    # Remover lineas
    for i in range(len(df.columns)-inicioPreguntas):
      df['P. '+str(i+1)] = df['P. '+str(i+1)].replace('-','0')

    # Convertir los datos de str a float
    for i in range(len(df.columns)-inicioPreguntas):
      df['P. '+str(i+1)] = df['P. '+str(i+1)].replace(',','.')

    # Convertir los datos de str a float
    for i in range(len(df.columns)-inicioPreguntas):
      df['P. '+str(i+1)] = df['P. '+str(i+1)].astype(float)

    # Lista de columnas de preguntas
    listaPregunta = df.columns[inicioPreguntas:]

    # EJECUCION DE CALCULOS

    print("rubricaEspecifica")
    print(self.rubricaEspecifica)

    print("rubricaGeneral")
    print(self.rubricaGeneral)

    # Se calcula los niveles de basico general
    NivelesGenerales = calcularNivelBasicoGeneral(self.rubricaGeneral)
    print(" Niveles Generales ")
    print( NivelesGenerales )
    
     # Se calcula los niveles de basico especifico
    NivelesEspecificos = calcularNivelBasicoEspecifico(self.rubricaEspecifica,self.rubricaGeneral)
    print(" Niveles Especificos ")
    print( NivelesEspecificos )
    print(" Datos")
    print(df)
    export = calcularResultado(self.rubricaGeneral,
                              self.rubricaEspecifica,
                              self.criterioPregunta, 
                              df,
                              NivelesGenerales,
                              NivelesEspecificos)

    # DEPURACION DE RESULTADO
    
    # Eliminador de columnas creadas durante el procesamiento de los datos.
    # mask = export.columns.str.contains('C_Numerico_C')
    # mask = mask + export.columns.str.contains('C_Numerico_G_Real')
    # mask = mask + export.columns.str.contains('C_N_Resultado_P')
    # mask2 = np.invert(mask)
    # columnsFilter  = export.columns[mask2]
    # export = export[columnsFilter]

    export['Puntuación del cuestionario'] = df['Calificación/100.00']
    
    # Tabla para crear una nueva hoja
    # tablaNueva = pd.DataFrame()
    # tablaNueva = export
    #
    # mask = tablaNueva.columns.str.contains('C_Numerico')
    # mask = mask + export.columns.str.contains('C_N_Resultado_P')
    # mask2 = np.invert(mask)
    # columnsFilter  = tablaNueva.columns[mask2]
    # tablaNueva = tablaNueva[columnsFilter]

    
    # tabla_cols_numerico = [col for col in tablaNueva.columns if 'Cualitativo' in col]
    # tabla_cols_numerico_new = [x.replace("C_Cualitativo_","")+" RA" for x in tabla_cols_numerico]
    # tablaNueva.rename(columns=dict(zip(tabla_cols_numerico, tabla_cols_numerico_new)), inplace=True)
    # tablaNueva.rename(columns={"C_C_Resultado_P2": "Nivel RA"}, inplace=True)
    
    print("RENOMBRAMIENTO")
    # tablaNueva.rename(columns={"C_C_Resultado_P2": "Nivel RA"}, inplace=True)
    
    print("NUEVA TABLA")
    # print(tabla_cols_numerico)
    # print(tabla_cols_numerico_new)
    # print(tablaNueva)

    pd.set_option('display.max_rows', None)  # Muestra todas las filas
    pd.set_option('display.max_columns', None)  # Muestra todas las columnas
    pd.set_option('display.width', None)  # Ajusta el ancho de la pantalla para que no haya truncamiento
    pd.set_option('display.max_colwidth', None)  # Muestra el contenido completo de cada celda
    
    # self.tablaNueva = tablaNueva
    self.tablaResultado = export
    print("TABLA RESULTANTE -> ")
    print(export)

  def modificar_ruta_descarga(self, nueva_ruta):
    self.RUTA_DESCARGA = nueva_ruta

  def obtener_ruta_descargar(self):
    return self.RUTA_DESCARGA

  def getTabla(self):
    return self.tablaResultado
  
  def getContadorCualitativoEspecifico(self, criterioEspeficico):
    try:
      data_avanzado = self.tablaResultado['Nivel_' + criterioEspeficico].value_counts()['A']
    except ValueError:
      print("ERROR A no existe")
      data_avanzado = 0
    try:
      data_intermedio = self.tablaResultado['Nivel_' + criterioEspeficico].value_counts()['I']
    except ValueError:
      print("ERROR I no existe")
      data_intermedio = 0
    try:
      data_basico = self.tablaResultado['Nivel_' + criterioEspeficico].value_counts()['B']
    except ValueError:
      print("ERROR B no existe")
      data_basico = 0
    return [data_basico, data_intermedio, data_avanzado]
  
  def getCualitativoCriterioGeneral(self, criterioGeneral):
    dim_indicado_logro = criterioGeneral.replace(DIM_CRITERIO, DIM_INDICADOR)
    # Se selecciona columnas del criterioGeneral cualitativas
    filtro_criterio_evaluacion = self.tablaResultado.columns.str.contains(criterioGeneral)
    filtro_indicador_logro = self.tablaResultado.columns.str.contains(dim_indicado_logro)
    filtro_columnas = self.tablaResultado.columns[filtro_criterio_evaluacion].to_list()
    filtro_columnas += self.tablaResultado.columns[filtro_indicador_logro].to_list()
    data = self.tablaResultado[filtro_columnas]
    mask = data.columns.str.contains('Nivel')
    mask = data.columns[mask]
    data = data[mask]
    
    # se cuenta los resultados
    resul = pd.DataFrame()
    # Se cuenta las calificaciones de los criterios especificos

    print("criterioGeneral", criterioGeneral)
    print("dim_indicado_logro", dim_indicado_logro)
    for n in range(len(data.columns) - 1):
      try:
        data_avanzado = data['Nivel_' + dim_indicado_logro + "_" + str(n + 1)].value_counts().get('A', 0)
      except ValueError:
        print("ERROR A no existe")
        data_avanzado = 0
      try:
        data_intermedio = data['Nivel_' + dim_indicado_logro + "_" + str(n + 1)].value_counts().get('I', 0)
      except ValueError:
        print("ERROR I no existe")
        data_intermedio = 0
      try:
        data_basico = data['Nivel_' + dim_indicado_logro + "_" + str(n + 1)].value_counts().get('B', 0)
      except ValueError:
        print("ERROR B no existe")
        data_basico = 0
      resul[dim_indicado_logro + "_" + str(n + 1)] = [data_basico, data_intermedio, data_avanzado]
      
    # Se cuenta del criterio general
    try:
      data_avanzado = data['Nivel_' + criterioGeneral].value_counts().get('A', 0)
    except ValueError:
      print("ERROR A no existe")
      data_avanzado = 0
    try:
      data_intermedio = data['Nivel_' + criterioGeneral].value_counts().get('I', 0)
    except ValueError:
      print("ERROR I no existe")
      data_intermedio = 0
    try:
      data_basico = data['Nivel_' + criterioGeneral].value_counts().get('B', 0)
    except ValueError:
      print("ERROR B no existe")
      data_basico = 0
    resul[criterioGeneral] = [data_basico, data_intermedio, data_avanzado]
    print("criterioGeneral ",resul)
    return resul

  def exportarTabla(self, nombre):
    self.tablaResultado.to_excel(nombre+'.xlsx')
    desktop = self.obtener_ruta_descargar()
    print(desktop)
    out_path =  desktop+"\\"+nombre+".xlsx"
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    self.tablaResultado.to_excel(writer, sheet_name='Sheet1')
    # self.tablaNueva.to_excel(writer, sheet_name='Sheet2')
    writer.close()
  
  def getNombre(self):
    nombre = self.nombreRuta.split("\\")
    nombre = self.nombreRuta.split("/")
    nombre = nombre[len(nombre)-1].split(".")
    return nombre[0]
  
  def getCualitativoCriterios(self):
    listaCriterios = []
    resultado = pd.DataFrame()
    for i in range(len(self.rubricaGeneral[CRITERIO_EVALUACION])):
      conteo = self.getCualitativoCriterioGeneral(DIM_CRITERIO + str(i + 1))
      data_basico = np.array(conteo.iloc[0, len(conteo.columns) - 1])
      data_intermedio = np.array(conteo.iloc[1, len(conteo.columns) - 1])
      data_avanzado = np.array(conteo.iloc[2, len(conteo.columns) - 1])
      resultado[DIM_CRITERIO + str(i + 1)] = [data_basico, data_intermedio, data_avanzado]
    print(" funcion getCualitativoCriterios ", resultado)
    return resultado
