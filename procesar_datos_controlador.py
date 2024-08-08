import os
import sys
import shutil
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from modelos import *
from repositorios import *
import pandas as pd
import matplotlib.image as mpimg
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from procesar_datos_vista import Ui_MainWindow
from repositorios import *

from funciones import *
from modelos_metodo_integral import *
from modelos_metodo_arrhenius import *
from componentes_auxiliares import *

#otras ventanas
from crud_db_controlador import PantallaCrud
from flujo_datos_controlador import FlujoDatos

# metodos comunes
from servicios import *


# metodos comunes
from servicios import *

class PanelDataAnalisis(QMainWindow):
    def __init__(self):
        super(PanelDataAnalisis, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()  
        self.RegistroDatosSalidaArrheniusManejador = RegistroDatosSalidaArrheniusManejador()   
        #traer funciones
        self.funciones = Funciones()
        self.modelos_metodo_integral = MetodoIntegralGraficador()
        self.modelos_metodo_arrhenius = ArrheniusGraficador()

        # Inicializar la variable para almacenar el DataFrame
        self.df_datos_cineticos_listos = None
        # metodos comunes refactorizados
        self.metodos_comunes = Servicios()
        self.componentes_auxiliares = ComponentesAuxiliares()

        # Inicializar elementos gráficos
        self.iniciar_iu_elementos()

        # Cargar datos iniciales
        self.buscar_registros()
        self.buscar_dato()
        self.buscar_condiciones_iniciales()
        self.buscar_datos_salida()
        self.buscar_datos_salida_arrhenius()
        self.crud_db = PantallaCrud()
        self.flujo_datos = FlujoDatos()
        self.init_panel_menu()

        self.ajustes_visuales_tabla()
        self.buscar_unidades_nombre_data()

        # Definir panel_izquierdo para cambios
        self.panel_izquierdo = self.ui.tab_3

        #mensajes barra de estado
        self.statusbar=self.ui.statusbar
        self.statusbar.showMessage("Bienvenido al panel para modelar datos")

        # graficos iniciales de arrhenius
        self.grafico_inicial_calcular_arrhenius()

    def iniciar_iu_elementos(self):
        # Tabla de datos cineticos
        self.datos_cineticos_tabla = self.ui.datos_cineticos_tabla
        self.datos_cineticos_tabla.setSortingEnabled(False)

        #Tabla de Reaccion Quimica
        self.reaccion_quimica_tabla = self.ui.reaccion_quimica_tabla
        self.reaccion_quimica_tabla.setSortingEnabled(False)

        # Tabla de condiciones iniciales
        self.condiciones_iniciales_tabla = self.ui.condiciones_iniciales_tabla
        self.condiciones_iniciales_tabla.setSortingEnabled(False)

        #tabla de datos de salida
        self.tabla_datos_salida = self.ui.datos_salida_tabla
        self.tabla_datos_salida.setSortingEnabled(False)
    
        self.datos_salida_arrhenius_tabla = self.ui.datos_salida_arrhenius_tabla
        self.datos_salida_arrhenius_tabla.setSortingEnabled(False)
        
        #cambio de columnas para la tabla de datos de salida
        # Combobox de registro datos experimentales
        self.registro_datos_box = self.ui.registro_datos_box
        self.registro_datos_box.currentIndexChanged.connect(self.imprimir_registro_seleccionado)
        self.registro_datos_box.currentIndexChanged.connect(self.buscar_unidades_nombre_data)


        #combo box filtro datos experimentales
        self.filtro_datos_box = self.ui.filtro_datos_box

        #self.filtro_datos_box.addItem("Todos")  # Añadir "Todos" al iniciar
        self.filtrar_datos()

        #combo box filtro datos experimentales por especie quimica
        self.filtro_datos_box_2 = self.ui.filtro_datos_box_2
        self.filtrar_especie_quimica()

        self.filtro_datos_box_3 = self.ui.filtro_datos_box_3
        self.filtrar_datos_id_condiciones_iniciales()
        
        # Crear un widget para el gráfico de Matplotlib
        self.matplotlib_widget = MatplotlibWidget(self)
        self.matplotlib_widget_1 = MatplotlibWidget(self)

        # Agregar el widget de Matplotlib al QVBoxLayout vista_grafica
        self.ui.vista_grafica_datos.addWidget(self.matplotlib_widget)
        self.ui.vista_grafica_arrhenius.addWidget(self.matplotlib_widget_1)

        #combo box de ajustar_modelo_box
        self.ajustar_modelo_box=self.ui.ajustar_modelo_box
            # Poblar el combobox
        self.mostrar_metodos_ajustador()

        # Conectar la señal currentIndexChanged a la función manejadora
        self.ajustar_modelo_box.currentIndexChanged.connect(self.manejador_seleccion_modelo)
        
        self.graficar_arrhenius = self.ui.graficar_arrhenius
        self.graficar_arrhenius.clicked.connect(self.calcular_arrhenius)

        #botones para abrir otros paneles
        # line edit de modelo de ajuste
        self.reactivo_limitante_inicial_edit = self.ui.reactivo_limitante_inicial_edit
        self.estimacion_inicial_k_edit = self.ui.estimacion_inicial_k_edit
        self.estimacion_inicial_n_edit = self.ui.estimacion_inicial_n_edit
        #line edit de calculo
        self.reactivo_limitante_calculado= self.ui.reactivo_limitante_calculado
        self.k_calculado = self.ui.k_calculado
        self.n_calculado = self.ui.n_calculado
        self.modelo_utilizado = self.ui.modelo_utilizado
        self.guardar_caso_btn = self.ui.guardar_caso_btn
        self.guardar_caso_btn.clicked.connect(self.actualizar_datos_salida)  
        #arrhenius
        self.agregar_a_btn = self.ui.agregar_a_btn  
        self.agregar_a_btn.clicked.connect(self.agregar_datos_salida_arrhenius)

        #boton de ejecutar modelo
        self.ejecutar_modelo_button = self.ui.graficar_btn
        self.ejecutar_modelo_button.clicked.connect(self.ejecutar_modelo)
        
        #Graficar datos de entrada
        self.graficar_datos_btn = self.ui.graficar_datos_btn
        self.graficar_datos_btn.clicked.connect(self.imprimir_registro_seleccionado)

        #boton CRUD
        self.crud_1= self.ui.panel_datos_btn
        self.crud_1.clicked.connect(self.abrir_crud_db)

        #boton ingreso de datos
        self.ingreso_datos_btn = self.ui.ingreso_datos_btn
        self.ingreso_datos_btn.clicked.connect(self.abrir_ingreso_datos)

        # cambiar configuracion de la base de datos
        self.cambiar_config_btn=self.ui.cambiar_config_btn
        self.cambiar_config_btn.clicked.connect(self.cambiar_config_base_datos)

        #nuevo archivo de base de datos
        self.nuevo_archivo_btn=self.ui.nuevo_archivo_btn
        self.nuevo_archivo_btn.clicked.connect(self.crear_base_datos)

        self.respaldar_conjunto_btn = self.ui.respaldar_conjunto_btn
        self.respaldar_conjunto_btn.clicked.connect(self.respaldar_base_datos)

        #reportes de datos
        self.ui.rep1.clicked.connect(self.evento_guardar_clicked)
        self.ui.rep2.clicked.connect(self.evento_guardar_metodo_integral_clicked)
        self.ui.rep3.clicked.connect(self.evento_guardar_metodo_arrhenius_clicked)
        #botones auxiliares
        self.ui.rep_mi.clicked.connect(self.evento_guardar_metodo_integral_clicked)
        self.ui.rep_arrh.clicked.connect(self.evento_guardar_metodo_arrhenius_clicked)

        self.vista_tabla_df = DataFrameWidget(self)
        #self.ui.vista_tabla_df.addWidget(self.vista_tabla_df)
        self.ui.vista_tabla_df.layout().addWidget(self.vista_tabla_df)
        self.vista_tabla_df.hide() # Ocultar la tabla al inicio

        self.ea_r_final=self.ui.ea_r_final
        self.k_0_calculado=self.ui.k_0_calculado
        self.ln_k_0_calculado=self.ui.ln_k_0_calculado

        self.ea_final=self.ui.ea_final

        self.r_box=self.ui.r_box
        self.r_edit = self.ui.r_edit
        #conexiones de r
        self.r_box.currentIndexChanged.connect(self.actualizar_lineedit_constante_r)   
        self.cargar_datos_json_constante_r(r"data\constante_R.json")
        self.r_box.currentIndexChanged.connect(self.multiplicar_valores_ea_r)
        self.r_edit.textChanged.connect(self.multiplicar_valores_ea_r)
        self.r_edit.editingFinished.connect(self.multiplicar_valores_ea_r)

        self.fecha_edit=self.ui.fecha_edit
        self.establecer_fecha_sistema()

        # Crear un atajo para la tecla F5
        shortcut = QShortcut(QKeySequence.StandardKey.Refresh, self)
        shortcut.activated.connect(self.reiniciar_aplicacion)
    
    def ajustes_visuales_tabla(self):
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos, ["id", "Tiempo", "Concentración", "Otra\nPropiedad", "Conversión reactivo\nlimitante", "Tipo\nEspecie", "id condiciones\nIniciales", "Nombre\ndata", "Nombre\nreacción", "Especie\nquímica"])
        self.componentes_auxiliares.ajustar_tabla(self.condiciones_iniciales_tabla, ["id", "Temperatura", "Tiempo", "Presión\nTotal", "Presión\nParcial", "Fracción\nMolar", "Especie\nQuímica", "Tipo\nEspecie", "Detalle", "Nombre\ndata"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos_salida, ["id","Data\nsalida","Fecha","id nombre\ndata","id condiciones\niniciales","id\nRegistro\nunidades","r\nutilizada","Nombre\ndata","Nombre\nreaccion","Δn\nreacción","ε\nreactivo\nlimitante","Tipo\nespecie", "Especie\nquímica","Constante\ncinética", "Orden\nreacción", "Modelo\ncinético", "Tipo\ncálculo", "Detalles"])
        self.componentes_auxiliares.ajustar_tabla(self.reaccion_quimica_tabla, ["id","Especie\nQuimica", "Fórmula", "Coeficiente\nEstequiométrico", "Detalle", "Tipo\nEspecie", "Nombre\nreaccion"])
        self.componentes_auxiliares.ajustar_tabla(self.datos_salida_arrhenius_tabla, ["id","Nombre\ncaso","id\nNombre\ndata\nsalida","id\nNombre\ndata","Fecha","Temperatura","1/Temperatura absoluta","Constante\ncinética","ln\nConstante\ncinética\n0","Energía\nactivación\nR","R\nutilizada","Energía\nactivación","Constante\ncinética\n0","ln\nConstante\ncinética","Detalles"])


        # funciones de la barra de menu
    def init_panel_menu(self):
        self.menu_bar = self.ui.menu_btn
        self.menu_derecho = self.ui.menu_derecho
        self.menu_bar.clicked.connect(self.modificar_menu)
    
    def modificar_menu(self):
        
        if self.menu_derecho.isVisible():
            self.menu_derecho.hide()
        else:
            self.menu_derecho.show()            
   
    def cargar_datos_json_constante_r(self, archivo):
        self.metodos_comunes.cargar_datos_json_box_group_box(archivo, "constante_R_gases", self.r_box, "valor",self.ui.groupBox_22)
    
    def actualizar_lineedit_constante_r(self):
        self.metodos_comunes.actualizar_lineedit(self.r_box, self.r_edit,True)
        self.actualizar_lineedit_unidades()
    
    def actualizar_lineedit_unidades(self):
        # Obtener el objeto JSON seleccionado en el QComboBox de la constante R
        elemento_seleccionado = self.r_box.currentData()

    #funciones de consulta de registros

    def buscar_registros(self):       
        registros = self.RegistroDataExperimentalManejador.consultar()
        self.mostrar_registros(registros)
    
    #despliega en el combobox
    def mostrar_registros(self, registros):
        self.mensaje_error = "No se encontraron registros en la base de datos."
        self.metodos_comunes.desplegar_datos_combo_box(self.registro_datos_box,registros,self.mensaje_error)
    
    def actualizar_condiciones_iniciales(self):
        nombre_data = self.registro_datos_box.currentText()
        if nombre_data == "Seleccione una opción":
            condiciones = self.CondicionesInicialesManejador.consultar()
        else:
            filtros = {'nombre_data': nombre_data}
            condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
        self.mostrar_condiciones_iniciales(condiciones)

    #funciones de consulta de condiciones iniciales

    def buscar_condiciones_iniciales(self):
        condiciones = self.CondicionesInicialesManejador.consultar()
        self.mostrar_condiciones_iniciales(condiciones) 
    
    def buscar_datos_salida(self):
        condiciones = self.RegistroDatosSalidaManejador.consultar()
        self.mostrar_datos_tabla_salida(condiciones)
    
    def buscar_datos_salida_arrhenius(self):
        condiciones = self.RegistroDatosSalidaArrheniusManejador.consultar()
        self.mostrar_datos_salida_arrhenius_tabla(condiciones)

    def mostrar_condiciones_iniciales(self,condiciones):
        self.mensaje_error = "No se encontraron condiciones iniciales en la base de datos."
        #self.metodos_comunes.desplegar_datos_combo_box(self.condiciones_iniciales_box,condiciones,self.mensaje_error)
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones)
    
    def mostrar_condiciones_iniciales_tabla(self, condiciones):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones, True)

    def buscar_dato(self):
        datos_resultados = self.DatosCineticosManejador.consultar()
        self.mostrar_datos_tabla(datos_resultados)

    def filtrar_datos(self):
        self.filtro_datos_box.clear()
        self.filtro_datos_box.addItem("Seleccione una opción")    
        datos_cineticos = self.DatosCineticosManejador.consultar()        
        if datos_cineticos:
            tipos_especie = set(registro.tipo_especie for registro in datos_cineticos)            
            for tipo_especie in tipos_especie:
                self.filtro_datos_box.addItem(tipo_especie)
        else:
            print("No se encontraron datos en la base de datos.")
            #QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)
    
    def filtrar_especie_quimica(self):
        self.filtro_datos_box_2.clear()
        self.filtro_datos_box_2.addItem("Seleccione una opción")
        datos_cineticos = self.DatosCineticosManejador.consultar()
        if datos_cineticos:
            especie_quimica = set(registro.especie_quimica for registro in datos_cineticos)
            
            for especie in especie_quimica:
                self.filtro_datos_box_2.addItem(especie)
        else:
            print("No se encontraron datos en la base de datos.")
            #QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

    def filtrar_datos_id_condiciones_iniciales(self):
        self.filtro_datos_box_3.clear()
        self.filtro_datos_box_3.addItem("Seleccione una opción")

        datos_cineticos = self.DatosCineticosManejador.consultar()

        if datos_cineticos:
            id_condiciones_iniciales = set(registro.id_condiciones_iniciales for registro in datos_cineticos)
            
            for id_condicion in id_condiciones_iniciales:
                self.filtro_datos_box_3.addItem(str(id_condicion))
        else:
            print("No se encontraron datos en la base de datos.")
            #QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

