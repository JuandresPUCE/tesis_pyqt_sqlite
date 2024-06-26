import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
#from PyQt6.uic import loadUi
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

#otras ventanas
from test_crud_db_controlador import PantallaCrud
from test2_flujo_datos_controlador import FlujoDatos

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
        self.crud_db = PantallaCrud()
        self.flujo_datos = FlujoDatos()
        self.init_panel_menu()

        # Definir panel_izquierdo para cambios
        self.panel_izquierdo = self.ui.tab_3

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

        # Combobox de registro datos experimentales
        self.registro_datos_box = self.ui.registro_datos_box
        #self.registro_datos_box.currentIndexChanged.connect(self.actualizar_condiciones_iniciales)
        self.registro_datos_box.currentIndexChanged.connect(self.imprimir_registro_seleccionado)
        #self.registro_datos_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)

        # Combobox de condiciones iniciales
        self.condiciones_iniciales_box = self.ui.condiciones_iniciales_box
        #self.condiciones_iniciales_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)
        #self.condiciones_iniciales_box.currentIndexChanged.connect(self.desplegar_condiciones_iniciales_tabla)
        self.filtrar_datos_condiciones_iniciales()

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

        # Agregar el widget de Matplotlib al QVBoxLayout vista_grafica
        self.ui.vista_grafica.addWidget(self.matplotlib_widget)

        #combo box de ajustar_modelo_box
        self.ajustar_modelo_box=self.ui.ajustar_modelo_box
            # Poblar el combobox
        self.mostrar_metodos_ajustador()

        # Conectar la señal currentIndexChanged a la función manejadora
        self.ajustar_modelo_box.currentIndexChanged.connect(self.manejador_seleccion_modelo)
        
        self.opcion_btn_3 = self.ui.opcion_btn_3
        self.opcion_btn_3.clicked.connect(self.calcular_arrenius)

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

        #boton de ejecutar modelo
        self.ejecutar_modelo_button = self.ui.graficar_btn
        self.ejecutar_modelo_button.clicked.connect(self.ejecutar_modelo)

        #boton CRUD
        self.crud_1= self.ui.panel_datos_btn
        self.crud_1.clicked.connect(self.abrir_crud_db)

        #boton ingreso de datos
        self.ingreso_datos_btn = self.ui.ingreso_datos_btn
        self.ingreso_datos_btn.clicked.connect(self.abrir_ingreso_datos)

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
        if nombre_data == "Todos":
            condiciones = self.CondicionesInicialesManejador.consultar()
        else:
            filtros = {'nombre_data': nombre_data}
            condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
        self.mostrar_condiciones_iniciales(condiciones)

    #funciones de consulta de condiciones iniciales

    def buscar_condiciones_iniciales(self):
        condiciones = self.CondicionesInicialesManejador.consultar()
        self.mostrar_condiciones_iniciales(condiciones) 

    def mostrar_condiciones_iniciales(self,condiciones):
        self.mensaje_error = "No se encontraron condiciones iniciales en la base de datos."
        self.metodos_comunes.desplegar_datos_combo_box(self.condiciones_iniciales_box,condiciones,self.mensaje_error)
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones)
    
    def desplegar_condiciones_iniciales_tabla(self):
        nombre_data = self.registro_datos_box.currentText()
        condicion_inicial_id = self.condiciones_iniciales_box.currentData()

        filtros = {}
        if nombre_data and nombre_data != "Todos":
            filtros['nombre_data'] = nombre_data
        if condicion_inicial_id and condicion_inicial_id != "Todos":
            filtros['id'] = condicion_inicial_id

        #condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
        #self.mostrar_condiciones_iniciales_tabla(condiciones)

    def mostrar_condiciones_iniciales_tabla(self, condiciones):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.condiciones_iniciales_tabla, condiciones)

    def buscar_dato(self):
        datos_resultados = self.DatosCineticosManejador.consultar()
        self.mostrar_datos_tabla(datos_resultados)

    def filtrar_datos_condiciones_iniciales(self):
        self.condiciones_iniciales_box.clear()
        self.condiciones_iniciales_box.addItem("Todos")

        condiciones_iniciales = self.CondicionesInicialesManejador.consultar()

        if condiciones_iniciales:
            nombre_data_columna = set(registro.nombre_data for registro in condiciones_iniciales)
            
            for nombre_data in nombre_data_columna:
                self.condiciones_iniciales_box.addItem(str(nombre_data))
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)


    def filtrar_datos(self):
        self.filtro_datos_box.clear()
        self.filtro_datos_box.addItem("Todos")    
        datos_cineticos = self.DatosCineticosManejador.consultar()        
        if datos_cineticos:
            tipos_especie = set(registro.tipo_especie for registro in datos_cineticos)            
            for tipo_especie in tipos_especie:
                self.filtro_datos_box.addItem(tipo_especie)
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)
    
    def filtrar_especie_quimica(self):
        self.filtro_datos_box_2.clear()
        self.filtro_datos_box_2.addItem("Todos")
        datos_cineticos = self.DatosCineticosManejador.consultar()
        if datos_cineticos:
            especie_quimica = set(registro.especie_quimica for registro in datos_cineticos)
            
            for especie in especie_quimica:
                self.filtro_datos_box_2.addItem(especie)
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

    def filtrar_datos_id_condiciones_iniciales(self):
        self.filtro_datos_box_3.clear()
        self.filtro_datos_box_3.addItem("Todos")

        datos_cineticos = self.DatosCineticosManejador.consultar()

        if datos_cineticos:
            id_condiciones_iniciales = set(registro.id_condiciones_iniciales for registro in datos_cineticos)
            
            for id_condicion in id_condiciones_iniciales:
                self.filtro_datos_box_3.addItem(str(id_condicion))
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)

