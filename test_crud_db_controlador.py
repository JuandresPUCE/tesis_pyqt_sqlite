import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from models import *
from repository import *
import logging

#importe ui de la ventana principal
from crud_db_vista import Ui_MainWindow

# metodos comunes
from funciones_comunes_controlador import *

class PantallaCrud(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Crear instancias de los manejadores de la base de datos
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()     
        # metodos comunes refactorizados
        self.metodos_comunes = MetodosComunesControlador()

        # Crear un atajo para la tecla F5
        shortcut = QShortcut(QKeySequence.StandardKey.Refresh, self)
        shortcut.activated.connect(self.refrescar_datos_tabla)        
        
        # elementos para datos cinéticos

        # UI elements
        self.tiempo = self.ui.tiempo_dc_edit
        self.concentracion = self.ui.concentracion_dc_edit
        self.otra_propiedad = self.ui.otra_propiedad_dc_edit
        self.conversion_reactivo_limitante = self.ui.conversion_reactivo_limitante_dc_edit
        self.tipo_especie = self.ui.tipo_especie_dc_edit
        self.id_condiciones_iniciales = self.ui.id_condiciones_iniciales_dc_edit
        self.nombre_data = self.ui.nombre_data_dc_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_dc_edit
        self.especie_quimica = self.ui.especie_quimica_dc_edit

        # Buttons
        self.agregar_dc_btn = self.ui.agregar_dc_btn
        self.actualizar_dc_btn = self.ui.actualizar_dc_btn
        self.seleccionar_dc_btn = self.ui.seleccionar_dc_btn
        self.buscar_dc_btn = self.ui.buscar_dc_btn
        self.limpiar_dc_btn = self.ui.limpiar_dc_btn
        self.borrar_dc_btn = self.ui.borrar_dc_btn

        # Table
        self.tabla_datos = self.ui.datos_cineticos_tabla
        self.tabla_datos.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame.findChildren(QPushButton)

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Load initial data
        #cargo los datos de la tabla de datos cinéticos
        self.buscar_dato()

        # Conectar la señal cellChanged para actualizar la base de datos cuando cambie una celda
        self.tabla_datos.cellChanged.connect(self.actualizar_valor_celda)

        # elementos para registro de data experimental
        #campos editables
        self.nombre_data_experimental = self.ui.nombre_data_rde_edit
        self.fecha_data_experimental = self.ui.fecha_rde_edit
        self.detalle_data_experimental = self.ui.detalle_rde_edit
        #botones
        self.agregar_rde_btn = self.ui.agregar_rde_btn
        self.actualizar_rde_btn = self.ui.actualizar_rde_btn
        self.seleccionar_rde_btn = self.ui.seleccionar_rde_btn
        self.buscar_rde_btn = self.ui.buscar_rde_btn
        self.limpiar_rde_btn = self.ui.limpiar_rde_btn
        self.borrar_rde_btn = self.ui.borrar_rde_btn
        #tabla
        self.tabla_registro_data_experimental = self.ui.registro_data_experimental_tabla
                #cargar los datos de la tabla de registro de data experimental
        self.buscar_registros()




    def init_signal_slot(self):
        # Conectar los botones a sus respectivas funciones
        # Datos cinéticos
        self.agregar_dc_btn.clicked.connect(self.agregar_dato)
        self.actualizar_dc_btn.clicked.connect(self.actualizar_dato)
        self.seleccionar_dc_btn.clicked.connect(self.seleccionar_dato)
        self.borrar_dc_btn.clicked.connect(self.borrar_dato)
        self.limpiar_dc_btn.clicked.connect(self.limpiar_formulario)
        self.buscar_dc_btn.clicked.connect(self.buscar_dato)
        
        # Registro de data experimental
        #self.agregar_rde_btn.clicked.connect(self.agregar_data_experimental)
        #self.actualizar_rde_btn.clicked.connect(self.actualizar_data_experimental)
        #self.seleccionar_rde_btn.clicked.connect(self.seleccionar_data_experimental)
        #self.borrar_rde_btn.clicked.connect(self.borrar_data_experimental)
        #self.limpiar_rde_btn.clicked.connect(self.limpiar_formulario_data_experimental)
        #self.buscar_rde_btn.clicked.connect(self.buscar_data_experimental)



    def refrescar_datos_tabla(self):
        # Limpiar la tabla
        self.tabla_datos.clearContents()
        
        # Buscar los datos nuevamente y mostrarlos en la tabla
        self.buscar_dato()

    def agregar_dato(self):
        self.boton_desactivado()

        # Validar que todos los campos estén llenos
        try:
            tiempo = float(self.tiempo.text())
            concentracion = float(self.concentracion.text())
            otra_propiedad = float(self.otra_propiedad.text())
            conversion_reactivo_limitante = float(self.conversion_reactivo_limitante.text())
            tipo_especie = self.tipo_especie.text()
            id_condiciones_iniciales = int(self.id_condiciones_iniciales.text())
            nombre_data = self.nombre_data.text()
            nombre_reaccion = self.nombre_reaccion.text()
            especie_quimica = self.especie_quimica.text()

            if not tipo_especie or not nombre_data or not nombre_reaccion or not especie_quimica:
                raise ValueError("Todos los campos de texto deben estar llenos")

        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return

        # Crear el objeto DatosIngresadosCineticos
        dato = DatosIngresadosCineticos(
            tiempo=tiempo,
            concentracion=concentracion,
            otra_propiedad=otra_propiedad,
            conversion_reactivo_limitante=conversion_reactivo_limitante,
            tipo_especie=tipo_especie,
            id_condiciones_iniciales=id_condiciones_iniciales,
            nombre_data=nombre_data,
            nombre_reaccion=nombre_reaccion,
            especie_quimica=especie_quimica,
        )

        # Intentar agregar el dato a la base de datos
        try:
            agregar_resultado = self.DatosCineticosManejador.agregar_dato(dato)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario()
                self.buscar_dato()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar los datos", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos: {e}", QMessageBox.StandardButton.Ok)

        self.boton_activado()

    def limpiar_formulario(self):
        # Limpiar formulario
        self.tiempo.clear()
        self.concentracion.clear()
        self.otra_propiedad.clear()
        self.conversion_reactivo_limitante.clear()
        self.tipo_especie.clear()
        self.id_condiciones_iniciales.clear()
        self.nombre_data.clear()
        self.nombre_reaccion.clear()
        self.especie_quimica.clear()

    def seleccionar_dato(self):
        seleccionar_fila = self.tabla_datos.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_datos.item(seleccionar_fila, 0).text().strip()
            tiempo = self.tabla_datos.item(seleccionar_fila, 1).text().strip()
            concentracion = self.tabla_datos.item(seleccionar_fila, 2).text().strip()
            otra_propiedad = self.tabla_datos.item(seleccionar_fila, 3).text().strip()
            conversion_reactivo_limitante = self.tabla_datos.item(seleccionar_fila, 4).text().strip()
            tipo_especie = self.tabla_datos.item(seleccionar_fila, 5).text().strip()
            id_condiciones_iniciales = self.tabla_datos.item(seleccionar_fila, 6).text().strip()
            nombre_data = self.tabla_datos.item(seleccionar_fila, 7).text().strip()
            nombre_reaccion = self.tabla_datos.item(seleccionar_fila, 8).text().strip()
            especie_quimica = self.tabla_datos.item(seleccionar_fila, 9).text().strip()

            self.tiempo.setText(tiempo)
            self.concentracion.setText(concentracion)
            self.otra_propiedad.setText(otra_propiedad)
            self.conversion_reactivo_limitante.setText(conversion_reactivo_limitante)
            self.tipo_especie.setText(tipo_especie)
            self.id_condiciones_iniciales.setText(id_condiciones_iniciales)
            self.nombre_data.setText(nombre_data)
            self.nombre_reaccion.setText(nombre_reaccion)
            self.especie_quimica.setText(especie_quimica)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return

    def actualizar_dato(self):
        self.boton_desactivado()

        try:
            # Obtener el ID del dato seleccionado
            fila_seleccionada = self.tabla_datos.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return

            id = int(self.tabla_datos.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            tiempo = float(self.tiempo.text())
            concentracion = float(self.concentracion.text())
            otra_propiedad = float(self.otra_propiedad.text())
            conversion_reactivo_limitante = float(self.conversion_reactivo_limitante.text())
            tipo_especie = self.tipo_especie.text()
            id_condiciones_iniciales = int(self.id_condiciones_iniciales.text())
            nombre_data = self.nombre_data.text()
            nombre_reaccion = self.nombre_reaccion.text()
            especie_quimica = self.especie_quimica.text()

            if not tipo_especie or not nombre_data or not nombre_reaccion or not especie_quimica:
                raise ValueError("Todos los campos de texto deben estar llenos")

            # Crear el objeto de datos actualizado
            new_dato = {
                "tiempo": tiempo,
                "concentracion": concentracion,
                "otra_propiedad": otra_propiedad,
                "conversion_reactivo_limitante": conversion_reactivo_limitante,
                "tipo_especie": tipo_especie,
                "id_condiciones_iniciales": id_condiciones_iniciales,
                "nombre_data": nombre_data,
                "nombre_reaccion": nombre_reaccion,
                "especie_quimica": especie_quimica,
            }

            # Intentar actualizar el dato en la base de datos
            actualizar_resultado = self.DatosCineticosManejador.actualizar_dato(id, new_dato)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Datos actualizados correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario()
                self.buscar_dato()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar los datos", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)
        
        except Exception as e:
            logging.error("Error al actualizar los datos: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar los datos: {e}", QMessageBox.StandardButton.Ok)
        
        finally:
            self.boton_activado()


    def borrar_dato(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar dato", "¿Estás seguro de eliminar el dato?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.DatosCineticosManejador.borrar_dato(id)
                if borrar_resultado:
                    
                    QMessageBox.information(self, "Información", "Dato eliminado correctamente", QMessageBox.StandardButton.Ok)
                    self.DatosCineticosManejador.consultar_datos()
                    self.refrescar_datos_tabla() 
                    self.buscar_dato()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar el dato", QMessageBox.StandardButton.Ok)

    def buscar_dato(self):
        filtros = {
            "tiempo": self.tiempo.text(),
            "concentracion": self.concentracion.text(),
            "otra_propiedad": self.otra_propiedad.text(),
            "conversion_reactivo_limitante": self.conversion_reactivo_limitante.text(),
            "tipo_especie": self.tipo_especie.text(),
            "id_condiciones_iniciales": self.id_condiciones_iniciales.text(),
            "nombre_data": self.nombre_data.text(),
            "nombre_reaccion": self.nombre_reaccion.text(),
            "especie_quimica": self.especie_quimica.text(),
        }

        datos_resultados = self.DatosCineticosManejador.consultar_datos(filtros,"like")
        self.mostrar_datos_tabla(datos_resultados)
    

    def boton_desactivado(self):
        for button in self.lista_botones:
            button.setDisabled(True)

    def boton_activado(self):
        for button in self.lista_botones:
            button.setDisabled(False)

    def mostrar_datos_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

    def actualizar_valor_celda(self, fila, columna):
        item = self.tabla_datos.item(fila, columna)
        if item is not None:
            nuevo_valor = item.text()
            # Verificar si la cadena es vacía
            if nuevo_valor != '':
                try:
                    # Intentar convertir la cadena a un número de punto flotante
                    nuevo_valor_float = float(nuevo_valor)
                except ValueError:
                    # Manejar el caso donde la cadena no se puede convertir a un número de punto flotante
                    print("Error: el valor ingresado no es un número válido.")
                    return
            else:
                # No se actualiza la base de datos si la cadena es vacía
                print("Error: el valor ingresado está vacío.")
                return

            # Resto de la lógica para actualizar la base de datos
            id = int(self.tabla_datos.item(fila, 0).text())
            item_nombre_data = self.tabla_datos.item(fila, 7)
            if item_nombre_data is not None:
                nombre_data = item_nombre_data.text()
                new_dato = {self.tabla_datos.horizontalHeaderItem(columna).text(): nuevo_valor}
                self.DatosCineticosManejador.actualizar_dato(id, new_dato)
            else:
                print("La celda de nombre de datos está vacía")
        else:
            print("La celda está vacía o fuera de los límites de la tabla")

    # funciones crud para registro de data experimental
    # Registro de data experimental
    def mostrar_registros(self, registros):
        self.metodos_comunes.mostrar_registros(self.tabla_registro_data_experimental, registros)

    def buscar_registros(self):
        filtros = {
            "nombre_data": self.nombre_data_experimental.text(),
            "fecha": self.fecha_data_experimental.text(),
            "detalle": self.detalle_data_experimental.text(),
        }
        registros = self.RegistroDataExperimentalManejador.consultar_registro(filtros, "like")
        self.mostrar_registros(registros)    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PantallaCrud()
    window.show()
    sys.exit(app.exec())
