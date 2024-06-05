from PyQt6.QtWidgets import *

class MetodosComunesControlador:
    def __init__(self):
        self.mensaje = "Metodos comunes del controlador"

    def mostrar_mensaje(self):
        print(self.mensaje)

    def mostrar_datos_tabla(self, tabla_datos_cineticos, resultados):
            self.tabla = tabla_datos_cineticos
            self.tabla.clearContents()
            self.tabla.setRowCount(0)
            if resultados:
                self.tabla.setRowCount(len(resultados))
                self.tabla.setColumnCount(10)
                for fila, dato in enumerate(resultados):
                    self.tabla.setItem(fila, 0, QTableWidgetItem(str(dato.id)))
                    self.tabla.setItem(fila, 1, QTableWidgetItem(str(dato.tiempo)))
                    self.tabla.setItem(fila, 2, QTableWidgetItem(str(dato.concentracion)))
                    self.tabla.setItem(fila, 3, QTableWidgetItem(str(dato.otra_propiedad)))
                    self.tabla.setItem(fila, 4, QTableWidgetItem(str(dato.conversion_reactivo_limitante)))
                    self.tabla.setItem(fila, 5, QTableWidgetItem(dato.tipo_especie))
                    self.tabla.setItem(fila, 6, QTableWidgetItem(str(dato.id_condiciones_iniciales)))
                    self.tabla.setItem(fila, 7, QTableWidgetItem(dato.nombre_data))
                    self.tabla.setItem(fila, 8, QTableWidgetItem(dato.nombre_reaccion))
                    self.tabla.setItem(fila, 9, QTableWidgetItem(dato.especie_quimica))
            else:
                QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)
    
    def mostrar_registros(self,registro_datos_tabla, registros):
        self.tabla = registro_datos_tabla
        if registros:
            self.tabla.setRowCount(len(registros))
            self.tabla.setColumnCount(4)

            for fila, registro in enumerate(registros):
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(registro.id)))
                self.tabla.setItem(fila, 1, QTableWidgetItem(registro.nombre_data))
                self.tabla.setItem(fila, 2, QTableWidgetItem(registro.fecha))
                self.tabla.setItem(fila, 3, QTableWidgetItem(registro.detalle))
        else:
            self.tabla.setRowCount(0)
            QMessageBox.information(self, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)
        