#manejar try except cuando la base de datos no tiene datos, regresar version no refactorizada
    def mostrar_datos_tabla(self, resultados):
        tabla = self.datos_cineticos_tabla
        tabla.clearContents()
        self.metodos_comunes.mostrar_datos_tabla(tabla, resultados)

    def mostrar_reaccion_tabla(self, resultados):
        tabla = self.reaccion_quimica_tabla
        tabla.clearContents()
        self.metodos_comunes.mostrar_reacciones(self.reaccion_quimica_tabla, resultados)
    

    def actualizar_datos_cineticos(self):
        nombre_data = self.registro_datos_box.currentText()
        condicion_inicial_id = self.condiciones_iniciales_box.currentData()

        filtros = {}
        if nombre_data and nombre_data != "Todos":
            filtros['nombre_data'] = nombre_data
        if condicion_inicial_id and condicion_inicial_id != "Todos":
            filtros['id_condiciones_iniciales'] = condicion_inicial_id

        datos_cineticos = self.DatosCineticosManejador.consultar(filtros=filtros)
        self.mostrar_datos_tabla(datos_cineticos)    


    def mostrar_metodos_ajustador(self):
        self.ajustar_modelo_box.clear()
        self.ajustar_modelo_box.addItem("Seleccionar Modelo")
        metodos = [metodo for metodo in dir(MetodoIntegralAjustador) if callable(getattr(MetodoIntegralAjustador, metodo)) and not metodo.startswith("__")]
        for metodo in metodos:
            self.ajustar_modelo_box.addItem(metodo)

    # Maneja la selección del modelo de ajuste
    def manejador_seleccion_modelo(self, index):
        if index == 0:  # Si se selecciona "Modelos cinéticos", no computa
            return

        try:
            dataframe = self.df_datos_cineticos_listos
            if dataframe is None:
                QMessageBox.information(self, "Datos no disponibles", "No se han cargado datos cinéticos para ejecutar el modelo.", QMessageBox.StandardButton.Ok)
                return

            # Obtener el nombre del método seleccionado
            nombre_metodo = self.ajustar_modelo_box.itemText(index)

            # Obtener el método de la clase MetodoIntegralAjustador
            metodo = getattr(MetodoIntegralAjustador, nombre_metodo)

            # Obtener los parámetros necesarios para el método
            #reactivo_limitante_inicial = self.reactivo_limitante_inicial_edit.text().strip()
            estimacion_inicial_k = self.estimacion_inicial_k_edit.text().strip()
            estimacion_inicial_n = self.estimacion_inicial_n_edit.text().strip()

            # Verificar si los valores son numéricos antes de convertirlos
            try:
                #reactivo_limitante_inicial = float(reactivo_limitante_inicial)
                estimacion_inicial_k = float(estimacion_inicial_k)
                estimacion_inicial_n = float(estimacion_inicial_n)  # Asumimos que n es un entero
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor ingrese valores numéricos válidos.", QMessageBox.StandardButton.Ok)
                return

            # Llamar al método con los parámetros y el reactivo opcional
            if self.reactivo_limitante_inicial_edit.text().strip():  # Si el campo no está vacío
                reactivo_limitante_inicial = float(self.reactivo_limitante_inicial_edit.text().strip())
                resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n, reactivo_limitante_inicial)
            else:
                resultado = metodo(dataframe, "tiempo", "concentracion", estimacion_inicial_k, estimacion_inicial_n)

            QMessageBox.information(self, "Resultado", f"El modelo se ajustó. Resultado: {resultado}", QMessageBox.StandardButton.Ok)
            print(resultado)
            #colocar en un box para enviar a la base de datos
            self.reactivo_limitante_calculado.setText(str(resultado[1]))
            self.k_calculado.setText(str(resultado[0]))
            self.n_calculado.setText(str(resultado[2]))
            self.modelo_utilizado.setText(nombre_metodo)
            
            # Graficar utilizando el resultado obtenido

            MetodoIntegralGraficador.graficar_modelo_salida_opcional(
            dataframe,
            "tiempo",
            "concentracion",
            resultado[0],  # Suponiendo que el primer valor retornado es k_ord_n_optimo
            dataframe['concentracion'].iloc[0],  # Suponiendo que el segundo valor retornado es A_0_optimo
            resultado[2],  # Suponiendo que el tercer valor retornado es n_optimo
            data_producto=None,
            columna_concentracion_producto=None,

            )

            MetodoIntegralGraficador.graficar_modelo_salida_opcional(
            dataframe,
            "tiempo",
            "concentracion",
            resultado[0],  # Suponiendo que el primer valor retornado es k_ord_n_optimo
            dataframe['concentracion'].iloc[0],  # Suponiendo que el segundo valor retornado es A_0_optimo
            resultado[2],  # Suponiendo que el tercer valor retornado es n_optimo
            data_producto=None,
            columna_concentracion_producto=None,
            grafico="MatplotlibWidget", 
            ax=self.matplotlib_widget.ax, 
            canvas=self.matplotlib_widget.canvas
            )
            
            return resultado
            # Ahora, graficamos el modelo utilizando los resultados obtenidos
            


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

        if hasattr(self, 'flujo_datos'):
            self.flujo_datos.setParent(None)
            self.flujo_datos.deleteLater()

        self.flujo_datos = FlujoDatos(self)
        self.flujo_datos.setParent(self.panel_izquierdo)

        if self.panel_izquierdo.layout() is None:
            self.layout = QVBoxLayout(self.panel_izquierdo)
        else:
            self.layout = self.panel_izquierdo.layout()

        self.layout.addWidget(self.flujo_datos)

        self.flujo_datos.show()
    
    def imprimir_registro_seleccionado(self):
        nombre_data = self.registro_datos_box.currentText()
        id_condiciones_iniciales = self.filtro_datos_box_3.currentText()
        nombre_data_filtro = self.condiciones_iniciales_box.currentText()
        tipo_especie = self.filtro_datos_box.currentText()
        especie_quimica = self.filtro_datos_box_2.currentText()

        if not nombre_data:
            return
        
        filtros = {'id': id_condiciones_iniciales}
        condiciones = self.CondicionesInicialesManejador.consultar(filtros=filtros)
        # Convertir las condiciones iniciales a un DataFrame de pandas
        df_condiciones_iniciales = pd.DataFrame.from_records([condicion.__dict__ for condicion in condiciones])
        print("Condiciones iniciales:", df_condiciones_iniciales)

        filtros_dc = {'id_condiciones_iniciales': id_condiciones_iniciales}

        # Consultar datos cinéticos filtrando por id de condiciones iniciales
        datos_cineticos = self.DatosCineticosManejador.consultar(filtros=filtros_dc)

        # Filtrar datos cinéticos por tipo_especie si se selecciona uno específico
        if tipo_especie != "Todos":
            datos_cineticos = [dato for dato in datos_cineticos if dato.tipo_especie == tipo_especie]
        
        # Filtrar datos cinéticos por especie_quimica si se selecciona una específica
        if especie_quimica != "Todos":
            datos_cineticos = [dato for dato in datos_cineticos if dato.especie_quimica == especie_quimica]

        # Convertir los datos a un DataFrame de pandas
        df_datos_cineticos_listos = pd.DataFrame.from_records([dato.__dict__ for dato in datos_cineticos])

                # Verificar si el DataFrame está vacío
        if not df_datos_cineticos_listos.empty:
            # Si no está vacío, ordenar por las columnas especificadas
            df_datos_cineticos_listos = df_datos_cineticos_listos.sort_values(by=["tiempo", "especie_quimica","tipo_especie" ])
                
        print("Datos cinéticos listos:", df_datos_cineticos_listos)
        # Guardar df_datos_cineticos_listos como variable de instancia
        
        self.df_datos_cineticos_listos = df_datos_cineticos_listos

        if df_datos_cineticos_listos.empty:
            ruta_imagen = 'assets/_2dcfdd65-68b6-4c73-ab67-0c542d136375.jpeg'
            self.matplotlib_widget.mostrar_imagen(ruta_imagen)
            return

        # Verificar si la columna 'nombre_reaccion' existe en el DataFrame
        if 'nombre_reaccion' in df_datos_cineticos_listos.columns:
            # Obtener el nombre de la reacción de la base de datos datos_ingresados_cineticos
            nombre_reaccion = df_datos_cineticos_listos['nombre_reaccion'].iloc[0]

            filtro_reaccion = {'nombre_reaccion': nombre_reaccion}
            reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros=filtro_reaccion)

            # Convertir la reacción química a un DataFrame de pandas
            df_reaccion_quimica = pd.DataFrame.from_records([reaccion.__dict__ for reaccion in reaccion_quimica])
            print("Reacción química:", df_reaccion_quimica)

            # Mostrar la tabla de reacciones químicas
            self.mostrar_reaccion_tabla(reaccion_quimica)
        else:
            print("La columna 'nombre_reaccion' no existe en el DataFrame.")

        # Llamar a la función para graficar
        etiqueta_horizontal = "tiempo"
        etiqueta_vertical = "concentracion"
        titulo = "concentracion vs tiempo"
        componente = "reactivo_limitate"
        try:
            # Limpiar la figura por completo
            self.matplotlib_widget.canvas.figure.clf()
            # Crear un nuevo conjunto de ejes
            self.matplotlib_widget.ax = self.matplotlib_widget.canvas.figure.subplots()

            # Graficar los datos experimentales iniciales
            self.matplotlib_widget.funciones.graficar_datos_experimentales_iniciales(
                df_datos_cineticos_listos["tiempo"], 
                df_datos_cineticos_listos["concentracion"],
                etiqueta_horizontal, 
                etiqueta_vertical, 
                titulo, 
                componente, 
                grafico="MatplotlibWidget", 
                ax=self.matplotlib_widget.ax, 
                canvas=self.matplotlib_widget.canvas
            )

            # Configurar los límites y las etiquetas de los ejes
            self.matplotlib_widget.ax.set_xlim([df_datos_cineticos_listos["tiempo"].min(), df_datos_cineticos_listos["tiempo"].max()])
            self.matplotlib_widget.ax.set_ylim([df_datos_cineticos_listos["concentracion"].min(), df_datos_cineticos_listos["concentracion"].max()])
            self.matplotlib_widget.ax.set_xlabel(etiqueta_horizontal)
            self.matplotlib_widget.ax.set_ylabel(etiqueta_vertical)

            # Actualizar el gráfico
            self.matplotlib_widget.canvas.draw()
        except KeyError as e:
            print(f"Error: {e}. La columna no existe en el DataFrame.")
            
    def calcular_arrenius(self):
        filtros = {'nombre_data': self.registro_datos_box.currentText()}
        resultados= self.RegistroDataExperimentalManejador.consultar(filtros=filtros)
        if resultados:
            filtros_datos_salida= {'id_registro_data_experimental': resultados[0].id}
            resultados_a_ci = self.CondicionesInicialesManejador.consultar(filtros=filtros)
            df_resultados_a_ci = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_a_ci])
            print("Condiciones iniciales:", df_resultados_a_ci[['id', 'temperatura']])
            fitro_salida={'id_nombre_data': resultados[0].id,'id_condiciones_iniciales': df_resultados_a_ci["id"].to_string(index=False)}
            print(fitro_salida)
            resultados_ds = self.RegistroDatosSalidaManejador.consultar(filtros=fitro_salida)
            df_resultados_ds = pd.DataFrame.from_records([condicion.__dict__ for condicion in resultados_ds])
            print("Datos Salida:", df_resultados_ds)
            print("CI T :", df_resultados_a_ci['temperatura'])
            print("Datos Salida:", df_resultados_ds['constante_cinetica'])
            #return resultados[0].id, print(resultados[0].id)
            # Primero, resetea el índice de las Series para evitar problemas de alineación.
            temperatura_reset = df_resultados_a_ci['temperatura'].reset_index(drop=True)
            constante_cinetica_reset = df_resultados_ds['constante_cinetica'].reset_index(drop=True)

            # Luego, concatena las dos Series en un nuevo DataFrame.
            df_combinado = pd.concat([temperatura_reset, constante_cinetica_reset], axis=1)

            # Renombra las columnas del nuevo DataFrame para reflejar el contenido.
            df_combinado.columns = ['temperatura', 'constante_cinetica']

            # Finalmente, imprime el DataFrame combinado.
            print(df_combinado.to_string(index=False))
            
            #ejecutar modelo de 2 puntos
            # Para acceder a los valores de la primera fila (índice 0)
            temperatura_primera_fila = df_combinado.iloc[0]['temperatura']
            constante_cinetica_primera_fila = df_combinado.iloc[0]['constante_cinetica']

            # Para acceder a los valores de la segunda fila (índice 1)
            temperatura_segunda_fila = df_combinado.iloc[1]['temperatura']
            constante_cinetica_segunda_fila = df_combinado.iloc[1]['constante_cinetica']
            
            # Llamar a la función calcular_energia_activacion con los valores obtenidos
            #calcular_energia_activacion(k1, T1, k2, T2, escala_temp='K', unidades='J', R_custom=None)
            resultado = Funciones.calcular_energia_activacion(
                k1=constante_cinetica_primera_fila,
                T1=temperatura_primera_fila,
                k2=constante_cinetica_segunda_fila,
                T2=temperatura_segunda_fila,escala_temp='K', unidades='cal'
            )

            # Imprimir el resultado
            print("El resultado de la energía de activación es:", resultado)

            
            
        else:
            logging.warning(f"No se encontró un registro con el nombre: {self.registro_datos_box.currentText()}")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelDataAnalisis()
    window.show()
    sys.exit(app.exec())