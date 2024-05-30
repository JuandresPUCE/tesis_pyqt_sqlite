import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import loadUi
from models import *
from repository import *
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from panel_data_analisis_alterno import Ui_MainWindow
from repository import *

from funciones import *


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

        # Combobox de registro datos experimentales
        self.registro_datos_box = self.ui.registro_datos_box
        self.registro_datos_box.currentIndexChanged.connect(self.actualizar_condiciones_iniciales)
        self.registro_datos_box.currentIndexChanged.connect(self.imprimir_registro_seleccionado)
        self.registro_datos_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)

        # Combobox de condiciones iniciales
        self.condiciones_iniciales_box = self.ui.condiciones_iniciales_box
        self.condiciones_iniciales_box.currentIndexChanged.connect(self.actualizar_datos_cineticos)
        
        # Crear un widget para el gráfico de Matplotlib
        self.matplotlib_widget = MatplotlibWidget(self)

        # Agregar el widget de Matplotlib al QVBoxLayout vista_grafica
        self.ui.vista_grafica.addWidget(self.matplotlib_widget)





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
        self.ax.plot([1, 2, 3, 4], [10, 20, 25, 30])

        # Agregar el lienzo al diseño del widget
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout) 

           


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelDataAnalisis()
    window.show()
    sys.exit(app.exec())