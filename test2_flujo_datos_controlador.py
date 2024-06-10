import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from modelos import *
from repositorios import *
import logging
from datetime import datetime
import json
import os
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(__file__))

#importe ui de la ventana principal
from flujo_datos_vista import Ui_MainWindow
from funciones import *


# metodos comunes
from servicios import *

class FlujoDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # Crear instancias de los manejadores de la base de datos
        self.manejadores_base()

        # Crear un atajo para la tecla F5
        shortcut = QShortcut(QKeySequence.StandardKey.Refresh, self)
        shortcut.activated.connect(self.refrescar_datos_tabla)        
        
        # Inicializar elementos de la UI
        self.init_ui_elementos_dc()
        self.init_ui_elementos_rde()
        self.init_ui_elementos_ci()
        self.init_ui_elementos_rq()

        # Inicializar conexiones de señales y ranuras
        self.init_control_botones_datos()
        self.init_control_botones_experimental()
        self.init_control_botones_ci()
        self.init_control_botones_rq()

        # Cargar datos iniciales
        self.buscar_dato()
        self.buscar_registros()
        self.buscar_condiciones_iniciales()
        self.buscar_reaccion_quimica()

         # Conectar la señal cellChanged para actualizar la base de datos cuando cambie una celda
        self.tabla_datos.cellChanged.connect(self.actualizar_valor_celda_datos)
        self.tabla_registro_data_experimental.cellChanged.connect(self.actualizar_valor_celda_registro)
        self.tabla_condiciones_iniciales.cellChanged.connect(self.actualizar_valor_celda_ci)
        self.tabla_reaccion_quimica.cellChanged.connect(self.actualizar_valor_celda_reaccion)

        #iniciar funciones diferentes a crud
        self.establecer_fecha_sistema()

        json_tipo_especie = r"data\tipo_especie.json"

        self.cargar_datos_json(json_tipo_especie)


    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()     

        #self.metodos_comunes = MetodosComunesControlador()
        self.metodos_comunes = Servicios(self)
        self.funciones=Funciones()

    def init_ui_elementos_dc(self):
        # Datos cinéticos
        self.tiempo = self.ui.tiempo_dc_edit
        self.concentracion = self.ui.concentracion_dc_edit
        self.otra_propiedad = self.ui.otra_propiedad_dc_edit
        self.conversion_reactivo_limitante = self.ui.conversion_reactivo_limitante_dc_edit
        self.tipo_especie = self.ui.tipo_especie_dc_edit
        self.id_condiciones_iniciales = self.ui.id_condiciones_iniciales_dc_edit
        #nombre_data_general_edit
        self.nombre_data = self.ui.nombre_data_general_edit
        #nombre_reaccion_dc_edit
        #self.nombre_data = self.ui.nombre_data_dc_edit
        #nombre_reaccion_dc_edit
        #self.nombre_reaccion = self.ui.nombre_reaccion_dc_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_general_edit
        self.especie_quimica = self.ui.especie_quimica_dc_edit

        # Botones de datos cinéticos
        self.agregar_dc_btn = self.ui.agregar_dc_btn
        self.actualizar_dc_btn = self.ui.actualizar_dc_btn
        self.seleccionar_dc_btn = self.ui.seleccionar_dc_btn
        self.buscar_dc_btn = self.ui.buscar_dc_btn
        self.limpiar_dc_btn = self.ui.limpiar_dc_btn
        self.borrar_dc_btn = self.ui.borrar_dc_btn

        # Tabla de datos cinéticos
        self.tabla_datos = self.ui.datos_cineticos_tabla
        self.tabla_datos.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_dc.findChildren(QPushButton)

        #objetos test
        self.calculo1=self.ui.marcar_a0_btn
        self.calculo0=self.ui.marcar_producto0_btn
        self.calculo2=self.ui.marcar_coeficiente_producto_btn
        self.calculo3=self.ui.marcar_coeficiente_reactivo_btn
        self.calculo4=self.ui.calcular_xa
        self.calculo5=self.ui.calcular_a

        self.coeficiente_estequiometro_producto = self.ui.coeficiente_estequiometrico_producto_edit
        self.coeficiente_estequiometro_reactivo = self.ui.coeficiente_estequiometrico_reactivo_edit
        self.concentracion_inicial_reactivo_limitante = self.ui.concentracion_reactivo_limitante_edit
        self.concentracion_inicial_producto = self.ui.concentracion_producto_edit



    def init_ui_elementos_rde(self):
        # Datos experimentales
        #nombre_data_rde_edit
        #self.nombre_data_experimental = self.ui.nombre_data_rde_edit
        #nombre_data_general_edit
        self.nombre_data_experimental = self.ui.nombre_data_general_edit
        self.fecha_data_experimental = self.ui.fecha_rde_edit
        self.detalle_data_experimental = self.ui.detalle_rde_edit

        # Botones de datos experimentales
        self.agregar_rde_btn = self.ui.agregar_rde_btn
        self.actualizar_rde_btn = self.ui.actualizar_rde_btn
        self.seleccionar_rde_btn = self.ui.seleccionar_rde_btn
        self.buscar_rde_btn = self.ui.buscar_rde_btn
        self.limpiar_rde_btn = self.ui.limpiar_rde_btn
        self.borrar_rde_btn = self.ui.borrar_rde_btn

        # Tabla de datos experimentales
        self.tabla_registro_data_experimental = self.ui.registro_data_experimental_tabla
        self.tabla_registro_data_experimental.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_rde.findChildren(QPushButton)

    def init_ui_elementos_ci(self):
        # Condiciones iniciales
        self.temperatura_ci = self.ui.temperatura_ci_edit
        self.tiempo_ci = self.ui.tiempo_ci_edit
        self.presion_total_ci = self.ui.presion_total_ci_edit
        self.presion_parcial_ci = self.ui.presion_parcial_ci_edit
        self.fraccion_molar_ci = self.ui.fraccion_molar_ci_edit
        self.especie_quimica_ci = self.ui.especie_quimica_ci_edit
        self.tipo_especie_ci = self.ui.tipo_especie_ci_edit
        self.detalle_ci = self.ui.detalle_ci_edit
        #nombre_data_ci_edit
        #self.nombre_data_ci = self.ui.nombre_data_ci_edit
        #nombre_data
        self.nombre_data_ci = self.ui.nombre_data_general_edit
        


        # Botones de condiciones iniciales
        self.agregar_ci_btn = self.ui.agregar_ci_btn
        self.actualizar_ci_btn = self.ui.actualizar_ci_btn
        self.seleccionar_ci_btn = self.ui.seleccionar_ci_btn
        self.buscar_ci_btn = self.ui.buscar_ci_btn
        self.limpiar_ci_btn = self.ui.limpiar_ci_btn
        self.borrar_ci_btn = self.ui.borrar_ci_btn

        # Tabla de condiciones iniciales
        self.tabla_condiciones_iniciales = self.ui.condiciones_iniciales_tabla
        self.tabla_condiciones_iniciales.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_ci.findChildren(QPushButton)
    
    def init_ui_elementos_rq(self):
        # Reacción química
        self.especie_quimica_rq = self.ui.especie_quimica_rq_edit
        self.formula_rq = self.ui.formula_rq_edit
        self.coeficiente_estequiometro_rq = self.ui.coeficiente_estequiometrico_rq_edit
        self.detalle_rq = self.ui.detalle_rq_edit
        self.tipo_especie_rq = self.ui.tipo_especie_rq_edit
        #nombre_data_general_edit
        self.nombre_reaccion_rq = self.ui.nombre_reaccion_general_edit
        #nombre_reaccion_rq_edit
        #self.nombre_reaccion_rq = self.ui.nombre_reaccion_rq_edit

        # Botones de reacción química
        self.agregar_rq_btn = self.ui.agregar_rq_btn
        self.actualizar_rq_btn = self.ui.actualizar_rq_btn
        self.seleccionar_rq_btn = self.ui.seleccionar_rq_btn
        self.buscar_rq_btn = self.ui.buscar_rq_btn
        self.limpiar_rq_btn = self.ui.limpiar_rq_btn
        self.borrar_rq_btn = self.ui.borrar_rq_btn

        # Tabla de reacción química
        self.tabla_reaccion_quimica = self.ui.reaccion_quimica_tabla
        self.tabla_reaccion_quimica.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_rq.findChildren(QPushButton)

        #combo box
        self.tipo_especie_rq_box=self.ui.tipo_especie_rq_box
        self.tipo_especie_rq_box.currentIndexChanged.connect(self.actualizar_lineedit)

    

    def init_control_botones_datos(self):
        # Conectar los botones a sus respectivas funciones
        # Datos cinéticos
        self.agregar_dc_btn.clicked.connect(self.agregar_dato)
        self.actualizar_dc_btn.clicked.connect(self.actualizar_dato)
        self.seleccionar_dc_btn.clicked.connect(self.seleccionar_dato)
        self.borrar_dc_btn.clicked.connect(self.borrar_dato)
        self.limpiar_dc_btn.clicked.connect(self.limpiar_formulario)
        self.buscar_dc_btn.clicked.connect(self.buscar_dato)

        self.calculo0.clicked.connect(self.marcar_quimico_inicial)
        self.calculo1.clicked.connect(self.marcar_quimico_inicial)
        self.calculo2.clicked.connect(self.marcar_coeficiente)
        self.calculo3.clicked.connect(self.marcar_coeficiente)
        self.calculo4.clicked.connect(self.calcular_conversion_reactivo_limitante_dado_producto)
        self.calculo5.clicked.connect(self.calcular_concentracion_reactivo_limitante_dado_conversion)

    def init_control_botones_experimental(self):
        self.agregar_rde_btn.clicked.connect(self.agregar_registro_data_experimental)
        self.actualizar_rde_btn.clicked.connect(self.actualizar_registro_data_experimental)
        self.seleccionar_rde_btn.clicked.connect(self.seleccionar_registro_data_experimental)
        self.borrar_rde_btn.clicked.connect(self.borrar_registro_data_experimental)
        self.limpiar_rde_btn.clicked.connect(self.limpiar_formulario_registro_data_experimental)
        self.buscar_rde_btn.clicked.connect(self.buscar_registros)

    def init_control_botones_ci(self):
        self.agregar_ci_btn.clicked.connect(self.agregar_condiciones_iniciales)
        self.actualizar_ci_btn.clicked.connect(self.actualizar_condiciones_iniciales)
        self.seleccionar_ci_btn.clicked.connect(self.seleccionar_condiciones_iniciales)
        self.borrar_ci_btn.clicked.connect(self.borrar_condiciones_iniciales)
        self.limpiar_ci_btn.clicked.connect(self.limpiar_formulario_ci)
        self.buscar_ci_btn.clicked.connect(self.buscar_condiciones_iniciales)   

    def init_control_botones_rq(self):
        self.agregar_rq_btn.clicked.connect(self.agregar_reaccion_quimica)
        self.actualizar_rq_btn.clicked.connect(self.actualizar_reaccion_quimica)
        self.seleccionar_rq_btn.clicked.connect(self.seleccionar_reaccion_quimica)
        self.borrar_rq_btn.clicked.connect(self.borrar_reaccion_quimica)
        self.limpiar_rq_btn.clicked.connect(self.limpiar_formulario_rq)
        self.buscar_rq_btn.clicked.connect(self.buscar_reaccion_quimica) 


    def refrescar_datos_tabla(self):
        # Limpiar la tabla
        self.tabla_datos.clearContents()
        self.tabla_registro_data_experimental.clearContents()
        self.tabla_condiciones_iniciales.clearContents()
        self.tabla_reaccion_quimica.clearContents()
                
        # Buscar los datos nuevamente y mostrarlos en la tabla
        self.buscar_dato()
        self.buscar_registros()
        self.buscar_condiciones_iniciales()
        self.buscar_reaccion_quimica()

    #metodos para desactivar y activar botones
    def boton_desactivado(self):
        for button in self.lista_botones:
            button.setDisabled(True)

    def boton_activado(self):
        for button in self.lista_botones:
            button.setDisabled(False)
    
    #metodos para crud de datos cineticos

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
            #print("Intentando agregar dato:", dato)
            agregar_resultado = self.DatosCineticosManejador.agregar_dato(dato)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario()
                self.buscar_dato()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar los datos ", QMessageBox.StandardButton.Ok)

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
            nuevo_dato = {
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
            actualizar_resultado = self.DatosCineticosManejador.actualizar_dato(id, nuevo_dato)

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
    

    def mostrar_datos_tabla(self, resultados):
        if resultados:
            self.tabla_datos.setRowCount(len(resultados))
            self.tabla_datos.setColumnCount(10)

            for fila, dato in enumerate(resultados):
                self.tabla_datos.setItem(fila, 0, QTableWidgetItem(str(dato.id)))
                self.tabla_datos.setItem(fila, 1, QTableWidgetItem(str(dato.tiempo)))
                self.tabla_datos.setItem(fila, 2, QTableWidgetItem(str(dato.concentracion)))
                self.tabla_datos.setItem(fila, 3, QTableWidgetItem(str(dato.otra_propiedad)))
                self.tabla_datos.setItem(fila, 4, QTableWidgetItem(str(dato.conversion_reactivo_limitante)))
                self.tabla_datos.setItem(fila, 5, QTableWidgetItem(dato.tipo_especie))
                self.tabla_datos.setItem(fila, 6, QTableWidgetItem(str(dato.id_condiciones_iniciales)))
                self.tabla_datos.setItem(fila, 7, QTableWidgetItem(dato.nombre_data))
                self.tabla_datos.setItem(fila, 8, QTableWidgetItem(dato.nombre_reaccion))
                self.tabla_datos.setItem(fila, 9, QTableWidgetItem(dato.especie_quimica))
        else:
            self.tabla_datos.setRowCount(0)
            QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)


    def actualizar_valor_celda_datos(self, fila, columna):
        try:
            item = self.tabla_datos.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return

            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return

            # Verificar si la celda debe contener un número y convertirla
            header_text = self.tabla_datos.horizontalHeaderItem(columna).text().lower()
            if header_text in ['tiempo', 'concentracion', 'otra_propiedad', 'conversion_reactivo_limitante']:
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return

            # Obtener el ID del dato a actualizar
            id_item = self.tabla_datos.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return

            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            new_dato = {header_text: nuevo_valor}

            # Intentar actualizar el dato en la base de datos
            if self.DatosCineticosManejador.actualizar_dato(id, new_dato):
                logging.info(f"Dato con ID {id} actualizado correctamente")
            else:
                logging.error(f"No se pudo actualizar el dato con ID {id}")

        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)


    # funciones crud para registro de data experimental
    # Registro de data experimental
    def mostrar_registros(self, registros):
        self.metodos_comunes.mostrar_registros(self.tabla_registro_data_experimental, registros)

    def agregar_registro_data_experimental(self):
        self.boton_desactivado()

        # Validar que todos los campos estén llenos
        try:
            nombre_data = self.nombre_data_experimental.text()
            fecha = self.fecha_data_experimental.text()
            detalle = self.detalle_data_experimental.text()

            if not nombre_data or not fecha or not detalle:
                raise ValueError("Todos los campos de texto deben estar llenos")

        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return

        # Crear el objeto RegistroDataExperimental
        registro = RegistroDataExperimental(
            nombre_data=nombre_data,
            fecha=fecha,
            detalle=detalle,
        )

        # Intentar agregar el registro a la base de datos
        try:
            print("Intentando agregar registro:", registro)
            agregar_resultado = self.RegistroDataExperimentalManejador.agregar_registro(registro)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Registro agregado correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_registro_data_experimental()
                self.buscar_registros()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar el registro", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar el registro: {e}", QMessageBox.StandardButton.Ok)

        self.boton_activado()

    
    def limpiar_formulario_registro_data_experimental(self):
        self.nombre_data_experimental.clear()
        self.fecha_data_experimental.clear()
        self.detalle_data_experimental.clear()
    
    def seleccionar_registro_data_experimental(self):
        seleccionar_fila = self.tabla_registro_data_experimental.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_registro_data_experimental.item(seleccionar_fila, 0).text().strip()
            nombre_data = self.tabla_registro_data_experimental.item(seleccionar_fila, 1).text().strip()
            fecha = self.tabla_registro_data_experimental.item(seleccionar_fila, 2).text().strip()
            detalle = self.tabla_registro_data_experimental.item(seleccionar_fila, 3).text().strip()

            self.nombre_data_experimental.setText(nombre_data)
            self.fecha_data_experimental.setText(fecha)
            self.detalle_data_experimental.setText(detalle)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
        
    def actualizar_registro_data_experimental(self):
        self.boton_desactivado()
        try:
            # Obtener el ID del registro seleccionado
            fila_seleccionada = self.tabla_registro_data_experimental.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return

            id = int(self.tabla_registro_data_experimental.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            nombre_data = self.nombre_data_experimental.text()
            fecha = self.fecha_data_experimental.text()
            detalle = self.detalle_data_experimental.text()

            if not nombre_data or not fecha or not detalle:
                raise ValueError("Todos los campos de texto deben estar llenos")

            # Crear el objeto de registro actualizado
            nuevo_registro = {
                "nombre_data": nombre_data,
                "fecha": fecha,
                "detalle": detalle,
            }

            # Intentar actualizar el registro en la base de datos
            actualizar_resultado = self.RegistroDataExperimentalManejador.actualizar_registro(id, nuevo_registro)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Registro actualizado correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_registro_data_experimental()
                self.buscar_registros()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar el registro", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)
        
        except Exception as e:
            logging.error("Error al actualizar el registro: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el registro: {e}", QMessageBox.StandardButton.Ok)
        
        finally:
            self.boton_activado()

    def actualizar_valor_celda_registro(self, fila, columna):
        try:
            item = self.tabla_registro_data_experimental.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return

            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return

            # Verificar si la celda debe contener un número y convertirla
            header_text = self.tabla_registro_data_experimental.horizontalHeaderItem(columna).text().lower()
            if header_text in ['nombre_data', 'fecha', 'detalle']:
                try:
                    nuevo_valor = str(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return

            # Obtener el ID del registro a actualizar
            id_item = self.tabla_registro_data_experimental.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return

            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            new_registro = {header_text: nuevo_valor}

            # Intentar actualizar el registro en la base de datos
            if self.RegistroDataExperimentalManejador.actualizar_registro(id, new_registro):
                logging.info(f"Registro con ID {id} actualizado correctamente")
            else:
                logging.error(f"No se pudo actualizar el registro con ID {id}")

        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)

    def borrar_registro_data_experimental(self):
        fila_seleccionada = self.tabla_registro_data_experimental.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar registro", "¿Estás seguro de eliminar el registro?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_registro_data_experimental.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.RegistroDataExperimentalManejador.borrar_registro(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Registro eliminado correctamente", QMessageBox.StandardButton.Ok)
                    self.RegistroDataExperimentalManejador.consultar_registro()
                    self.buscar_registros()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar el registro", QMessageBox.StandardButton.Ok)

    def buscar_registros(self):
        filtros = {
            "nombre_data": self.nombre_data_experimental.text(),
            "fecha": self.fecha_data_experimental.text(),
            "detalle": self.detalle_data_experimental.text(),
        }
        registros = self.RegistroDataExperimentalManejador.consultar_registro(filtros, "like")
        self.mostrar_registros(registros)    

    # funciones crud para condiciones iniciales
    # Condiciones iniciales
    def mostrar_condiciones_iniciales(self, condiciones_iniciales):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.tabla_condiciones_iniciales, condiciones_iniciales)
    
    def agregar_condiciones_iniciales(self):
        self.boton_desactivado()

        # Validar que todos los campos estén llenos
        try:
            temperatura = self.temperatura_ci.text()
            tiempo = self.tiempo_ci.text()
            presion_total = self.presion_total_ci.text()
            presion_parcial = self.presion_parcial_ci.text()
            fraccion_molar = self.fraccion_molar_ci.text()
            especie_quimica = self.especie_quimica_ci.text()
            tipo_especie = self.tipo_especie_ci.text()
            detalle = self.detalle_ci.text()
            nombre_data = self.nombre_data_ci.text()

            if not temperatura or not tiempo or not presion_total or not presion_parcial or not fraccion_molar or not especie_quimica or not tipo_especie or not detalle or not nombre_data:
                raise ValueError("Todos los campos de texto deben estar llenos")
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return
        # Crear el objeto CondicionesIniciales
        condiciones_iniciales = CondicionesIniciales(
            temperatura=temperatura,
            tiempo=tiempo,
            presion_total=presion_total,
            presion_parcial=presion_parcial,
            fraccion_molar=fraccion_molar,
            especie_quimica=especie_quimica,
            tipo_especie=tipo_especie,
            detalle=detalle,
            nombre_data=nombre_data,
        )

        # Intentar agregar las condiciones iniciales a la base de datos
        try:
            print("Intentando agregar condiciones iniciales:", condiciones_iniciales)
            agregar_resultado = self.CondicionesInicialesManejador.agregar_condicion(condiciones_iniciales)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Condiciones iniciales agregadas correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_ci()
                self.buscar_condiciones_iniciales()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar las condiciones iniciales", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar las condiciones iniciales: {e}", QMessageBox.StandardButton.Ok)
        
        self.boton_activado()

    def limpiar_formulario_ci(self):
        self.temperatura_ci.clear()
        self.tiempo_ci.clear()
        self.presion_total_ci.clear()
        self.presion_parcial_ci.clear()
        self.fraccion_molar_ci.clear()
        self.especie_quimica_ci.clear()
        self.tipo_especie_ci.clear()
        self.detalle_ci.clear()
        self.nombre_data_ci.clear()
    
    def seleccionar_condiciones_iniciales(self):
        seleccionar_fila = self.tabla_condiciones_iniciales.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_condiciones_iniciales.item(seleccionar_fila, 0).text().strip()
            temperatura = self.tabla_condiciones_iniciales.item(seleccionar_fila, 1).text().strip()
            tiempo = self.tabla_condiciones_iniciales.item(seleccionar_fila, 2).text().strip()
            presion_total = self.tabla_condiciones_iniciales.item(seleccionar_fila, 3).text().strip()
            presion_parcial = self.tabla_condiciones_iniciales.item(seleccionar_fila, 4).text().strip()
            fraccion_molar = self.tabla_condiciones_iniciales.item(seleccionar_fila, 5).text().strip()
            especie_quimica = self.tabla_condiciones_iniciales.item(seleccionar_fila, 6).text().strip()
            tipo_especie = self.tabla_condiciones_iniciales.item(seleccionar_fila, 7).text().strip()
            detalle = self.tabla_condiciones_iniciales.item(seleccionar_fila, 8).text().strip()
            nombre_data = self.tabla_condiciones_iniciales.item(seleccionar_fila, 9).text().strip()

            self.temperatura_ci.setText(temperatura)
            self.tiempo_ci.setText(tiempo)
            self.presion_total_ci.setText(presion_total)
            self.presion_parcial_ci.setText(presion_parcial)
            self.fraccion_molar_ci.setText(fraccion_molar)
            self.especie_quimica_ci.setText(especie_quimica)
            self.tipo_especie_ci.setText(tipo_especie)
            self.detalle_ci.setText(detalle)
            self.nombre_data_ci.setText(nombre_data)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    def actualizar_condiciones_iniciales(self):
        self.boton_desactivado()
        try:
            # Obtener el ID de las condiciones iniciales seleccionadas
            fila_seleccionada = self.tabla_condiciones_iniciales.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return
            id = int(self.tabla_condiciones_iniciales.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            temperatura = self.temperatura_ci.text()
            tiempo = self.tiempo_ci.text()
            presion_total = self.presion_total_ci.text()
            presion_parcial = self.presion_parcial_ci.text()
            fraccion_molar = self.fraccion_molar_ci.text()
            especie_quimica = self.especie_quimica_ci.text()
            tipo_especie = self.tipo_especie_ci.text()
            detalle = self.detalle_ci.text()
            nombre_data = self.nombre_data_ci.text()

            if not temperatura or not tiempo or not presion_total or not presion_parcial or not fraccion_molar or not especie_quimica or not tipo_especie or not detalle or not nombre_data:
                raise ValueError("Todos los campos de texto deben estar llenos")
            
            # Crear el objeto de condiciones iniciales actualizadas
            nuevas_condiciones_iniciales = {
                "temperatura": temperatura,
                "tiempo": tiempo,
                "presion_total": presion_total,
                "presion_parcial": presion_parcial,
                "fraccion_molar": fraccion_molar,
                "especie_quimica": especie_quimica,
                "tipo_especie": tipo_especie,
                "detalle": detalle,
                "nombre_data": nombre_data,
            }

            # Intentar actualizar las condiciones iniciales en la base de datos
            actualizar_resultado = self.CondicionesInicialesManejador.actualizar_condicion(id, nuevas_condiciones_iniciales)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Condiciones iniciales actualizadas correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_ci()
                self.buscar_condiciones_iniciales()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar las condiciones iniciales", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al actualizar las condiciones iniciales: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar las condiciones iniciales: {e}", QMessageBox.StandardButton.Ok)

        finally:
            self.boton_activado()

    def actualizar_valor_celda_ci(self, fila, columna):
        try:
            item = self.tabla_condiciones_iniciales.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return

            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return

            # Verificar si la celda debe contener un número y convertirla
            header_text = self.tabla_condiciones_iniciales.horizontalHeaderItem(columna).text().lower()
            if header_text in ['temperatura', 'tiempo', 'presion_total', 'presion_parcial', 'fraccion_molar']:
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return

            # Obtener el ID de las condiciones iniciales a actualizar
            id_item = self.tabla_condiciones_iniciales.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return

            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            new_condiciones_iniciales = {header_text: nuevo_valor}

            # Intentar actualizar las condiciones iniciales en la base de datos
            if self.CondicionesInicialesManejador.actualizar_condicion(id, new_condiciones_iniciales):
                logging.info(f"Condiciones iniciales con ID {id} actualizadas correctamente")
            else:
                logging.error(f"No se pudo actualizar las condiciones iniciales con ID {id}")

        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)
    
    def borrar_condiciones_iniciales(self):
        fila_seleccionada = self.tabla_condiciones_iniciales.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar condiciones iniciales", "¿Estás seguro de eliminar las condiciones iniciales?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_condiciones_iniciales.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.CondicionesInicialesManejador.borrar_condicion(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Condiciones iniciales eliminadas correctamente", QMessageBox.StandardButton.Ok)
                    self.CondicionesInicialesManejador.consultar_condicion()
                    self.buscar_condiciones_iniciales()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar las condiciones iniciales", QMessageBox.StandardButton.Ok)
    
    def buscar_condiciones_iniciales(self):
        filtros = {
            "temperatura": self.temperatura_ci.text(),
            "tiempo": self.tiempo_ci.text(),
            "presion_total": self.presion_total_ci.text(),
            "presion_parcial": self.presion_parcial_ci.text(),
            "fraccion_molar": self.fraccion_molar_ci.text(),
            "especie_quimica": self.especie_quimica_ci.text(),
            "tipo_especie": self.tipo_especie_ci.text(),
            "detalle": self.detalle_ci.text(),
            "nombre_data": self.nombre_data_ci.text(),
        }
        condiciones_iniciales = self.CondicionesInicialesManejador.consultar_condicion(filtros, "like")
        self.mostrar_condiciones_iniciales(condiciones_iniciales)
    
    # funciones crud para reaccion quimica
    # Reacción química
    def mostrar_reaccion_quimica(self, reaccion_quimica):
        self.metodos_comunes.mostrar_reacciones(self.tabla_reaccion_quimica, reaccion_quimica)
    
    def agregar_reaccion_quimica(self):
        self.boton_desactivado()

        # Validar que todos los campos estén llenos
        try:
            especie_quimica = self.especie_quimica_rq.text()
            formula = self.formula_rq.text()
            coeficiente_estequiometrico = self.coeficiente_estequiometro_rq.text()
            detalle = self.detalle_rq.text()
            tipo_especie = self.tipo_especie_rq.text()
            nombre_reaccion = self.nombre_reaccion_rq.text()

            if not especie_quimica or not formula or not coeficiente_estequiometrico or not detalle or not tipo_especie or not nombre_reaccion:
                raise ValueError("Todos los campos de texto deben estar llenos")
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return
        # Crear el objeto ReaccionQuimica
        reaccion_quimica = ReaccionQuimica(
            especie_quimica=especie_quimica,
            formula=formula,
            coeficiente_estequiometrico=coeficiente_estequiometrico,
            detalle=detalle,
            tipo_especie=tipo_especie,
            nombre_reaccion=nombre_reaccion,
        )

        # Intentar agregar la reacción química a la base de datos
        try:
            print("Intentando agregar reacción química:", reaccion_quimica)
            agregar_resultado = self.ReaccionQuimicaManejador.agregar_reaccion(reaccion_quimica)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Reacción química agregada correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_rq()
                self.buscar_reaccion_quimica()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar la reacción química", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar la reacción química: {e}", QMessageBox.StandardButton.Ok)
        
        self.boton_activado()

    def limpiar_formulario_rq(self):
        self.especie_quimica_rq.clear()
        self.formula_rq.clear()
        self.coeficiente_estequiometro_rq.clear()
        self.detalle_rq.clear()
        self.tipo_especie_rq.clear()
        self.nombre_reaccion_rq.clear()
    
    def seleccionar_reaccion_quimica(self):
        seleccionar_fila = self.tabla_reaccion_quimica.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_reaccion_quimica.item(seleccionar_fila, 0).text().strip()
            especie_quimica = self.tabla_reaccion_quimica.item(seleccionar_fila, 1).text().strip()
            formula = self.tabla_reaccion_quimica.item(seleccionar_fila, 2).text().strip()
            coeficiente_estequiometrico = self.tabla_reaccion_quimica.item(seleccionar_fila, 3).text().strip()
            detalle = self.tabla_reaccion_quimica.item(seleccionar_fila, 4).text().strip()
            tipo_especie = self.tabla_reaccion_quimica.item(seleccionar_fila, 5).text().strip()
            nombre_reaccion = self.tabla_reaccion_quimica.item(seleccionar_fila, 6).text().strip()

            self.especie_quimica_rq.setText(especie_quimica)
            self.formula_rq.setText(formula)
            self.coeficiente_estequiometro_rq.setText(coeficiente_estequiometrico)
            self.detalle_rq.setText(detalle)
            self.tipo_especie_rq.setText(tipo_especie)
            self.nombre_reaccion_rq.setText(nombre_reaccion)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    
    def actualizar_reaccion_quimica(self):
        self.boton_desactivado()
        try:
            # Obtener el ID de la reacción química seleccionada
            fila_seleccionada = self.tabla_reaccion_quimica.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return
            id = int(self.tabla_reaccion_quimica.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            especie_quimica = self.especie_quimica_rq.text()
            formula = self.formula_rq.text()
            coeficiente_estequiometrico = self.coeficiente_estequiometro_rq.text()
            detalle = self.detalle_rq.text()
            tipo_especie = self.tipo_especie_rq.text()
            nombre_reaccion = self.nombre_reaccion_rq.text()

            if not especie_quimica or not formula or not coeficiente_estequiometrico or not detalle or not tipo_especie or not nombre_reaccion:
                raise ValueError("Todos los campos de texto deben estar llenos")
        
            # Crear el objeto de reacción química actualizada
            nueva_reaccion_quimica = {
                "especie_quimica": especie_quimica,
                "formula": formula,
                "coeficiente_estequiometrico": coeficiente_estequiometrico,
                "detalle": detalle,
                "tipo_especie": tipo_especie,
                "nombre_reaccion": nombre_reaccion,
            }

            # Intentar actualizar la reacción química en la base de datos
            actualizar_resultado = self.ReaccionQuimicaManejador.actualizar_reaccion(id, nueva_reaccion_quimica)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Reacción química actualizada correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_rq()
                self.buscar_reaccion_quimica()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar la reacción química", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al actualizar la reacción química: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar la reacción química: {e}", QMessageBox.StandardButton.Ok)

        finally:
            self.boton_activado()

    def actualizar_valor_celda_reaccion(self, fila, columna):
        try:
            item = self.tabla_reaccion_quimica.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return
            
            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return
            
            # Verificar si la celda debe contener un número y convertirla
            header_text = self.tabla_reaccion_quimica.horizontalHeaderItem(columna).text().lower()
            if header_text in ['coeficiente_estequiometrico']:
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return
                
            # Obtener el ID de la reacción química a actualizar
            id_item = self.tabla_reaccion_quimica.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return
            
            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            new_reaccion_quimica = {header_text: nuevo_valor}

            # Intentar actualizar la reacción química en la base de datos
            if self.ReaccionQuimicaManejador.actualizar_reaccion(id, new_reaccion_quimica):
                logging.info(f"Reacción química con ID {id} actualizada correctamente")
            else:
                logging.error(f"No se pudo actualizar la reacción química con ID {id}")

        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)

    def borrar_reaccion_quimica(self):
        fila_seleccionada = self.tabla_reaccion_quimica.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar reacción química", "¿Estás seguro de eliminar la reacción química?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_reaccion_quimica.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.ReaccionQuimicaManejador.borrar_reaccion(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Reacción química eliminada correctamente", QMessageBox.StandardButton.Ok)
                    self.ReaccionQuimicaManejador.consultar_reaccion()
                    self.buscar_reaccion_quimica()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar la reacción química", QMessageBox.StandardButton.Ok)
        
    def buscar_reaccion_quimica(self):
        filtros = {
            "especie_quimica": self.especie_quimica_rq.text(),
            "formula": self.formula_rq.text(),
            "coeficiente_estequiometrico": self.coeficiente_estequiometro_rq.text(),
            "detalle": self.detalle_rq.text(),
            "tipo_especie": self.tipo_especie_rq.text(),
            "nombre_reaccion": self.nombre_reaccion_rq.text(),
        }
        reaccion_quimica = self.ReaccionQuimicaManejador.consultar_reaccion(filtros, "like")
        self.mostrar_reaccion_quimica(reaccion_quimica)

    # funciones especiales para datos
    def establecer_fecha_sistema(self):
        # Obtener la fecha actual del sistema
        fecha_actual = datetime.now().date()

        # Convertir la fecha a una cadena en el formato dd/mm/yyyy
        fecha_str = fecha_actual.strftime("%d/%m/%Y")

        # Establecer la fecha en fecha_rde_edit
        self.ui.fecha_rde_edit.setText(fecha_str)

        # Asignar fecha_rde_edit a fecha_data_experimental
        self.fecha_data_experimental = self.ui.fecha_rde_edit

    def mostrar_tipo_especie(self, catalogo):
        self.tipo_especie_rq_box.clear()
        self.tipo_especie_rq_box.addItem("Seleccione una opción", -1)
        if catalogo:
            for item in catalogo:
                self.tipo_especie_rq_box.addItem(item["Descripcion"], item["ID"])
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en el archivo JSON.", QMessageBox.StandardButton.Ok)

    def cargar_datos_json(self, archivo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self.mostrar_tipo_especie(data.get("Tipo_especie_catalogo", []))
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"No se encontró el archivo {archivo}", QMessageBox.StandardButton.Ok)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", f"Error al leer el archivo {archivo}", QMessageBox.StandardButton.Ok)
    
    def actualizar_lineedit(self):
        current_text = self.tipo_especie_rq_box.currentText()
        if current_text != "Seleccione una opción":
            self.tipo_especie_rq.setText(current_text)
        else:
            self.tipo_especie_rq.clear()

    
    def marcar_quimico_inicial(self):
        # Definir los filtros para la consulta

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

            if tipo_especie == "producto":
                self.concentracion_inicial_producto.setText(concentracion)
            else:
                self.concentracion_inicial_reactivo_limitante.setText(concentracion)

        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
        
        seleccion_quimico_inicial = {
            "tiempo": [self.tiempo.text()],
            "concentracion": [self.concentracion.text()],
            "otra_propiedad": [self.otra_propiedad.text()],
            "conversion_reactivo_limitante": [self.conversion_reactivo_limitante.text()],
            "tipo_especie": [self.tipo_especie.text()],
            "id_condiciones_iniciales": [self.id_condiciones_iniciales.text()],
            "nombre_data": [self.nombre_data.text()],
            "nombre_reaccion": [self.nombre_reaccion.text()],
            "especie_quimica": [self.especie_quimica.text()],
        }

        self.seleccion_quimico_inicial = pd.DataFrame.from_dict(seleccion_quimico_inicial)
        print(self.seleccion_quimico_inicial)
        return self.seleccion_quimico_inicial
    
    def marcar_coeficiente(self):
        seleccionar_fila = self.tabla_reaccion_quimica.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_reaccion_quimica.item(seleccionar_fila, 0).text().strip()
            especie_quimica = self.tabla_reaccion_quimica.item(seleccionar_fila, 1).text().strip()
            formula = self.tabla_reaccion_quimica.item(seleccionar_fila, 2).text().strip()
            coeficiente_estequiometrico = self.tabla_reaccion_quimica.item(seleccionar_fila, 3).text().strip()
            detalle = self.tabla_reaccion_quimica.item(seleccionar_fila, 4).text().strip()
            tipo_especie = self.tabla_reaccion_quimica.item(seleccionar_fila, 5).text().strip()
            nombre_reaccion = self.tabla_reaccion_quimica.item(seleccionar_fila, 6).text().strip()

            if tipo_especie == "producto":
                self.coeficiente_estequiometro_producto.setText(coeficiente_estequiometrico)
            else:
                self.coeficiente_estequiometro_reactivo.setText(coeficiente_estequiometrico)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
        
        seleccion_reaccion_quimica = {
            "especie_quimica": [self.especie_quimica_rq.text()],
            "formula": [self.formula_rq.text()],
            "coeficiente_estequiometrico": [self.coeficiente_estequiometro_rq.text()],
            "detalle": [self.detalle_rq.text()],
            "tipo_especie": [self.tipo_especie_rq.text()],
            "nombre_reaccion": [self.nombre_reaccion_rq.text()],
        }

        print(seleccion_reaccion_quimica)


    def calcular_conversion_reactivo_limitante_dado_producto(self):
        funciones=Funciones()
        concentracion = float(self.concentracion.text())
        concentracion_inicial_producto = float(self.concentracion_inicial_producto.text())
        concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
        coeficiente_estequiometro_producto = float(self.coeficiente_estequiometro_producto.text())
        coeficiente_estequiometro_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
        xa=funciones.conversion_reactivo_limitante_dado_producto(concentracion, concentracion_inicial_producto, concentracion_inicial_reactivo_limitante, coeficiente_estequiometro_producto, coeficiente_estequiometro_reactivo)
        print(xa)
        self.conversion_reactivo_limitante.setText(str(xa))

    def calcular_concentracion_reactivo_limitante_dado_conversion(self):
        funciones=Funciones()
        concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
        conversion_reactivo_limitante =float(self.conversion_reactivo_limitante.text())
        A=funciones.concentracion_reactivo_funcion_conversion(concentracion_inicial_reactivo_limitante,conversion_reactivo_limitante)
        print(A)
        self.concentracion.setText(str(A))






    #calcular despues
    def calculo_delta_n(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlujoDatos()
    window.show()
    sys.exit(app.exec())