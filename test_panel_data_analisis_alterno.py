import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
#from PyQt6.uic import loadUi
from PyQt6.uic import *
from models import *
from repository import *
import pandas as pd
import matplotlib.image as mpimg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from panel_data_analisis_alterno import Ui_MainWindow
from repository import *

from funciones import *
from modelos_metodo_integral import *


class PanelDataAnalisis(QMainWindow):
    def __init__(self):
        super(PanelDataAnalisis, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        #traer funciones
        self.funciones = Funciones()
        self.modelos_metodo_integral = MetodoIntegralGraficador()

        # Inicializar la variable para almacenar el DataFrame
        self.df_datos_cineticos_listos = None

    #elementos gráficos
    
        # Inicializar elementos gráficos
        self.init_ui_elements()

        # Cargar datos iniciales
        self.buscar_registros()
        self.buscar_dato()

    def init_ui_elements(self):
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
        self.registro_datos_box.currentIndexChanged.connect(self.actualizar_condiciones_iniciales)
        self.registro_datos_box.currentIndexChanged.connect(self.imprimir_registro_seleccionado)
        self.registro_datos_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)

        # Combobox de condiciones iniciales
        self.condiciones_iniciales_box = self.ui.condiciones_iniciales_box
        self.condiciones_iniciales_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)
        self.condiciones_iniciales_box.currentIndexChanged.connect(self.mostrar_condiciones_iniciales_en_tabla)
        
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
        

        # line edit de modelo de ajuste
        self.reactivo_limitante_inicial_edit = self.ui.reactivo_limitante_inicial_edit
        self.estimacion_inicial_k_edit = self.ui.estimacion_inicial_k_edit
        self.estimacion_inicial_n_edit = self.ui.estimacion_inicial_n_edit

        #boton de ejecutar modelo
        self.ejecutar_modelo_button = self.ui.pushButton_2
        self.ejecutar_modelo_button.clicked.connect(self.ejecutar_modelo)




    #funciones de consulta de registros    

    def buscar_registros(self):       
        registros = self.RegistroDataExperimentalManejador.consultar_registro()
        self.mostrar_registros(registros)
        
    def mostrar_registros(self, registros):
        self.registro_datos_box.clear()
        self.registro_datos_box.addItem("Todos")
        if registros:
            for registro in registros:
                self.registro_datos_box.addItem(registro.nombre_data, registro.id)
            self.actualizar_condiciones_iniciales()  # Update conditions for the first item
        else:
            QMessageBox.information(self, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)
            
    def actualizar_condiciones_iniciales(self):
        nombre_data = self.registro_datos_box.currentText()
        if nombre_data == "Todos":
            condiciones = self.CondicionesInicialesManejador.consultar_condicion()
        else:
            filtros = {'nombre_data': nombre_data}
            condiciones = self.CondicionesInicialesManejador.consultar_condicion(filtros=filtros)
        self.mostrar_condiciones_iniciales(condiciones)

    #funciones de consulta de condiciones iniciales

    def buscar_condiciones_iniciales(self):
        condiciones = self.CondicionesInicialesManejador.consultar_condicion()
        self.mostrar_condiciones_iniciales(condiciones) 

    def mostrar_condiciones_iniciales(self, condiciones):
        self.condiciones_iniciales_box.clear()
        self.condiciones_iniciales_box.addItem("Todos")
        if condiciones:
            for condicion in condiciones:
                self.condiciones_iniciales_box.addItem(condicion.nombre_data, condicion.id)
        else:
            QMessageBox.information(self, "No hay condiciones iniciales", "No se encontraron condiciones iniciales en la base de datos.", QMessageBox.StandardButton.Ok)
    
    def mostrar_condiciones_iniciales_en_tabla(self):
        nombre_data = self.registro_datos_box.currentText()
        condicion_inicial_id = self.condiciones_iniciales_box.currentData()

        filtros = {}
        if nombre_data and nombre_data != "Todos":
            filtros['nombre_data'] = nombre_data
        if condicion_inicial_id and condicion_inicial_id != "Todos":
            filtros['id'] = condicion_inicial_id

        condiciones = self.CondicionesInicialesManejador.consultar_condicion(filtros=filtros)
        self.mostrar_condiciones_iniciales_tabla(condiciones)

    def mostrar_condiciones_iniciales_tabla(self, condiciones):
        self.tabla = self.condiciones_iniciales_tabla
        if condiciones:
            self.tabla.setRowCount(len(condiciones))
            self.tabla.setColumnCount(10)

            for fila, condicion in enumerate(condiciones):
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(condicion.id)))
                self.tabla.setItem(fila, 1, QTableWidgetItem(str(condicion.temperatura)))
                self.tabla.setItem(fila, 2, QTableWidgetItem(str(condicion.tiempo)))
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(condicion.presion_total)))
                self.tabla.setItem(fila, 4, QTableWidgetItem(str(condicion.presion_parcial)))
                self.tabla.setItem(fila, 5, QTableWidgetItem(str(condicion.fraccion_molar)))
                self.tabla.setItem(fila, 6, QTableWidgetItem(condicion.especie_quimica))
                self.tabla.setItem(fila, 7, QTableWidgetItem(condicion.tipo_especie))
                self.tabla.setItem(fila, 8, QTableWidgetItem(condicion.detalle))
                self.tabla.setItem(fila, 9, QTableWidgetItem(condicion.nombre_data))
        else:
            self.tabla.setRowCount(0)
            QMessageBox.information(self, "No hay condiciones iniciales", "No se encontraron condiciones iniciales en la base de datos.", QMessageBox.StandardButton.Ok)

