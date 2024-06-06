import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import loadUi
from modelos import *
from repositorios import *


from panel_data_analisis import Ui_MainWindow
from repositorios import *




class PanelDataAnalisis(QMainWindow):
    def __init__(self):
        super(PanelDataAnalisis, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()


    #elementos gráficos
    
        #tabla registro datos experimentales
        self.registro_datos_tabla= self.ui.registro_datos_tabla
        self.registro_datos_tabla.setSortingEnabled(False)
        # consulta de registros al seleccionar
        self.registro_datos_tabla.cellClicked.connect(self.imprimir_registro_seleccionado)
    
        # consulta de registros
        self.buscar_registros()

        #tabla de condiciones iniciales
        self.condiciones_iniciales_tabla = self.ui.condiciones_iniciales_tabla
        self.condiciones_iniciales_tabla.setSortingEnabled(False)
        # consulta de condiciones iniciales
        self.buscar_condiciones_iniciales()

        #tabla de datos cineticos
        self.datos_cineticos_tabla = self.ui.datos_cineticos_tabla
        self.datos_cineticos_tabla.setSortingEnabled(False)
        # consulta de datos cineticos
        self.buscar_dato()
        




    #funciones de consulta de registros    

    def buscar_registros(self):       
        registros = self.RegistroDataExperimentalManejador.consultar_registro()
        self.mostrar_registros(registros)
    
    def mostrar_registros(self, registros):
        if registros:
            self.registro_datos_tabla.setRowCount(len(registros))
            self.registro_datos_tabla.setColumnCount(4)

            for fila, registro in enumerate(registros):
                self.registro_datos_tabla.setItem(fila, 0, QTableWidgetItem(str(registro.id)))
                self.registro_datos_tabla.setItem(fila, 1, QTableWidgetItem(registro.nombre_data))
                self.registro_datos_tabla.setItem(fila, 2, QTableWidgetItem(registro.fecha))
                self.registro_datos_tabla.setItem(fila, 3, QTableWidgetItem(registro.detalle))
        else:
            self.registro_datos_tabla.setRowCount(0)
            QMessageBox.information(self, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)


    #funciones de consulta de condiciones iniciales

    def buscar_condiciones_iniciales(self):
        condiciones = self.CondicionesInicialesManejador.consultar_condicion()
        self.mostrar_condiciones_iniciales(condiciones) 

    def mostrar_condiciones_iniciales(self, condiciones):
        if condiciones:
            self.condiciones_iniciales_tabla.setRowCount(len(condiciones))
            self.condiciones_iniciales_tabla.setColumnCount(10)

            for fila, condicion in enumerate(condiciones):
                self.condiciones_iniciales_tabla.setItem(fila, 0, QTableWidgetItem(str(condicion.id)))
                self.condiciones_iniciales_tabla.setItem(fila, 1, QTableWidgetItem(str(condicion.temperatura)))
                self.condiciones_iniciales_tabla.setItem(fila, 2, QTableWidgetItem(str(condicion.tiempo)))
                self.condiciones_iniciales_tabla.setItem(fila, 3, QTableWidgetItem(str(condicion.presion_total)))
                self.condiciones_iniciales_tabla.setItem(fila, 4, QTableWidgetItem(str(condicion.presion_parcial)))
                self.condiciones_iniciales_tabla.setItem(fila, 5, QTableWidgetItem(str(condicion.fraccion_molar)))
                self.condiciones_iniciales_tabla.setItem(fila, 6, QTableWidgetItem(condicion.especie_quimica))
                self.condiciones_iniciales_tabla.setItem(fila, 7, QTableWidgetItem(condicion.tipo_especie))
                self.condiciones_iniciales_tabla.setItem(fila, 8, QTableWidgetItem(condicion.detalle))
                self.condiciones_iniciales_tabla.setItem(fila, 9, QTableWidgetItem(condicion.nombre_data))
        else:
            self.condiciones_iniciales_tabla.setRowCount(0)
            QMessageBox.information(self, "No hay condiciones iniciales", "No se encontraron condiciones iniciales en la base de datos.", QMessageBox.StandardButton.Ok)

# organizar en otra clase

    
    def buscar_dato(self):


        datos_resultados = self.DatosCineticosManejador.consultar_datos()
        self.mostrar_datos_tabla(datos_resultados)

    def mostrar_datos_tabla(self, resultados):
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
            self.datos_cineticos_tabla.setRowCount(0)
            QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)

    #manipulaciones
    def imprimir_registro_seleccionado(self, fila, columna):
        # Obtener los datos de cada columna en la fila activada
        datos_fila = [self.registro_datos_tabla.item(fila, i).text() for i in range(self.registro_datos_tabla.columnCount())]

        # Imprimir los datos en la consola
        print(datos_fila)
        # Obtener el nombre_data de la fila seleccionada
        nombre_data = datos_fila[1]

        # Crear los filtros
        filtros = {'nombre_data': nombre_data}

        # Consultar las condiciones iniciales

        condiciones = self.CondicionesInicialesManejador.consultar_condicion(filtros=filtros)

        # Imprimir las condiciones
        for condicion in condiciones:
            print("\n -start-", condicion,"\n -end-")

            # Consultar los datos cinéticos
        datos_cineticos = self.DatosCineticosManejador.consultar_datos(filtros=filtros)

        # Imprimir los datos cinéticos
        for dato in datos_cineticos:
            print("\n -start-", dato,"\n -end-")
    
    

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelDataAnalisis()
    window.show()
    sys.exit(app.exec())
