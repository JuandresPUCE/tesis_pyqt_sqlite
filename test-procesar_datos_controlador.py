import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from modelos import *
from repositorios import *
import pandas as pd
import matplotlib.image as mpimg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from panel_data_analisis_alterno import Ui_MainWindow
from repositorios import *

from funciones import *
from modelos_metodo_integral import *
from modelos_metodo_arrhenius import *

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
        #traer funciones
        self.funciones = Funciones()
        self.modelos_metodo_integral = MetodoIntegralGraficador()
        self.modelos_metodo_arrhenius = ArrheniusGraficador()

        # Inicializar la variable para almacenar el DataFrame
        self.df_datos_cineticos_listos = None
        # metodos comunes refactorizados
        self.metodos_comunes = Servicios()

        # Inicializar elementos gráficos
        self.iniciar_iu_elementos()

        # Cargar datos iniciales
        self.buscar_registros()
        self.buscar_dato()
        self.buscar_condiciones_iniciales()
        self.buscar_datos_salida()
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
        self.ui.vista_grafica.addWidget(self.matplotlib_widget)
        self.ui.vista_grafico.addWidget(self.matplotlib_widget_1)

        #combo box de ajustar_modelo_box
        self.ajustar_modelo_box=self.ui.ajustar_modelo_box
            # Poblar el combobox
        self.mostrar_metodos_ajustador()

        # Conectar la señal currentIndexChanged a la función manejadora
        self.ajustar_modelo_box.currentIndexChanged.connect(self.manejador_seleccion_modelo)
        
        self.graficar_arrhenius = self.ui.graficar_arrhenius
        self.graficar_arrhenius.clicked.connect(self.calcular_arrenius)

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

        #reoirte de datos
        self.ui.rep1.clicked.connect(self.evento_guardar_clicked)
        self.ui.rep2.clicked.connect(self.evento_guardar_metodo_integral_clicked)

        self.vista_tabla_df = DataFrameWidget(self)
        #self.ui.vista_tabla_df.addWidget(self.vista_tabla_df)
        self.ui.vista_tabla_df.layout().addWidget(self.vista_tabla_df)

        self.ea_r_final=self.ui.ea_r_final
        self.k_0_calculado=self.ui.k_0_calculado
        self.ln_k_0_calculado=self.ui.ln_k_0_calculado
    
    def ajustes_visuales_tabla(self):
         #ajuste visual columnas tabla datos
        titulos_columnas_datos = ["id", "Tiempo", "Concentración", "Otra\nPropiedad", "Conversión\nReactivo\nLimitante", "Tipo\nEspecie", "id\nCondiciones\nIniciales", "Nombre\ndata", "Nombre\nreacción", "Especie\nquímica"]
        self.tabla_datos.setHorizontalHeaderLabels(titulos_columnas_datos)
        self.tabla_datos.resizeColumnsToContents()
         #ajuste visual columnas condiciones iniciales
        titulos_columnas_condiciones_iniciales = ["id", "Temperatura", "Tiempo", "Presión\nTotal", "Presión\nParcial", "Fracción\nMolar", "Especie\nQuímica", "Tipo\nEspecie", "Detalle", "Nombre\ndata"]
        self.condiciones_iniciales_tabla.setHorizontalHeaderLabels(titulos_columnas_condiciones_iniciales)
        self.condiciones_iniciales_tabla.resizeColumnsToContents()
        titulos_columnas_datos_salida = ["id","Data\nsalida","Fecha","id\nNombre\ndata","id\nCondiciones\niniciales","id\nRegistro\nunidades","r\nutilizada","Nombre\ndata","Nombre\nreaccion","Δn\nreacción","ε\nreactivo\nlimitante","Tipo\nespecie", "Especie\nquímica","Constante\ncinética", "Orden\nreacción", "Modelo\ncinético", "Tipo\ncálculo", "Detalles"]        
        self.tabla_datos_salida.setHorizontalHeaderLabels(titulos_columnas_datos_salida)
        self.tabla_datos_salida.resizeColumnsToContents()
        
        #ajuste visual columnas tabla reaccion quimica
        titulos_columnas_reaccion_q = ["id","Especie\nQuimica", "Fórmula", "Coeficiente\nEstequiométrico", "Detalle", "Tipo\nEspecie", "Nombre\nreaccion"]
        # Aplicar los títulos a la tabla
        self.reaccion_quimica_tabla.setHorizontalHeaderLabels(titulos_columnas_reaccion_q)
        # Autoajustar el ancho de las columnas al contenido
        self.reaccion_quimica_tabla.resizeColumnsToContents()

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

    def mostrar_condiciones_iniciales(self,condiciones):
        self.mensaje_error = "No se encontraron condiciones iniciales en la base de datos."
        #self.metodos_comunes.desplegar_datos_combo_box(self.condiciones_iniciales_box,condiciones,self.mensaje_error)
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones)
    
    def mostrar_condiciones_iniciales_tabla(self, condiciones):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones)

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
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)
    
    def filtrar_especie_quimica(self):
        self.filtro_datos_box_2.clear()
        self.filtro_datos_box_2.addItem("Seleccione una opción")
        datos_cineticos = self.DatosCineticosManejador.consultar()
        if datos_cineticos:
            especie_quimica = set(registro.especie_quimica for registro in datos_cineticos)
            
            for especie in especie_quimica:
                self.filtro_datos_box_2.addItem(especie)
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

    def filtrar_datos_id_condiciones_iniciales(self):
        self.filtro_datos_box_3.clear()
        self.filtro_datos_box_3.addItem("Seleccione una opción")

        datos_cineticos = self.DatosCineticosManejador.consultar()

        if datos_cineticos:
            id_condiciones_iniciales = set(registro.id_condiciones_iniciales for registro in datos_cineticos)
            
            for id_condicion in id_condiciones_iniciales:
                self.filtro_datos_box_3.addItem(str(id_condicion))
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