#manejar try except cuando la base de datos no tiene datos, regresar version no refactorizada
    def mostrar_datos_tabla(self, resultados):
        self.tabla_datos = self.datos_cineticos_tabla
        self.tabla_datos.clearContents()
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados,True)

    def mostrar_reaccion_tabla(self, resultados):
        tabla = self.reaccion_quimica_tabla
        tabla.clearContents()
        self.metodos_comunes.mostrar_reacciones(self.reaccion_quimica_tabla, resultados)
    
    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados,True)
    
    def mostrar_datos_salida_arrhenius_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_arrhenius(self.datos_salida_arrhenius_tabla, resultados,True)


    def mostrar_metodos_ajustador(self):
        self.ajustar_modelo_box.clear()
        self.ajustar_modelo_box.addItem("Seleccionar Modelo")
        metodos = [metodo for metodo in dir(MetodoIntegralAjustador) if callable(getattr(MetodoIntegralAjustador, metodo)) and not metodo.startswith("__")]
        for metodo in metodos:
            self.ajustar_modelo_box.addItem(metodo)

        # Maneja la selección del modelo de ajuste
    def manejador_seleccion_modelo(self, index=None, guardar_reporte=False):
        if index == 0 and not guardar_reporte:  # Si se selecciona "Modelos cinéticos", no computa
            QMessageBox.warning(self, "Selección requerida", "Por favor, escoja un modelo.")
            return

        try:
            dataframe = self.df_datos_cineticos_listos
            if dataframe is None:
                QMessageBox.information(self, "Datos no disponibles", "No se han cargado datos cinéticos para ejecutar el modelo.", QMessageBox.StandardButton.Ok)
                return

            # Obtener el nombre del método seleccionado
            nombre_metodo = self.ajustar_modelo_box.itemText(index) if index is not None else self.ajustar_modelo_box.currentText()

            # Obtener el método de la clase MetodoIntegralAjustador
            metodo = getattr(MetodoIntegralAjustador, nombre_metodo)

            # Obtener los parámetros necesarios para el método
            estimacion_inicial_k = self.estimacion_inicial_k_edit.text().strip()
            estimacion_inicial_n = self.estimacion_inicial_n_edit.text().strip()

            # Verificar si los valores son numéricos antes de convertirlos
            try:
                estimacion_inicial_k = float(estimacion_inicial_k)
                estimacion_inicial_n = float(estimacion_inicial_n)
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor ingrese valores numéricos válidos.", QMessageBox.StandardButton.Ok)
                return

            # Manejar el ajuste para el modelo bimolecular
            if nombre_metodo == 'ajustar_modelo_bimolecular':
                # Obtener el nombre de la reacción desde el DataFrame
                if not dataframe.empty:
                    nombre_reaccion = dataframe.iloc[0]['nombre_reaccion']
                else:
                    raise ValueError("El DataFrame de datos cinéticos está vacío.")

                filtro_reaccion = {'nombre_reaccion': nombre_reaccion}
                reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros=filtro_reaccion)
                self.df_reaccion_quimica = pd.DataFrame.from_records([reaccion.__dict__ for reaccion in reaccion_quimica])

                filtros_data = {"nombre_data": self.registro_datos_box.currentText()}
                datos_cineticos = self.DatosCineticosManejador.consultar(filtros=filtros_data)
                self.df_datos_cineticos_completos = pd.DataFrame.from_records([dato.__dict__ for dato in datos_cineticos])

                # Obtener coeficientes
                coeficiente_a_values = self.df_reaccion_quimica.loc[
                    self.df_reaccion_quimica['tipo_especie'] == 'reactivo_limitante', 
                    'coeficiente_estequiometrico'
                ].values

                coeficiente_b_values = self.df_reaccion_quimica.loc[
                    self.df_reaccion_quimica['tipo_especie'] == 'reactivo', 
                    'coeficiente_estequiometrico'
                ].values

                coeficiente_a = coeficiente_a_values[0] if coeficiente_a_values.size > 0 else 1
                coeficiente_b = coeficiente_b_values[0] if coeficiente_b_values.size > 0 else 1

                print("Coeficiente A:", coeficiente_a)
                print("Coeficiente B:", coeficiente_b)

                # Llamar al método ajustador específico para el modelo bimolecular
                if self.estimacion_inicial_n_edit.text().strip():
                    n_inicial = float(self.estimacion_inicial_n_edit.text().strip())
                    #ajustar_modelo_bimolecular(data_cinetica, columna_tiempo, columna_conversion, estimacion_inicial_k, coeficiente_a, coeficiente_b, data_auxiliar):
                    resultado = metodo(dataframe, "tiempo", "conversion_reactivo_limitante", estimacion_inicial_k, 
                                       coeficiente_a, coeficiente_b, self.df_datos_cineticos_completos,n_inicial)

                    k_optimo, A0, m_optimo, _, ecuacion_texto, ecuacion_texto_cadena, ruta_imagen = resultado

                    # Mostrar la imagen generada en el widget de Matplotlib
                    self.mostrar_imagen_datos_vacios(ruta_imagen, grafico_mostrar=self.matplotlib_widget)

                    # Actualizar los campos de la interfaz
                    self.reactivo_limitante_calculado.setText(str(A0))
                    self.k_calculado.setText(str(k_optimo))
                    self.n_calculado.setText(str(m_optimo))
                    self.modelo_utilizado.setText(str(resultado[3]))
                    self.ecuacion_utilizada=(ecuacion_texto_cadena)
                    # Guardar el reporte si se solicita
                    QMessageBox.information(self, "Resultado", f"El modelo se ajustó. Resultado: {resultado[0], resultado[2], resultado[3]}", QMessageBox.StandardButton.Ok)
                    self.statusbar.showMessage(f"El modelo se ajustó. Resultado: {resultado[0], resultado[2], resultado[3]}", 5000)
                    if guardar_reporte:
                        self.guardar_reporte_metodo_integral(resultado, otra_imagen=ruta_imagen)

            else:
                # Llamar al método con los parámetros y el reactivo opcional
                if self.reactivo_limitante_inicial_edit.text().strip():  # Si el campo no está vacío
                    reactivo_limitante_inicial = float(self.reactivo_limitante_inicial_edit.text().strip())
                    resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n, reactivo_limitante_inicial)
                else:
                    resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n)

                # Mostrar resultados
                QMessageBox.information(self, "Resultado", f"El modelo se ajustó. Resultado: {resultado[0], resultado[2], resultado[3]}", QMessageBox.StandardButton.Ok)
                self.statusbar.showMessage(f"El modelo se ajustó. Resultado: {resultado[0], resultado[2], resultado[3]}", 5000)
                print(resultado)

                # Actualizar los campos de la interfaz
                self.reactivo_limitante_calculado.setText(str(resultado[1]))
                self.k_calculado.setText(str(resultado[0]))
                self.n_calculado.setText(str(resultado[2]))
                self.modelo_utilizado.setText(str(resultado[3]))
                self.ecuacion_utilizada=(resultado[5])

                # Graficar utilizando el resultado obtenido
                MetodoIntegralGraficador.graficar_modelo_salida_opcional_ecuacion(
                    dataframe,
                    "tiempo",
                    "concentracion",
                    resultado[0],
                    dataframe['concentracion'].iloc[0],
                    resultado[2],
                    resultado[3],
                    resultado[4],
                    data_producto=None,
                    columna_concentracion_producto=None,
                    grafico="MatplotlibWidget",
                    ax=self.matplotlib_widget.ax,
                    canvas=self.matplotlib_widget.canvas
                )
                if guardar_reporte:
                    self.guardar_reporte_metodo_integral(resultado)

                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ejecutar el modelo: {str(e)}", QMessageBox.StandardButton.Ok)
            return None


            
    def ejecutar_modelo(self):
        index = self.ajustar_modelo_box.currentIndex()
        #self.manejador_seleccion_modelo(index, self.df_datos_cineticos_listos)
        self.manejador_seleccion_modelo(index)

    def abrir_crud_db(self):
        self.crud_db.show()
    
    def abrir_ingreso_datos(self):
        self.flujo_datos.show()

    def imprimir_registro_seleccionado(self):
        nombre_data = self.registro_datos_box.currentText()

        if nombre_data == "Seleccione una opción":
            self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
            self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos para modelar.", 5000)
            return
        
        if not nombre_data:
            return

        id_condiciones_iniciales = self.filtro_datos_box_3.currentText()
        tipo_especie = self.filtro_datos_box.currentText()
        especie_quimica = self.filtro_datos_box_2.currentText()
        try:
            filtros = {'id': id_condiciones_iniciales}
            condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
            self.df_condiciones_iniciales = pd.DataFrame.from_records([condicion.__dict__ for condicion in condiciones])
            print("Condiciones iniciales:", self.df_condiciones_iniciales)
        except Exception as e:
            print(f"Error al consultar condiciones iniciales: {e}")
            self.statusBar().showMessage("Error al consultar condiciones iniciales.", 5000)
            return

        try:
            filtros_nombre_data = {'nombre_data': nombre_data}
            unidades = self.RegistroUnidadesManejador.consultar(filtros=filtros_nombre_data)
            self.df_unidades = pd.DataFrame.from_records([unidad.__dict__ for unidad in unidades])
            print("Unidades:", self.df_unidades)
        except Exception as e:
            print(f"Error al consultar unidades: {e}")
            self.statusBar().showMessage("Error al consultar unidades.", 5000)
            return

        try:
            filtros_dc = {'id_condiciones_iniciales': id_condiciones_iniciales}
            datos_cineticos = self.DatosCineticosManejador.consultar(filtros=filtros_dc)

            nombres_datos = [dato.nombre_data for dato in datos_cineticos]
            if nombre_data not in nombres_datos:
                self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
                self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos válido para modelar.", 5000)
                return

            tipos_datos = [dato.tipo_especie for dato in datos_cineticos]
            if tipo_especie not in tipos_datos:
                self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
                self.statusBar().showMessage("Por favor, seleccione un tipo de especie válido.", 5000)
                return

            especies_datos = [dato.especie_quimica for dato in datos_cineticos]
            if especie_quimica not in especies_datos:
                self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
                self.statusBar().showMessage("Por favor, seleccione una especie química válida.", 5000)
                return

            if tipo_especie != "Seleccione una opción":
                datos_cineticos = [dato for dato in datos_cineticos if dato.tipo_especie == tipo_especie]

            if especie_quimica != "Seleccione una opción":
                datos_cineticos = [dato for dato in datos_cineticos if dato.especie_quimica == especie_quimica]

            self.df_datos_cineticos_listos = pd.DataFrame.from_records([dato.__dict__ for dato in datos_cineticos])

            if not self.df_datos_cineticos_listos.empty:
                self.df_datos_cineticos_listos = self.df_datos_cineticos_listos.sort_values(by=["tiempo", "especie_quimica", "tipo_especie"])
            
            print("Datos cinéticos listos:", self.df_datos_cineticos_listos)
        except Exception as e:
            print(f"Error al procesar datos cinéticos: {e}")
            self.statusBar().showMessage("Error al procesar datos cinéticos.", 5000)
            return

        if self.df_datos_cineticos_listos.empty:
            self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
            return

        try:
            if 'nombre_reaccion' in self.df_datos_cineticos_listos.columns:
                nombre_reaccion = self.df_datos_cineticos_listos['nombre_reaccion'].iloc[0]
                filtro_reaccion = {'nombre_reaccion': nombre_reaccion}
                reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros=filtro_reaccion)
                reaccion_quimica_ecuacion = self.ReaccionQuimicaManejador.imprimir_ecuacion(nombre_reaccion)
                self.ui.reaccion_label.setText(reaccion_quimica_ecuacion)

                self.df_reaccion_quimica = pd.DataFrame.from_records([reaccion.__dict__ for reaccion in reaccion_quimica])
                print("Reacción química:", self.df_reaccion_quimica)

                self.mostrar_reaccion_tabla(reaccion_quimica)
            else:
                print("La columna 'nombre_reaccion' no existe en el DataFrame.")
        except Exception as e:
            print(f"Error al procesar la reacción química: {e}")
            self.statusBar().showMessage("Error al procesar la reacción química.", 5000)
            return

        etiqueta_horizontal = "tiempo"
        etiqueta_vertical = "concentracion"
        titulo = "Concentracion vs Tiempo"
        componente = f"{tipo_especie} - {especie_quimica}"
            
        # Verificar si la columna 'concentracion' está vacía y usar 'otra_propiedad' si es necesario
        if self.df_datos_cineticos_listos['concentracion'].isnull().all() or self.df_datos_cineticos_listos['concentracion'].empty:
            if 'otra_propiedad' in self.df_datos_cineticos_listos.columns:
                etiqueta_vertical = "Otra Propiedad"
                columna_y = "otra_propiedad"
            else:
                self.mostrar_imagen_datos_vacios('assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg', grafico_mostrar=self.matplotlib_widget)
                self.statusBar().showMessage("La columna 'concentracion' y 'otra_propiedad' están vacías. No se puede graficar.", 5000)
                return
        else:
            columna_y = "concentracion"

        try:
            self.matplotlib_widget.canvas.figure.clf()
            self.matplotlib_widget.ax = self.matplotlib_widget.canvas.figure.subplots()

            self.matplotlib_widget.funciones.graficar_datos_experimentales_iniciales(
                self.df_datos_cineticos_listos["tiempo"], 
                self.df_datos_cineticos_listos[columna_y],
                etiqueta_horizontal, 
                etiqueta_vertical, 
                titulo, 
                componente, 
                grafico="MatplotlibWidget", 
                ax=self.matplotlib_widget.ax, 
                canvas=self.matplotlib_widget.canvas
            )

            self.matplotlib_widget.ax.set_xlim([self.df_datos_cineticos_listos["tiempo"].min(), self.df_datos_cineticos_listos["tiempo"].max()])
            self.matplotlib_widget.ax.set_ylim([self.df_datos_cineticos_listos[columna_y].min(), self.df_datos_cineticos_listos[columna_y].max()])
            self.matplotlib_widget.ax.set_xlabel(etiqueta_horizontal)
            self.matplotlib_widget.ax.set_ylabel(etiqueta_vertical)

            self.matplotlib_widget.canvas.draw()

            QMessageBox.information(self, "Datos Listos", "Los datos iniciales han sido identificados y están listos para ser modelados.")
        except KeyError as e:
            print(f"Error: {e}. La columna no existe en el DataFrame.")


    def grafico_inicial_calcular_arrhenius(self):
        try:
            if self.registro_datos_box.currentText() == "Seleccione una opción":
                self.mostrar_imagen_datos_vacios('assets/_a2764da6-9c43-41de-a6b4-5501b6265810.jpeg', grafico_mostrar=self.matplotlib_widget_1)
                #self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos para modelar.", 5000)
                return False
            return True
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "La imagen no se encuentra en la ruta especificada.", QMessageBox.StandardButton.Ok)
            return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {e}", QMessageBox.StandardButton.Ok)
            return False

                
    def calcular_arrhenius(self):
        if self.registro_datos_box.currentText() == "Seleccione una opción":
            self.mostrar_imagen_datos_vacios('assets/_a2764da6-9c43-41de-a6b4-5501b6265810.jpeg', grafico_mostrar=self.matplotlib_widget_1)
            self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos para modelar.", 5000)
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione un nombre de conjunto de datos para modelar.")
            return
        try:
            # Obtener los datos de la base de datos del combo box registro_datos_box
            filtros = {'nombre_data': self.registro_datos_box.currentText()}
            # Consultar datos experimentales
            resultados = self.RegistroDataExperimentalManejador.consultar(filtros=filtros)
            # Verificar si se encontraron resultados
            if resultados:
                #filtros_datos_salida = {'id_registro_data_experimental': resultados[0].id}
                # Consultar datos en condiciones iniciales
                resultados_a_ci = self.CondicionesInicialesManejador.consultar(filtros=filtros)
                # Pasar a DataFrame las condiciones iniciales
                self.df_resultados_a_ci = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_a_ci])
                #print("Condiciones iniciales_todo:", self.df_resultados_a_ci)
                # Filtrado de CI
                print("Condiciones iniciales:", self.df_resultados_a_ci[['id', 'temperatura']])
                # Consultar unidades
                resultados_unidades = self.RegistroUnidadesManejador.consultar(filtros=filtros)
                # Pasar a DataFrame las unidades
                self.df_resultados_unidades = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_unidades])

                fitro_salida = {'id_nombre_data': resultados[0].id, 'id_condiciones_iniciales': self.df_resultados_a_ci["id"].to_string(index=False)}
                resultados_ds = self.RegistroDatosSalidaManejador.consultar(filtros=fitro_salida)
                self.df_resultados_ds = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_ds])

                # Resetea el índice de las Series para evitar problemas de alineación
                temperatura_reset = self.df_resultados_a_ci['temperatura'].reset_index(drop=True)
                constante_cinetica_reset = self.df_resultados_ds['constante_cinetica'].reset_index(drop=True)
                id_data_salida_reset = self.df_resultados_ds['id'].reset_index(drop=True)

                # Concatena las dos Series en un nuevo DataFrame
                self.df_combinado = pd.concat([temperatura_reset, constante_cinetica_reset], axis=1)
                self.df_combinado.columns = ['temperatura', 'constante_cinetica']
                self.df_combinado.dropna(inplace=True)

                # Ejecutar modelo de n puntos
                self.resultado_arrhenius = ArrheniusAjustador.ajustar_modelo_arrhenius_lineal_multiple(self.df_combinado, "temperatura", "constante_cinetica", self.ui.temp_u_l.text())
                QMessageBox.information(self, "Resultado", f"El resultado de la energía de activación es: K0={self.resultado_arrhenius[0]:.4e} ln(K0)={self.resultado_arrhenius[1]:.6f} EA/R={self.resultado_arrhenius[2]:.6e} ", QMessageBox.StandardButton.Ok)

                # Actualizar la barra de estado
                self.statusbar.showMessage(f"El resultado de la energía de activación es: K0={self.resultado_arrhenius[0]} ln(K0)={self.resultado_arrhenius[1]} EA/R={self.resultado_arrhenius[2]} ", 5000)

                # Mostrar los resultados en la tabla de datos
                #self.vista_tabla_df.set_data(self.df_combinado)

                # Mostrar los resultados en los campos de texto
                self.k_0_calculado.setText(str(self.resultado_arrhenius[0]))
                self.ln_k_0_calculado.setText(str(self.resultado_arrhenius[1]))
                self.ea_r_final.setText(str(self.resultado_arrhenius[2]))
                #anexo al dataframe

                # Limpiar la figura por completo y crear un nuevo conjunto de ejes
                self.matplotlib_widget_1.canvas.figure.clf()
                self.matplotlib_widget_1.ax = self.matplotlib_widget_1.canvas.figure.subplots()
                self.escala_temperatura = self.ui.temp_u_l.text()

                # Convertir temperaturas a absolutas y luego a recíprocas
                if self.escala_temperatura == 'C':
                    T_absoluta = self.df_combinado['temperatura'] + 273.15  # Convertir a Kelvin
                elif self.escala_temperatura == 'F':
                    T_absoluta = self.df_combinado['temperatura'] + 459.67  # Convertir a Kelvin
                elif self.escala_temperatura == 'K':
                    T_absoluta = self.df_combinado['temperatura']
                elif self.escala_temperatura == 'R':
                    T_absoluta = self.df_combinado['temperatura']  # Convertir a Kelvin
                else:
                    raise ValueError("Escala de temperatura no reconocida. Elija entre 'C', 'F', 'K' o 'R'.")
                reciproco_T = 1 / T_absoluta
                #columna 1/T reciproco de la temperatura absoluta               
                ln_k = np.log(self.df_combinado['constante_cinetica'])
                #columna logaritmo de la constante cinetica
                self.df_combinado['reciproco_temperatura_absoluta'] = reciproco_T
                self.df_combinado['logaritmo_constante_cinetica'] = ln_k

                titulos_columna_mini_tabla_arrenius = ["Temperatura","Constante\ncinética","1/Temperatura absoluta","ln\nConstante\ncinética"]
                self.vista_tabla_df.set_data(self.df_combinado,titulos_columna_mini_tabla_arrenius)

                self.df_combinado['energia_activacion_R'] = self.resultado_arrhenius[2]
                self.df_combinado['constante_cinetica_0'] = self.resultado_arrhenius[0]
                self.df_combinado['ln_constante_cinetica_0'] = self.resultado_arrhenius[1]
                self.df_combinado['detalles'] = self.resultado_arrhenius[4]
                self.df_combinado['id_nombre_data']=resultados[0].id
                self.df_combinado['id_nombre_data_salida'] = id_data_salida_reset
                #self.df_combinado['r_utilizada'] = self.ui.r_edit.text()
                #self.df_combinado['nombre_caso'] = self.ui.nombre_caso_a_edit.text()
                #self.df_combinado['energia_activacion'] = self.ea_final.text()

                ArrheniusGraficador.graficar_modelo_arrhenius_lineal_multiple(
                    data_cinetica=self.df_combinado,
                    columna_temperatura='temperatura',
                    columna_contante_cinetica='constante_cinetica',
                    escala_temperatura=self.escala_temperatura,
                    k_0=self.resultado_arrhenius[0],
                    energia_activacion_R=self.resultado_arrhenius[2],
                    ecuacion_texto=self.resultado_arrhenius[3],
                    grafico='MatplotlibWidget',
                    ax=self.matplotlib_widget_1.ax,
                    canvas=self.matplotlib_widget_1.canvas
                )

                # Configurar los límites y las etiquetas de los ejes
                self.matplotlib_widget_1.ax.set_xlim([reciproco_T.min(), reciproco_T.max()])
                self.matplotlib_widget_1.ax.set_ylim([ln_k.min(), ln_k.max()])
                self.matplotlib_widget_1.ax.set_xlabel("1/T")
                self.matplotlib_widget_1.ax.set_ylabel("ln(k)")
                self.matplotlib_widget_1.canvas.draw()
            else:
                logging.warning(f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}")
                self.statusbar.showMessage(f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}", 5000)
                QMessageBox.warning(self, "Advertencia", f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}", QMessageBox.StandardButton.Ok)
                return None
        except Exception as e:
            logging.error(f"Error al calcular la energía de activación: {str(e)}")
            return None
        
    def multiplicar_valores_ea_r(self):
        # Obtener el texto del comboBox y el QTextEdit
        valor_r_box = self.r_edit.text()
        valor_ea_r_final = self.ea_r_final.text()

        # Verificar si el valor del comboBox es "Otro" o "Seleccione una opción"
        if valor_r_box == "Otro" or valor_r_box == "Seleccione una opción":
            #QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una opción válida en el comboBox.", QMessageBox.StandardButton.Ok)
            return

        # Verificar si el QTextEdit está vacío
        if not valor_ea_r_final:
            #QMessageBox.warning(self, "Advertencia", "El campo de texto está vacío.", QMessageBox.StandardButton.Ok)
            return

        try:
            # Convertir el valor del QTextEdit a un número (float)
            valor_ea_r_final_num = float(valor_ea_r_final)
            
            # Supongamos que los valores en el comboBox son números (para fines de multiplicación)
            valor_r_box_num = float(valor_r_box)
            
            # Multiplicar los valores
            ea_valor = valor_r_box_num * valor_ea_r_final_num
            
            # Mostrar el resultado
            self.ea_final.setText(str(ea_valor))

        except ValueError:
            QMessageBox.critical(self, "Error", "Los valores deben ser numéricos.", QMessageBox.StandardButton.Ok)
    
    def agregar_datos_salida_arrhenius(self):
        try:
            # Verificar si el campo nombre_caso está vacío
            nombre_caso = self.ui.nombre_caso_a_edit.text().strip()
            if not nombre_caso:
                QMessageBox.warning(self, "Advertencia", "El campo 'Nombre del caso' está vacío. Por favor, ingrese un nombre para continuar.", QMessageBox.StandardButton.Ok)
                return
            # Verificar si el DataFrame self.df_combinado existe y no está vacío
            if not hasattr(self, 'df_combinado') or self.df_combinado.empty:
                QMessageBox.warning(self, "Advertencia", "No se han modelado o no se han seleccionado conjuto de datos. No hay datos para agregar.", QMessageBox.StandardButton.Ok)
                return
            
            # Iterar sobre cada fila del DataFrame
            for index, row in self.df_combinado.iterrows():
                # Crear el objeto de datos de salida para cada fila
                nuevos_datos_salida = DatosSalidaArrhenius(
                    nombre_caso=self.ui.nombre_caso_a_edit.text(),
                    id_nombre_data_salida=int(row['id_nombre_data_salida']),
                    id_nombre_data=int(row['id_nombre_data']),
                    fecha=self.fecha_edit.text(),
                    temperatura=float(row['temperatura']),
                    reciproco_temperatura_absoluta=float(row['reciproco_temperatura_absoluta']),
                    constante_cinetica=float(row['constante_cinetica']),
                    logaritmo_constante_cinetica=float(row['logaritmo_constante_cinetica']),
                    energia_activacion_r=float(row['energia_activacion_R']),
                    r_utilizada=float(self.r_edit.text()),
                    energia_activacion=float(self.ea_final.text()),
                    constante_cinetica_0=float(row['constante_cinetica_0']),
                    logaritmo_constante_cinetica_0=float(row['ln_constante_cinetica_0']),
                    detalles=row['detalles']
                )

                # Intentar agregar los datos de salida en la base de datos
                agregar_resultado = self.RegistroDatosSalidaArrheniusManejador.agregar(nuevos_datos_salida)

                if not agregar_resultado:
                    QMessageBox.critical(self, "Error", f"Hubo un problema al agregar los datos de salida en la fila {index}", QMessageBox.StandardButton.Ok)
                    return

            QMessageBox.information(self, "Información", "Datos de salida agregados correctamente", QMessageBox.StandardButton.Ok)
            self.buscar_datos_salida_arrhenius()  # Actualizar la vista con los nuevos datos

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al agregar los datos de salida: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos de salida: {e}", QMessageBox.StandardButton.Ok)


    def cambiar_config_base_datos(self):
        self.componentes_auxiliares.cambiar_config_base_datos()

    def reiniciar_aplicacion(self):
        self.componentes_auxiliares.reiniciar_aplicacion()

    def crear_base_datos(self):
        self.componentes_auxiliares.crear_base_datos()
    
    def respaldar_base_datos(self):
        self.componentes_auxiliares.respaldar_base_datos()


    def actualizar_datos_salida(self):
        try:
            # Obtener el ID de los datos de salida seleccionados
            fila_seleccionada = self.tabla_datos_salida.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return
            id = int(self.tabla_datos_salida.item(fila_seleccionada, 0).text().strip())

            tipo_especie=self.filtro_datos_box.currentText()
            especie_quimica=self.filtro_datos_box_2.currentText()
            constante_cinetica=float(self.k_calculado.text())
            orden_reaccion=float(self.n_calculado.text())
            modelo_cinetico=self.modelo_utilizado.text()
            detalles = self.ecuacion_utilizada
            

            # Crear el objeto de datos de salida actualizados
            nuevos_datos_salida = {

                "tipo_especie": tipo_especie,
                "especie_quimica": especie_quimica,
                "constante_cinetica": constante_cinetica,
                "orden_reaccion": orden_reaccion,
                "modelo_cinetico": modelo_cinetico,
                "tipo_calculo": "método integral",
                "detalles": detalles
                

            }

            # Intentar actualizar los datos de salida en la base de datos
            actualizar_resultado = self.RegistroDatosSalidaManejador.actualizar(id, nuevos_datos_salida)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Datos de salida actualizados correctamente", QMessageBox.StandardButton.Ok)
                self.buscar_datos_salida()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar los datos de salida", QMessageBox.StandardButton.Ok)
            
        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al actualizar los datos de salida: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar los datos de salida: {e}", QMessageBox.StandardButton.Ok)
            
    def buscar_unidades_nombre_data(self):
        # Verifica si nombre_data_experimental está vacío
        if not self.registro_datos_box.currentText():
            self.ui.temp_u_l.setText("T")
            self.ui.t_u_label.setText("t")
            self.ui.p_u_l.setText("P")
            self.ui.c_u_label.setText("[C]")
            return  # Termina la ejecución del método aquí
        try:
            filtros = {"nombre_data": self.registro_datos_box.currentText()}
            registros = self.RegistroUnidadesManejador.consultar(filtros=filtros)
            if registros:  # Verifica si la lista no está vacía
                # Accede al atributo 'id' del registro directamente

                self.ui.temp_u_l.setText(str(registros[0].temperatura))
                self.ui.t_u_label.setText(str(registros[0].tiempo))
                self.ui.p_u_l.setText(str(registros[0].presion))
                self.ui.c_u_label.setText(str(registros[0].concentracion))
                #self.ui.id_registro_unidades_ds_edit.setText(str(registros[0].id))
            else:
                self.ui.temp_u_l.setText("T")
                self.ui.t_u_label.setText("t")
                self.ui.p_u_l.setText("P")
                self.ui.c_u_label.setText("[C]")
        except Exception as e:
            # Mostrar un mensaje de error en la interfaz de usuario
            self.statusbar.showMessage(f"Error al buscar registros por ID: {e}", 5000)

    def mostrar_imagen_datos_vacios(self, ruta_imagen=None, grafico_mostrar=None):
            try:
                if grafico_mostrar is None:
                    QMessageBox.warning(self, "Advertencia", "No se ha especificado un widget gráfico para mostrar la imagen.", QMessageBox.StandardButton.Ok)
                    return
                
                grafico_mostrar.mostrar_imagen(ruta_imagen)
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "La imagen no se encuentra en la ruta especificada.", QMessageBox.StandardButton.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Se produjo un error al mostrar la imagen: {e}", QMessageBox.StandardButton.Ok)

    def guardar_reporte(self):
        # Crear cuadro de diálogo para guardar archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "HTML Files (*.html)")

        if ruta_archivo:
            # Asegurarse de que la extensión del archivo sea correcta
            if not ruta_archivo.endswith(".html"):
                ruta_archivo += ".html"

            try:
                # Usar el nombre del archivo HTML para el gráfico
                grafico_path = ruta_archivo.replace('.html', '.png')
                self.matplotlib_widget.canvas.figure.savefig(grafico_path, format='png')

                # Crear contenido HTML
                html_content = "<html><head><title>Reporte</title></head><body>"
                html_content += "<h1>Reporte de Datos</h1>"
                html_content += f"<h2>Gráfico</h2><img src='{grafico_path}' alt='Gráfico'>"

                # Agregar tablas al HTML
                #Agregar tablas al HTML con orden de columnas especificado
                if hasattr(self, 'df_unidades') and not self.df_unidades.empty:
                    df_unidades = self.df_unidades.drop(columns=['_sa_instance_state'], errors='ignore')
                    # Ordenar columnas
                    orden_columnas_unidades = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
                    df_unidades = df_unidades.reindex(columns=orden_columnas_unidades)
                    html_content += "<h2>Set de Unidades</h2>"
                    html_content += df_unidades.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_datos_cineticos_listos') and not self.df_datos_cineticos_listos.empty:
                    df_datos_cineticos = self.df_datos_cineticos_listos.drop(columns=['_sa_instance_state'], errors='ignore')
                    # Ordenar columnas
                    orden_columnas_datos_cineticos = ["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
                    df_datos_cineticos = df_datos_cineticos.reindex(columns=orden_columnas_datos_cineticos)
                    html_content += "<h2>Datos Cinéticos Listos</h2>"
                    html_content += df_datos_cineticos.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_condiciones_iniciales') and not self.df_condiciones_iniciales.empty:
                    df_condiciones = self.df_condiciones_iniciales.drop(columns=['_sa_instance_state'], errors='ignore')
                    orden_columnas_condiciones_iniciales = ["id", "temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
                    df_condiciones = df_condiciones.reindex(columns=orden_columnas_condiciones_iniciales)
                    html_content += "<h2>Condiciones Iniciales</h2>"
                    html_content += df_condiciones.to_html(classes='table table-striped', border=0, index=False)

                if hasattr(self, 'df_reaccion_quimica') and not self.df_reaccion_quimica.empty:
                    df_reaccion = self.df_reaccion_quimica.drop(columns=['_sa_instance_state'], errors='ignore')
                    # Ordenar columnas (ajustar el orden según tus necesidades)
                    orden_columnas_reaccion =  ["id","especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
                    df_reaccion = df_reaccion.reindex(columns=orden_columnas_reaccion)
                    html_content += "<h2>Reacción Química</h2>"
                    html_content += df_reaccion.to_html(classes='table table-striped', border=0, index=False)

                html_content += "</body></html>"

                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                QMessageBox.information(self, "Éxito", "El reporte se ha guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el reporte: {e}")
        
    def guardar_reporte_metodo_integral(self, resultado, otra_imagen=None):
        # Crear cuadro de diálogo para guardar archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte del Método Integral", "", "HTML Files (*.html)")

        if ruta_archivo:
            # Asegurarse de que la extensión del archivo sea correcta
            if not ruta_archivo.endswith(".html"):
                ruta_archivo += ".html"
            
            # Crear la ruta para la copia de la imagen
            if otra_imagen:
                grafico_path = ruta_archivo.replace('.html', '.png')
                try:
                    # Copiar la imagen alternativa a la ruta de destino
                    shutil.copy(otra_imagen, grafico_path)
                except Exception as e:
                    QMessageBox.warning(self, "Advertencia", f"No se pudo copiar la imagen alternativa: {e}")

            else:
                grafico_path = ruta_archivo.replace('.html', '.png')
                self.matplotlib_widget.canvas.figure.savefig(grafico_path, format='png')

            # Crear contenido HTML
            html_content = "<html><head><title>Reporte del Método Integral</title></head><body>"
            html_content += "<h1>Reporte del Método Integral</h1>"
            html_content += f"<h2>Gráfico</h2><img src='{grafico_path}' alt='Gráfico'>"

            # Agregar tablas y resultados al HTML
            if hasattr(self, 'df_reaccion_quimica') and not self.df_reaccion_quimica.empty:
                df_reaccion = self.df_reaccion_quimica.drop(columns=['_sa_instance_state'], errors='ignore')
                # Ordenar columnas
                orden_columnas_reaccion = ["id", "especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
                df_reaccion = df_reaccion.reindex(columns=orden_columnas_reaccion)
                html_content += "<h2>Reacción Química</h2>"
                html_content += df_reaccion.to_html(classes='table table-striped', border=0, index=False)

            if hasattr(self, 'df_unidades') and not self.df_unidades.empty:
                df_unidades = self.df_unidades.drop(columns=['_sa_instance_state'], errors='ignore')
                # Ordenar columnas
                orden_columnas_unidades = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
                df_unidades = df_unidades.reindex(columns=orden_columnas_unidades)
                html_content += "<h2>Set de Unidades</h2>"
                html_content += df_unidades.to_html(classes='table table-striped', border=0, index=False)

            if hasattr(self, 'df_datos_cineticos_listos') and not self.df_datos_cineticos_listos.empty:
                df_datos_cineticos = self.df_datos_cineticos_listos.drop(columns=['_sa_instance_state'], errors='ignore')
                # Ordenar columnas
                orden_columnas_datos_cineticos = ["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
                df_datos_cineticos = df_datos_cineticos.reindex(columns=orden_columnas_datos_cineticos)
                html_content += "<h2>Datos Cinéticos Listos</h2>"
                html_content += df_datos_cineticos.to_html(classes='table table-striped', border=0, index=False)

            # Resultados del método integral
            html_content += "<h2>Resultados del Método Integral</h2>"
            html_content += f"<p>k: {resultado[0]}</p>"
            html_content += f"<p>n: {resultado[2]}</p>"
            html_content += f"<p>Reactivo Limitante Calculado: {resultado[1]}</p>"
            html_content += f"<p>Modelo Utilizado: {resultado[3]}</p>"
            html_content += f"<p>Ecuación: {resultado[5]}</p>"

            html_content += "</body></html>"

            try:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                QMessageBox.information(self, "Éxito", "El reporte se ha guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el reporte: {e}")
    
    def guardar_reporte_arrhenius(self, resultado):
        # Definir el nombre del archivo y la ruta
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Guardar Reporte de Arrhenius")
        file_dialog.setNameFilter("HTML Files (*.html)")

        if file_dialog.exec():
            ruta_archivo = file_dialog.selectedFiles()[0]

            # Asegurarse de que la extensión del archivo sea correcta
            if not ruta_archivo.endswith(".html"):
                ruta_archivo += ".html"

            try:
                # Usar el nombre del archivo HTML para el gráfico
                grafico_path = ruta_archivo.replace('.html', '.png')
                self.matplotlib_widget_1.canvas.figure.savefig(grafico_path, format='png')

                # Crear contenido HTML
                html_content = "<html><head><title>Reporte de Arrhenius</title></head><body>"
                html_content += f"<h1>Reporte de Arrhenius</h1>"
                html_content += f"<h2>Gráfico</h2><img src='{grafico_path}' alt='Gráfico'>"

                # Agregar tablas y resultados al HTML
                if hasattr(self, 'df_resultados_a_ci') and not self.df_resultados_a_ci.empty:
                    df_condiciones_iniciales = self.df_resultados_a_ci.drop(columns=['_sa_instance_state'], errors='ignore')
                    orden_columnas_condiciones_iniciales = ["id", "temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
                    df_condiciones_iniciales = df_condiciones_iniciales.reindex(columns=orden_columnas_condiciones_iniciales)
                    html_content += f"<h2>Condiciones Iniciales</h2>"
                    html_content += df_condiciones_iniciales.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_resultados_unidades') and not self.df_resultados_unidades.empty:
                    df_unidades = self.df_resultados_unidades.drop(columns=['_sa_instance_state'], errors='ignore')
                    orden_columnas_unidades = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
                    df_unidades = df_unidades.reindex(columns=orden_columnas_unidades)
                    html_content += f"<h2>Unidades</h2>"
                    html_content += df_unidades.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_combinado'):
                    df_combinado = self.df_combinado.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Datos Combinados</h2>"
                    html_content += df_combinado.to_html(classes='table table-striped', border=0, index=False)
                
                if hasattr(self, 'df_resultados_ds') and not self.df_resultados_ds.empty:
                    df_resultados_ds = self.df_resultados_ds.drop(columns=['_sa_instance_state'], errors='ignore')
                    orden_columnas_resultados_ds = [ "id","nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales","id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion","delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", "tipo_calculo", "detalles"]
                    df_resultados_ds = df_resultados_ds.reindex(columns=orden_columnas_resultados_ds)
                    html_content += f"<h2>Datos de Salida</h2>"
                    html_content += df_resultados_ds.to_html(classes='table table-striped', border=0, index=False)

                # Resultados de Arrhenius
                html_content += f"<h2>Resultados de Arrhenius</h2>"
                html_content += f"<p>K0: {resultado[0]:.4e}</p>"
                html_content += f"<p>ln(K0): {resultado[1]:.6f}</p>"
                html_content += f"<p>EA/R: {resultado[2]:.6e}</p>"
                html_content += f"<p>Ecuación: {resultado[4]}</p>"

                html_content += "</body></html>"

                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                QMessageBox.information(self, "Éxito", "El reporte se ha guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el reporte: {e}")

    def evento_guardar_clicked(self):
        try:
            # Ejecutar la lógica de impresión
            self.imprimir_registro_seleccionado()


            # Verificar si los datos están listos
            if hasattr(self, 'df_datos_cineticos_listos') and self.df_datos_cineticos_listos is not None and not self.df_datos_cineticos_listos.empty:
                self.guardar_reporte()
            else:
                QMessageBox.warning(self, "Advertencia", "No hay datos listos para guardar. Por favor, seleccione un conjunto de datos.")
        except AttributeError as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error de atributo: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")
        
    def evento_guardar_metodo_integral_clicked(self):

        try:
            self.manejador_seleccion_modelo(index=self.ajustar_modelo_box.currentIndex(), guardar_reporte=True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ejecutar el modelo: {str(e)}", QMessageBox.StandardButton.Ok)
            return None
    
    def evento_guardar_metodo_arrhenius_clicked(self):
        try:
            # Verificar que los resultados de Arrhenius estén disponibles
            if hasattr(self, 'resultado_arrhenius'):
                # Guardar el reporte de Arrhenius
                self.guardar_reporte_arrhenius(self.resultado_arrhenius)
            else:
                QMessageBox.warning(self, "Advertencia", "No se han calculado los resultados de Arrhenius. Por favor, calcule los resultados primero.", QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar el reporte: {str(e)}", QMessageBox.StandardButton.Ok)
            return None
        
        # funciones especiales para datos
    def establecer_fecha_sistema(self):
        self.componentes_auxiliares.establecer_fecha_sistema(self.fecha_edit)

    def refrescar_data(self):
        self.buscar_registros()
        self.buscar_dato()
        self.buscar_condiciones_iniciales()
        self.buscar_datos_salida()
        self.buscar_datos_salida_arrhenius()

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Crear la figura de Matplotlib
        self.figure = plt.figure()

        # Crear un lienzo para la figura
        self.canvas = FigureCanvas(self.figure)

        # Obtener el eje actual (ax)
        self.ax = self.figure.add_subplot(111)

        # Agregar un gráfico de ejemplo
        #self.ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
        self.funciones = Funciones()

        # Agregar el lienzo al diseño del widget
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
         

    def mostrar_imagen(self, ruta_imagen):
        self.ax.clear()
        img = mpimg.imread(ruta_imagen)
        self.ax.imshow(img)
        self.ax.axis('off')  # Ocultar los ejes
        self.canvas.draw()

class DataFrameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Crear la tabla de datos
        self.tableWidget = QTableWidget()

        # Configurar el layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def set_data(self, df, columnas=None):
        # Limpiar la tabla antes de actualizarla
        self.tableWidget.clear()

        # Establecer el número de filas y columnas
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])

        # Establecer las etiquetas de las columnas
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        # Llenar la tabla con los datos del DataFrame
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.tableWidget.setItem(row, col, item)

        # definir nombres columnas
        self.tableWidget.setHorizontalHeaderLabels(columnas)

        # Ajustar tamaño de las columnas para que se ajusten al contenido
        self.tableWidget.resizeColumnsToContents()

        # Opcional: Ajustar tamaño de las filas para que se ajusten al contenido
        self.tableWidget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelDataAnalisis()
    window.show()
    sys.exit(app.exec())