# organizar en otra clase

    
    def buscar_dato(self):


        datos_resultados = self.DatosCineticosManejador.consultar_datos()
        self.mostrar_datos_tabla(datos_resultados)

    def mostrar_datos_tabla(self, resultados):
            self.datos_cineticos_tabla.clearContents()
            self.datos_cineticos_tabla.setRowCount(0)
            if resultados:
                self.datos_cineticos_tabla.setRowCount(len(resultados))
                self.datos_cineticos_tabla.setColumnCount(10)
                for fila, dato in enumerate(resultados):
                    self.datos_cineticos_tabla.setItem(fila, 0, QTableWidgetItem(str(dato.id)))
                    self.datos_cineticos_tabla.setItem(fila, 1, QTableWidgetItem(str(dato.tiempo)))
                    self.datos_cineticos_tabla.setItem(fila, 2, QTableWidgetItem(str(dato.concentracion)))
                    self.datos_cineticos_tabla.setItem(fila, 3, QTableWidgetItem(str(dato.otra_propiedad)))
                    self.datos_cineticos_tabla.setItem(fila, 4, QTableWidgetItem(str(dato.conversion_reactivo_limitante)))
                    self.datos_cineticos_tabla.setItem(fila, 5, QTableWidgetItem(dato.tipo_especie))
                    self.datos_cineticos_tabla.setItem(fila, 6, QTableWidgetItem(str(dato.id_condiciones_iniciales)))
                    self.datos_cineticos_tabla.setItem(fila, 7, QTableWidgetItem(dato.nombre_data))
                    self.datos_cineticos_tabla.setItem(fila, 8, QTableWidgetItem(dato.nombre_reaccion))
                    self.datos_cineticos_tabla.setItem(fila, 9, QTableWidgetItem(dato.especie_quimica))
            else:
                QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)
    
    def mostrar_reaccion_tabla(self, resultados):
        tabla = self.reaccion_quimica_tabla
        tabla.clearContents()
        tabla.setRowCount(0)
        if resultados:
            tabla.setRowCount(len(resultados))
            tabla.setColumnCount(7)
            for fila, dato in enumerate(resultados):
                tabla.setItem(fila, 0, QTableWidgetItem(str(dato.id)))
                tabla.setItem(fila, 1, QTableWidgetItem(str(dato.especie_quimica)))
                tabla.setItem(fila, 2, QTableWidgetItem(str(dato.formula)))
                tabla.setItem(fila, 3, QTableWidgetItem(str(dato.coeficiente_estequiometrico)))
                tabla.setItem(fila, 4, QTableWidgetItem(str(dato.detalle)))
                tabla.setItem(fila, 5, QTableWidgetItem(str(dato.tipo_especie)))
                tabla.setItem(fila, 6, QTableWidgetItem(str(dato.nombre_reaccion)))
        else:
            QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)

    def actualizar_datos_cineticos(self):
            nombre_data = self.registro_datos_box.currentText()
            condicion_inicial_id = self.condiciones_iniciales_box.currentData()

            filtros = {}
            if nombre_data and nombre_data != "Todos":
                filtros['nombre_data'] = nombre_data
            if condicion_inicial_id and condicion_inicial_id != "Todos":
                filtros['id_condiciones_iniciales'] = condicion_inicial_id

            datos_cineticos = self.DatosCineticosManejador.consultar_datos(filtros=filtros)
            self.mostrar_datos_tabla(datos_cineticos)

    def imprimir_registro_seleccionado(self):
        self.actualizar_datos_cineticos()
        nombre_data = self.registro_datos_box.currentText()

        if not nombre_data:
            return

        filtros = {'nombre_data': nombre_data}
        condiciones = self.CondicionesInicialesManejador.consultar_condicion(filtros=filtros)

        # Convertir las condiciones a un DataFrame de pandas
        df_condiciones_iniciales = pd.DataFrame.from_records([condicion.__dict__ for condicion in condiciones])
        print(df_condiciones_iniciales)

        datos_cineticos = self.DatosCineticosManejador.consultar_datos(filtros=filtros)
        # Convertir los datos a un DataFrame de pandas
        df_datos_cineticos_listos = pd.DataFrame.from_records([dato.__dict__ for dato in datos_cineticos])
        print(df_datos_cineticos_listos)
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
            reaccion_quimica = self.ReaccionQuimicaManejador.consultar_reaccion(filtros=filtro_reaccion)

            # Convertir la reacción química a un DataFrame de pandas
            df_reaccion_quimica = pd.DataFrame.from_records([reaccion.__dict__ for reaccion in reaccion_quimica])
            print(df_reaccion_quimica)

            # Mostrar la tabla de reacciones químicas
            self.mostrar_reaccion_tabla(reaccion_quimica)
        else:
            print("La columna 'nombre_reaccion' no existe en el DataFrame.")

            # Llamar al manejador para seleccionar el modelo
            #index = self.ajustar_modelo_box.currentIndex()
            #self.manejador_seleccion_modelo(index, df_datos_cineticos_listos)

        # Llamar a la función para graficar
           
        etiqueta_horizontal="tiempo"
        etiqueta_vertical="concentracion"
        titulo="concentracion vs tiempo"
        componente="reactivo_limitate"
        try:
            # Limpiar la figura por completo
            self.matplotlib_widget.canvas.figure.clf()
            # Crear un nuevo conjunto de ejes
            self.matplotlib_widget.ax = self.matplotlib_widget.canvas.figure.subplots()

            self.matplotlib_widget.funciones.graficar_datos_experimentales_iniciales(df_datos_cineticos_listos["tiempo"], df_datos_cineticos_listos["concentracion"],
                                                etiqueta_horizontal, etiqueta_vertical, titulo, componente, grafico="MatplotlibWidget", ax=self.matplotlib_widget.ax, canvas=self.matplotlib_widget.canvas)
            # Configurar los límites y las etiquetas de los ejes
            self.matplotlib_widget.ax.set_xlim([df_datos_cineticos_listos["tiempo"].min(), df_datos_cineticos_listos["tiempo"].max()])
            self.matplotlib_widget.ax.set_ylim([df_datos_cineticos_listos["concentracion"].min(), df_datos_cineticos_listos["concentracion"].max()])
            self.matplotlib_widget.ax.set_xlabel(etiqueta_horizontal)
            self.matplotlib_widget.ax.set_ylabel(etiqueta_vertical)

            # Actualizar el gráfico
            self.matplotlib_widget.canvas.draw()
        except KeyError as e:
            print(f"Error: {e}. La columna no existe en el DataFrame.")

        # Llamar a manejador_seleccion_modelo


    def mostrar_metodos_ajustador(self):
        self.ajustar_modelo_box.clear()
        self.ajustar_modelo_box.addItem("Modelos cinéticos")
        metodos = [metodo for metodo in dir(MetodoIntegralAjustador) if callable(getattr(MetodoIntegralAjustador, metodo)) and not metodo.startswith("__")]
        for metodo in metodos:
            self.ajustar_modelo_box.addItem(metodo)

    # Maneja la selección del modelo de ajuste
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

            print(resultado)
            # Ahora, graficamos el modelo utilizando los resultados obtenidos
          

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ejecutar el modelo: {str(e)}", QMessageBox.StandardButton.Ok)
            
    def ejecutar_modelo(self):
        index = self.ajustar_modelo_box.currentIndex()
        #self.manejador_seleccion_modelo(index, self.df_datos_cineticos_listos)
        self.manejador_seleccion_modelo(index)



        
        
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