#manejar try except cuando la base de datos no tiene datos, regresar version no refactorizada
    def mostrar_datos_tabla(self, resultados):
        self.tabla_datos = self.datos_cineticos_tabla
        self.tabla_datos.clearContents()
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

    def mostrar_reaccion_tabla(self, resultados):
        tabla = self.reaccion_quimica_tabla
        tabla.clearContents()
        self.metodos_comunes.mostrar_reacciones(self.reaccion_quimica_tabla, resultados)
    
    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados)


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

            # Llamar al método con los parámetros y el reactivo opcional
            if self.reactivo_limitante_inicial_edit.text().strip():  # Si el campo no está vacío
                reactivo_limitante_inicial = float(self.reactivo_limitante_inicial_edit.text().strip())
                resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n, reactivo_limitante_inicial)
            else:
                resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n)

            # Mostrar resultados
            QMessageBox.information(self, "Resultado", f"El modelo se ajustó. Resultado: {resultado[0],resultado[2],resultado[3]}", QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"El modelo se ajustó. Resultado: {resultado[0],resultado[2],resultado[3]}", 5000)
            print(resultado)
            
            # Actualizar los campos de la interfaz
            self.reactivo_limitante_calculado.setText(str(resultado[1]))
            self.k_calculado.setText(str(resultado[0]))
            self.n_calculado.setText(str(resultado[2]))
            self.modelo_utilizado.setText(str(resultado[3]))

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
            self.mostrar_imagen_datos_vacios()
            self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos para modelar.", 5000)
            return
        
        if not nombre_data:
            return

        id_condiciones_iniciales = self.filtro_datos_box_3.currentText()
        tipo_especie = self.filtro_datos_box.currentText()
        especie_quimica = self.filtro_datos_box_2.currentText()

        filtros = {'id': id_condiciones_iniciales}
        condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
        self.df_condiciones_iniciales = pd.DataFrame.from_records([condicion.__dict__ for condicion in condiciones])
        print("Condiciones iniciales:", self.df_condiciones_iniciales)
        
        filtos_nombre_data = {'nombre_data': nombre_data}
        unidades = self.RegistroUnidadesManejador.consultar(filtros=filtos_nombre_data)
        self.df_unidades = pd.DataFrame.from_records([unidad.__dict__ for unidad in unidades])
        print("Unidades:", self.df_unidades)

        filtros_dc = {'id_condiciones_iniciales': id_condiciones_iniciales}
        datos_cineticos = self.DatosCineticosManejador.consultar(filtros=filtros_dc)

        nombres_datos = [dato.nombre_data for dato in datos_cineticos]
        if nombre_data not in nombres_datos:
            self.mostrar_imagen_datos_vacios()
            self.statusBar().showMessage("Por favor, seleccione un nombre de conjunto de datos válido para modelar.", 5000)
            return

        tipos_datos = [dato.tipo_especie for dato in datos_cineticos]
        if tipo_especie not in tipos_datos:
            self.mostrar_imagen_datos_vacios()
            self.statusBar().showMessage("Por favor, seleccione un tipo de especie válido.", 5000)
            return

        especies_datos = [dato.especie_quimica for dato in datos_cineticos]
        if especie_quimica not in especies_datos:
            self.mostrar_imagen_datos_vacios()
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

        if self.df_datos_cineticos_listos.empty:
            self.mostrar_imagen_datos_vacios()
            return

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

        etiqueta_horizontal = "tiempo"
        etiqueta_vertical = "concentracion"
        titulo = "Concentracion vs Tiempo"
        componente = f"{tipo_especie} - {especie_quimica}"
        
        try:
            self.matplotlib_widget.canvas.figure.clf()
            self.matplotlib_widget.ax = self.matplotlib_widget.canvas.figure.subplots()

            self.matplotlib_widget.funciones.graficar_datos_experimentales_iniciales(
                self.df_datos_cineticos_listos["tiempo"], 
                self.df_datos_cineticos_listos["concentracion"],
                etiqueta_horizontal, 
                etiqueta_vertical, 
                titulo, 
                componente, 
                grafico="MatplotlibWidget", 
                ax=self.matplotlib_widget.ax, 
                canvas=self.matplotlib_widget.canvas
            )

            self.matplotlib_widget.ax.set_xlim([self.df_datos_cineticos_listos["tiempo"].min(), self.df_datos_cineticos_listos["tiempo"].max()])
            self.matplotlib_widget.ax.set_ylim([self.df_datos_cineticos_listos["concentracion"].min(), self.df_datos_cineticos_listos["concentracion"].max()])
            self.matplotlib_widget.ax.set_xlabel(etiqueta_horizontal)
            self.matplotlib_widget.ax.set_ylabel(etiqueta_vertical)

            self.matplotlib_widget.canvas.draw()

            QMessageBox.information(self, "Datos Listos", "Los datos iniciales han sido identificados y están listos para ser modelados.")
        except KeyError as e:
            print(f"Error: {e}. La columna no existe en el DataFrame.")

                
    def calcular_arrenius(self):
        try:
            # Obtener los datos de la base de datos del combo box registro_datos_box
            filtros = {'nombre_data': self.registro_datos_box.currentText()}
            #consultar datos experimentales
            resultados= self.RegistroDataExperimentalManejador.consultar(filtros=filtros)
            # Verificar si se encontraron resultados
            if resultados:
                filtros_datos_salida= {'id_registro_data_experimental': resultados[0].id}
                #consultar datos en condiciones iniciales
                resultados_a_ci = self.CondicionesInicialesManejador.consultar(filtros=filtros)
                #pasar a dataframe las condiciones iniciales
                df_resultados_a_ci = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_a_ci])
                #imprimir condiciones iniciales
                #print("Condiciones iniciales:", df_resultados_a_ci[['id', 'temperatura']])
                #consultar unidades
                resultados_unidades = self.RegistroUnidadesManejador.consultar(filtros=filtros)
                #pasar a dataframe las unidades
                df_resultados_unidades = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_unidades])
                #imprimir unidades
                #print("Unidades:", df_resultados_unidades)

                fitro_salida={'id_nombre_data': resultados[0].id,'id_condiciones_iniciales': df_resultados_a_ci["id"].to_string(index=False)}
                #print(fitro_salida)
                resultados_ds = self.RegistroDatosSalidaManejador.consultar(filtros=fitro_salida)
                df_resultados_ds = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_ds])
                #print("Datos Salida:", df_resultados_ds)
                #print("CI T :", df_resultados_a_ci['temperatura'])
                #print("Datos Salida:", df_resultados_ds['constante_cinetica'])
                #return resultados[0].id, print(resultados[0].id)
                # Primero, resetea el índice de las Series para evitar problemas de alineación.
                temperatura_reset = df_resultados_a_ci['temperatura'].reset_index(drop=True)
                constante_cinetica_reset = df_resultados_ds['constante_cinetica'].reset_index(drop=True)

                # Luego, concatena las dos Series en un nuevo DataFrame.
                df_combinado = pd.concat([temperatura_reset, constante_cinetica_reset], axis=1)

                # Renombra las columnas del nuevo DataFrame para reflejar el contenido.
                df_combinado.columns = ['temperatura', 'constante_cinetica']
                df_combinado.dropna(inplace=True)

                # Finalmente, imprime el DataFrame combinado.
                #print(df_combinado.to_string(index=False))
                
                #ejecutar modelo de n puntos
                resultado=ArrheniusAjustador.ajustar_modelo_arrhenius_lineal_multiple(df_combinado, "temperatura", "constante_cinetica",self.ui.temp_u_l.text())
                QMessageBox.information(self, "Resultado", f"El resultado de la energía de activación es: K0={resultado[0]:.4e} ln(K0)={resultado[1]:.6f} EA/R={resultado[2]:.6e} ", QMessageBox.StandardButton.Ok)

                # Imprimir el resultado
                #print("El resultado de la energía de activación es:", resultado)
                
                # Imprimir el resultado en la barra de estado

                self.statusbar.showMessage(f"El resultado de la energía de activación es: K0={resultado[0]} ln(K0)={resultado[1]} EA/R={resultado[2]} ",5000)

                self.vista_tabla_df.set_data(df_combinado)
                #asignar valores a los line edit

                self.k_0_calculado.setText(str(resultado[0]))
                self.ln_k_0_calculado.setText(str(resultado[1]))
                self.ea_r_final.setText(str(resultado[2]))

                # Limpiar la figura por completo
                self.matplotlib_widget_1.canvas.figure.clf()
                # Crear un nuevo conjunto de ejes
                self.matplotlib_widget_1.ax = self.matplotlib_widget_1.canvas.figure.subplots()
                self.escala_temperatura=self.ui.temp_u_l.text()

                 # Convertir temperaturas a absolutas y luego a recíprocas
                if self.escala_temperatura == 'C':
                    T_absoluta = df_combinado['temperatura'] + 273.15  # Convertir a Kelvin
                elif self.escala_temperatura == 'F':
                    T_absoluta = df_combinado['temperatura'] + 459.67  # Convertir a Kelvin
                elif self.escala_temperatura == 'K':
                    T_absoluta = df_combinado['temperatura']
                elif self.escala_temperatura == 'R':
                    T_absoluta = df_combinado['temperatura']  # Convertir a Kelvin
                else:
                    raise ValueError("Escala de temperatura no reconocida. Elija entre 'C', 'F', 'K' o 'R'.")
                reciproco_T = 1 / T_absoluta
                ln_k = np.log(df_combinado['constante_cinetica'])
                #print(ln_k)
                #print(reciproco_T)


                ArrheniusGraficador.graficar_modelo_arrhenius_lineal_multiple(
                    data_cinetica=df_combinado,
                    columna_temperatura='temperatura',
                    columna_contante_cinetica='constante_cinetica',
                    escala_temperatura=self.escala_temperatura,
                    k_0=resultado[0],
                    energia_activacion_R=resultado[2],
                    ecuacion_texto=resultado[3],
                    grafico='MatplotlibWidget',
                    ax=self.matplotlib_widget_1.ax,
                    canvas=self.matplotlib_widget_1.canvas
                )

                # Configurar los límites y las etiquetas de los ejes
                
                #print(f"Reciproco_T: {reciproco_T}, ln_k: {ln_k}")
                self.matplotlib_widget_1.ax.set_xlim([reciproco_T.min(), reciproco_T.max()])
                self.matplotlib_widget_1.ax.set_ylim([ln_k.min(), ln_k.max()])
                self.matplotlib_widget_1.ax.set_xlabel("1/T")
                self.matplotlib_widget_1.ax.set_ylabel("ln(k)")
                # Actualizar el gráfico
                
                #print("Actualizando el gráfico")
                self.matplotlib_widget_1.canvas.draw()

            else:
                logging.warning(f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}")
                self.statusbar.showMessage(f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}",5000)
                QMessageBox.warning(self, "Advertencia", f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}", QMessageBox.StandardButton.Ok)
                return None
            
        except Exception as e:
            logging.error(f"Error al calcular la energía de activación: {str(e)}")
            return None     

    def cambiar_config_base_datos(self):
        self.metodos_comunes.cambiar_configuracion_db()

    def crear_base_datos(self):
        self.metodos_comunes.nueva_configuracion_db()

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

            # Crear el objeto de datos de salida actualizados
            nuevos_datos_salida = {

                "tipo_especie": tipo_especie,
                "especie_quimica": especie_quimica,
                "constante_cinetica": constante_cinetica,
                "orden_reaccion": orden_reaccion,
                "modelo_cinetico": modelo_cinetico,
                "tipo_calculo": "método integral",
                

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

    def mostrar_imagen_datos_vacios(self):
        ruta_imagen = 'assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg'
        try:
            self.matplotlib_widget.mostrar_imagen(ruta_imagen)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "La imagen no se encuentra en la ruta especificada.", QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al mostrar la imagen: {e}", QMessageBox.StandardButton.Ok)

    def guardar_reporte(self):
        # Definir el nombre del archivo y la ruta
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Guardar Reporte")
        file_dialog.setNameFilter("HTML Files (*.html)")

        if file_dialog.exec():
            ruta_archivo = file_dialog.selectedFiles()[0]

            # Asegurarse de que la extensión del archivo sea correcta
            if not ruta_archivo.endswith(".html"):
                ruta_archivo += ".html"

            try:
                # Usar el nombre del archivo HTML para el gráfico
                grafico_path = ruta_archivo.replace('.html', '.png')
                self.matplotlib_widget.canvas.figure.savefig(grafico_path, format='png')

                # Crear contenido HTML
                html_content = "<html><head><title>Reporte</title></head><body>"
                html_content += f"<h1>Reporte de Datos</h1>"
                html_content += f"<h2>Gráfico</h2><img src='{grafico_path}' alt='Gráfico'>"

                # Agregar tablas al HTML
                if hasattr(self, 'df_unidades') and not self.df_unidades.empty:
                    df_unidades = self.df_unidades.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Set de Unidades</h2>"
                    html_content += df_unidades.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_datos_cineticos_listos'):
                    df_datos_cineticos = self.df_datos_cineticos_listos.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Datos Cinéticos Listos</h2>"
                    html_content += df_datos_cineticos.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_condiciones_iniciales') and not self.df_condiciones_iniciales.empty:
                    df_condiciones = self.df_condiciones_iniciales.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Condiciones Iniciales</h2>"
                    html_content += df_condiciones.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_reaccion_quimica') and not self.df_reaccion_quimica.empty:
                    df_reaccion = self.df_reaccion_quimica.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Reacción Química</h2>"
                    html_content += df_reaccion.to_html(classes='table table-striped', border=0, index=False)

                html_content += "</body></html>"

                with open(ruta_archivo, 'w') as f:
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
    
    def guardar_reporte_metodo_integral(self, resultado):
        # Definir el nombre del archivo y la ruta
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Guardar Reporte del Método Integral")
        file_dialog.setNameFilter("HTML Files (*.html)")

        if file_dialog.exec():
            ruta_archivo = file_dialog.selectedFiles()[0]

            # Asegurarse de que la extensión del archivo sea correcta
            if not ruta_archivo.endswith(".html"):
                ruta_archivo += ".html"

            try:
                # Usar el nombre del archivo HTML para el gráfico
                grafico_path = ruta_archivo.replace('.html', '.png')
                self.matplotlib_widget.canvas.figure.savefig(grafico_path, format='png')

                # Crear contenido HTML
                html_content = "<html><head><title>Reporte del Método Integral</title></head><body>"
                html_content += f"<h1>Reporte del Método Integral</h1>"
                html_content += f"<h2>Gráfico</h2><img src='{grafico_path}' alt='Gráfico'>"

                # Agregar tablas y resultados al HTML
                if hasattr(self, 'df_reaccion_quimica') and not self.df_reaccion_quimica.empty:
                    df_reaccion = self.df_reaccion_quimica.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Reacción Química</h2>"
                    html_content += df_reaccion.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_unidades') and not self.df_unidades.empty:
                    df_unidades = self.df_unidades.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Set de Unidades</h2>"
                    html_content += df_unidades.to_html(classes='table table-striped', border=0, index=False)
                if hasattr(self, 'df_datos_cineticos_listos'):
                    df_datos_cineticos = self.df_datos_cineticos_listos.drop(columns=['_sa_instance_state'], errors='ignore')
                    html_content += f"<h2>Datos Cinéticos Listos</h2>"
                    html_content += df_datos_cineticos.to_html(classes='table table-striped', border=0, index=False)

                # Resultados del método integral
                html_content += f"<h2>Resultados del Método Integral</h2>"
                html_content += f"<p>k: {resultado[0]}</p>"
                html_content += f"<p>n: {resultado[2]}</p>"
                html_content += f"<p>Reactivo Limitante Calculado: {resultado[1]}</p>"
                html_content += f"<p>Modelo Utilizado: {resultado[3]}</p>"
                html_content += f"<p>Ecuación: {resultado[5]}</p>"

                html_content += "</body></html>"

                with open(ruta_archivo, 'w') as f:
                    f.write(html_content)

                QMessageBox.information(self, "Éxito", "El reporte se ha guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el reporte: {e}")
    
    def evento_guardar_metodo_integral_clicked(self):

        try:
            self.manejador_seleccion_modelo(index=self.ajustar_modelo_box.currentIndex(), guardar_reporte=True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ejecutar el modelo: {str(e)}", QMessageBox.StandardButton.Ok)
            return None


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

    def set_data(self, df):
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

        # Ajustar tamaño de las columnas para que se ajusten al contenido
        self.tableWidget.resizeColumnsToContents()

        # Opcional: Ajustar tamaño de las filas para que se ajusten al contenido
        self.tableWidget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelDataAnalisis()
    window.show()
    sys.exit(app.exec())