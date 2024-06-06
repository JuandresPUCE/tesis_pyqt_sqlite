from PyQt6.QtWidgets import *

class Servicios:
    def __init__(self, parent=None):
        self.parent = parent
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
                    self.tabla.setItem(fila, 5, QTableWidgetItem(str(dato.tipo_especie)))
                    self.tabla.setItem(fila, 6, QTableWidgetItem(str(dato.id_condiciones_iniciales)))
                    self.tabla.setItem(fila, 7, QTableWidgetItem(str(dato.nombre_data)))
                    self.tabla.setItem(fila, 8, QTableWidgetItem(str(dato.nombre_reaccion)))
                    self.tabla.setItem(fila, 9, QTableWidgetItem(str(dato.especie_quimica)))
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
            QMessageBox.information(self.parent, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)

    def mostrar_condiciones_iniciales(self, condiciones_iniciales_tabla, condiciones):
        self.tabla = condiciones_iniciales_tabla
        self.tabla.clearContents()
        self.tabla.setRowCount(0)
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
            QMessageBox.information(self.parent, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)
    
    def mostrar_reacciones(self, reacciones_tabla, reacciones):
        self.tabla = reacciones_tabla
        self.tabla.clearContents()
        self.tabla.setRowCount(0)
        if reacciones:
            self.tabla.setRowCount(len(reacciones))
            self.tabla.setColumnCount(7)

            for fila, reaccion in enumerate(reacciones):
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(reaccion.id)))
                self.tabla.setItem(fila, 1, QTableWidgetItem(str(reaccion.especie_quimica)))
                self.tabla.setItem(fila, 2, QTableWidgetItem(str(reaccion.formula)))
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(reaccion.coeficiente_estequiometrico)))
                self.tabla.setItem(fila, 4, QTableWidgetItem(str(reaccion.detalle)))
                self.tabla.setItem(fila, 5, QTableWidgetItem(str(reaccion.tipo_especie)))
                self.tabla.setItem(fila, 6, QTableWidgetItem(str(reaccion.nombre_reaccion)))
        else:
            self.tabla.setRowCount(0)
            QMessageBox.information(self.parent, "No hay registros", "No se encontraron registros en la base de datos.", QMessageBox.StandardButton.Ok)