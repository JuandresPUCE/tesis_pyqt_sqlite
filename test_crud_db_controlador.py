import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from modelos import *
from repositorios import *
import logging

#importe ui de la ventana principal
from crud_db_vista import Ui_MainWindow

# metodos comunes
from servicios import *

class PantallaCrud(QMainWindow):
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
        self.init_ui_elementos_u()
        self.init_ui_elementos_ds()

        # Inicializar conexiones de señales y ranuras
        self.init_control_botones_datos()
        self.init_control_botones_experimental()
        self.init_control_botones_ci()
        self.init_control_botones_rq()
        self.init_control_botones_u()
        self.init_control_botones_ds()

        # Cargar datos iniciales
        self.buscar_dato()
        self.buscar_registros()
        self.buscar_condiciones_iniciales()
        self.buscar_reaccion_quimica()
        self.buscar_unidades()
        self.buscar_datos_salida()


         # Conectar la señal cellChanged para actualizar la base de datos cuando cambie una celda
        self.tabla_datos.cellChanged.connect(self.actualizar_valor_celda_datos)
        self.tabla_registro_data_experimental.cellChanged.connect(self.actualizar_valor_celda_registro)
        self.tabla_condiciones_iniciales.cellChanged.connect(self.actualizar_valor_celda_ci)
        self.tabla_reaccion_quimica.cellChanged.connect(self.actualizar_valor_celda_reaccion)
        self.tabla_registro_unidades.cellChanged.connect(self.actualizar_valor_celda_unidades)
        self.tabla_datos_salida.cellChanged.connect(self.actualizar_valor_celda_datos_salida)

    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()           

        self.metodos_comunes = Servicios(self)

    def init_ui_elementos_dc(self):
        # Datos cinéticos
        self.tiempo = self.ui.tiempo_dc_edit
        self.concentracion = self.ui.concentracion_dc_edit
        self.otra_propiedad = self.ui.otra_propiedad_dc_edit
        self.conversion_reactivo_limitante = self.ui.conversion_reactivo_limitante_dc_edit
        self.tipo_especie = self.ui.tipo_especie_dc_edit
        self.id_condiciones_iniciales = self.ui.id_condiciones_iniciales_dc_edit
        self.nombre_data = self.ui.nombre_data_dc_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_dc_edit
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

    def init_ui_elementos_rde(self):
        # Datos experimentales
        self.nombre_data_experimental = self.ui.nombre_data_rde_edit
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
        self.nombre_data_ci = self.ui.nombre_data_ci_edit


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
        self.tabla_condiciones_iniciales.setColumnWidth(0, 10)  # Establece el ancho de la primera columna a 100
        self.tabla_condiciones_iniciales.setColumnWidth(1, 10)  # Establece el ancho de la primera columna a 100
        #self.tabla_condiciones_iniciales.resizeColumnToContents(1)

        self.tabla_condiciones_iniciales.resizeColumnToContents(3)
        self.tabla_condiciones_iniciales.resizeColumnToContents(4)
        
        self.lista_botones = self.ui.funciones_frame_ci.findChildren(QPushButton)
    
    def init_ui_elementos_rq(self):
        # Reacción química
        self.especie_quimica_rq = self.ui.especie_quimica_rq_edit
        self.formula_rq = self.ui.formula_rq_edit
        self.coeficiente_estequiometro_rq = self.ui.coeficiente_estequiometrico_rq_edit
        self.detalle_rq = self.ui.detalle_rq_edit
        self.tipo_especie_rq = self.ui.tipo_especie_rq_edit
        self.nombre_reaccion_rq = self.ui.nombre_reaccion_rq_edit

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

    def init_ui_elementos_ds(self):
        self.agregar_ds_btn = self.ui.agregar_ds_btn
        self.actualizar_ds_btn = self.ui.actualizar_ds_btn
        self.seleccionar_ds_btn = self.ui.seleccionar_ds_btn
        self.buscar_ds_btn = self.ui.buscar_ds_btn
        self.limpiar_ds_btn = self.ui.limpiar_ds_btn
        self.borrar_ds_btn = self.ui.borrar_ds_btn
    
        #edicion manual de datos de salida
        self.nombre_ds_edit=self.ui.nombre_ds_edit
        self.fecha_ds_edit = self.ui.fecha_ds_edit
        self.nombre_data_ds_edit=self.ui.nombre_data_ds_edit
        self.id_nombre_data_ds_edit = self.ui.id_nombre_data_ds_edit
        self.id_condiciones_iniciales_ds_edit = self.ui.id_condiciones_iniciales_ds_edit
        self.id_registro_unidades_ds_edit = self.ui.id_registro_unidades_ds_edit

        self.r_ds_edit=self.ui.r_ds_edit

        self.nombre_reaccion_ds_edit=self.ui.nombre_reaccion_ds_edit
        self.delta_n_ds_edit=self.ui.delta_n_ds_edit
       
        self.epsilon_rl_ds_edit=self.ui.epsilon_rl_ds_edit

        self.tipo_especie_ds_edit=self.ui.tipo_especie_ds_edit
        self.especie_quimica_ds_edit=self.ui.especie_quimica_ds_edit

        self.constante_cinetica_ds_edit=self.ui.constante_cinetica_ds_edit
        self.orden_reaccion_ds_edit=self.ui.orden_reaccion_ds_edit
        self.modelo_cinetico_ds_edit=self.ui.modelo_cinetico_ds_edit
        self.tipo_calculo_ds_edit=self.ui.tipo_calculo_ds_edit
        self.energia_activacion_ds_edit=self.ui.energia_activacion_ds_edit
        self.detalles_ds_edit=self.ui.detalles_ds_edit
        #tabla de datos de salida
        self.tabla_datos_salida = self.ui.datos_salida_tabla
        self.tabla_datos_salida.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_ds.findChildren(QPushButton)


    def init_ui_elementos_u(self):
        #Edicion manual de unidades
        self.presion_u_edit = self.ui.presion_u_edit
        self.temperatura_u_edit = self.ui.temperatura_u_edit
        self.tiempo_u_edit = self.ui.tiempo_u_edit
        self.concentracion_u_edit = self.ui.concentracion_u_edit
        self.energia_u_edit = self.ui.energia_u_edit
        self.nombre_data_u_edit = self.ui.nombre_data_u_edit
        self.r_u_edit = self.ui.r_u_edit
        #botones de unidades
        self.agregar_ru_btn = self.ui.agregar_ru_btn
        self.actualizar_ru_btn = self.ui.actualizar_ru_btn
        self.seleccionar_ru_btn = self.ui.seleccionar_ru_btn
        self.buscar_ru_btn = self.ui.buscar_ru_btn
        self.limpiar_ru_btn = self.ui.limpiar_ru_btn
        self.borrar_ru_btn = self.ui.borrar_ru_btn


        #tabla de unidades
        self.tabla_registro_unidades = self.ui.registro_unidades_tabla
        self.tabla_registro_unidades.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_u.findChildren(QPushButton)    
    
    

    def init_control_botones_datos(self):
        # Conectar los botones a sus respectivas funciones
        # Datos cinéticos
        self.agregar_dc_btn.clicked.connect(self.agregar_dato)
        self.actualizar_dc_btn.clicked.connect(self.actualizar_dato)
        self.seleccionar_dc_btn.clicked.connect(self.seleccionar_dato)
        self.borrar_dc_btn.clicked.connect(self.borrar_dato)
        self.limpiar_dc_btn.clicked.connect(self.limpiar_formulario)
        self.buscar_dc_btn.clicked.connect(self.buscar_dato)

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

    def init_control_botones_u(self):
        self.agregar_ru_btn.clicked.connect(self.agregar_unidades)
        self.actualizar_ru_btn.clicked.connect(self.actualizar_unidades)
        self.seleccionar_ru_btn.clicked.connect(self.seleccionar_unidades)
        self.borrar_ru_btn.clicked.connect(self.borrar_unidades)
        self.limpiar_ru_btn.clicked.connect(self.limpiar_formulario_unidades)
        self.buscar_ru_btn.clicked.connect(self.buscar_unidades)

    def init_control_botones_ds(self):
        self.agregar_ds_btn.clicked.connect(self.agregar_datos_salida)
        self.actualizar_ds_btn.clicked.connect(self.actualizar_datos_salida)
        self.seleccionar_ds_btn.clicked.connect(self.seleccionar_datos_salida)
        self.borrar_ds_btn.clicked.connect(self.borrar_datos_salida)
        self.limpiar_ds_btn.clicked.connect(self.limpiar_formulario_datos_salida)
        self.buscar_ds_btn.clicked.connect(self.buscar_datos_salida)


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
        self.buscar_unidades()
        self.buscar_datos_salida()

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
            agregar_resultado = self.DatosCineticosManejador.agregar(dato)

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
            actualizar_resultado = self.DatosCineticosManejador.actualizar(id, nuevo_dato)

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
            id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.DatosCineticosManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(self.tabla_datos, borrar_resultado, "¿Estás seguro de eliminar el dato?", "Dato eliminado correctamente", "Hubo un problema al eliminar el dato", self.DatosCineticosManejador.consultar, self.refrescar_datos_tabla, self.buscar_dato)
                
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

        datos_resultados = self.DatosCineticosManejador.consultar(filtros,"like")
        self.mostrar_datos_tabla(datos_resultados)
    

    def mostrar_datos_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

    def actualizar_valor_celda_datos(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos, self.DatosCineticosManejador, fila, columna)

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
            agregar_resultado = self.RegistroDataExperimentalManejador.agregar(registro)

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
            actualizar_resultado = self.RegistroDataExperimentalManejador.actualizar(id, nuevo_registro)

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
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_data_experimental, self.RegistroDataExperimentalManejador, fila, columna)

    def borrar_registro_data_experimental(self):
        fila_seleccionada = self.tabla_registro_data_experimental.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_registro_data_experimental.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroDataExperimentalManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_registro_data_experimental, 
                borrar_resultado, 
                "¿Estás seguro de eliminar el registro?", 
                "Registro eliminado correctamente", 
                "Hubo un problema al eliminar el registro", 
                self.RegistroDataExperimentalManejador.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_registros
            )
    def buscar_registros(self):
        filtros = {
            "nombre_data": self.nombre_data_experimental.text(),
            "fecha": self.fecha_data_experimental.text(),
            "detalle": self.detalle_data_experimental.text(),
        }
        registros = self.RegistroDataExperimentalManejador.consultar(filtros, "like")
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
            agregar_resultado = self.CondicionesInicialesManejador.agregar(condiciones_iniciales)

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
            actualizar_resultado = self.CondicionesInicialesManejador.actualizar(id, nuevas_condiciones_iniciales)

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
        self.metodos_comunes.actualizar_valor_celda(self.tabla_condiciones_iniciales, self.CondicionesInicialesManejador, fila, columna)

    def borrar_condiciones_iniciales(self):
        fila_seleccionada = self.tabla_condiciones_iniciales.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_condiciones_iniciales.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.CondicionesInicialesManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_condiciones_iniciales, 
                borrar_resultado, 
                "¿Estás seguro de eliminar las condiciones iniciales?", 
                "Condiciones iniciales eliminadas correctamente", 
                "Hubo un problema al eliminar las condiciones iniciales", 
                self.CondicionesInicialesManejador.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_condiciones_iniciales
            )
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
        condiciones_iniciales = self.CondicionesInicialesManejador.consultar(filtros, "like")
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
            agregar_resultado = self.ReaccionQuimicaManejador.agregar(reaccion_quimica)

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
            actualizar_resultado = self.ReaccionQuimicaManejador.actualizar(id, nueva_reaccion_quimica)

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
        self.metodos_comunes.actualizar_valor_celda(self.tabla_reaccion_quimica, self.ReaccionQuimicaManejador, fila, columna)

    def borrar_reaccion_quimica(self):
        fila_seleccionada = self.tabla_reaccion_quimica.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_reaccion_quimica.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.ReaccionQuimicaManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_reaccion_quimica, 
                borrar_resultado, 
                "¿Estás seguro de eliminar la reacción química?", 
                "Reacción química eliminada correctamente", 
                "Hubo un problema al eliminar la reacción química", 
                self.ReaccionQuimicaManejador.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_reaccion_quimica
            ) 
    def buscar_reaccion_quimica(self):
        filtros = {
            "especie_quimica": self.especie_quimica_rq.text(),
            "formula": self.formula_rq.text(),
            "coeficiente_estequiometrico": self.coeficiente_estequiometro_rq.text(),
            "detalle": self.detalle_rq.text(),
            "tipo_especie": self.tipo_especie_rq.text(),
            "nombre_reaccion": self.nombre_reaccion_rq.text(),
        }
        reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros, "like")
        self.mostrar_reaccion_quimica(reaccion_quimica)

    def agregar_unidades(self):
        self.boton_desactivado()

        # Validar que todos los campos estén llenos
        try:
            presion = self.presion_u_edit.text()
            temperatura = self.temperatura_u_edit.text()
            tiempo = self.tiempo_u_edit.text()
            concentracion = self.concentracion_u_edit.text()
            energia = self.energia_u_edit.text()
            r = float(self.r_u_edit.text())
            nombre_data = self.nombre_data_u_edit.text()
            
            if not presion or not temperatura or not tiempo or not concentracion or not energia or not nombre_data:
                raise ValueError("Todos los campos de texto deben estar llenos")
        except ValueError as e:
            # Crear un QMessageBox con opciones de Cancelar, Aceptar, y Completar con 0
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Advertencia")
            msg_box.setText(f"Datos inválidos o incompletos: {e}")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Ignore)
            msg_box.button(QMessageBox.StandardButton.Cancel).setText("Cancelar")
            msg_box.button(QMessageBox.StandardButton.Ok).setText("Aceptar")
            msg_box.button(QMessageBox.StandardButton.Ignore).setText("Completar con 0")

            result = msg_box.exec()

            if result == QMessageBox.StandardButton.Cancel:
                self.boton_activado()
                return
            elif result == QMessageBox.StandardButton.Ignore:
                # Completar campos vacíos con 0 o 'N/A'
                presion = presion or '0'
                temperatura = temperatura or '0'
                tiempo = tiempo or '0'
                concentracion = concentracion or '0'
                energia = energia or '0'
                r = r or '0'
                nombre_data = nombre_data or 'N/A'
            else:
                # Si se selecciona "Aceptar", simplemente se reintenta la operación
                self.boton_activado()
                return

        # Crear el objeto RegistroUnidades
        unidades = RegistroUnidades(
            presion=presion,
            temperatura=temperatura,
            tiempo=tiempo,
            concentracion=concentracion,
            energia=energia,
            r=r,
            nombre_data=nombre_data
        )

        # Intentar agregar las unidades a la base de datos
        try:
            print("Intentando agregar unidades:", unidades)
            agregar_resultado = self.RegistroUnidadesManejador.agregar(unidades)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Unidades agregadas correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_unidades()
                self.buscar_unidades()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar las unidades", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar las unidades: {e}", QMessageBox.StandardButton.Ok)
        
        self.boton_activado()
            
    def actualizar_unidades(self):
        self.boton_desactivado()
        try:
            # Obtener el ID de las unidades seleccionadas
            fila_seleccionada = self.tabla_registro_unidades.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return
            id = int(self.tabla_registro_unidades.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            presion = self.presion_u_edit.text()
            temperatura = self.temperatura_u_edit.text()
            tiempo = self.tiempo_u_edit.text()
            concentracion = self.concentracion_u_edit.text()
            energia = self.energia_u_edit.text()
            r= float(self.r_u_edit.text())
            nombre_data = self.nombre_data_u_edit.text()

            if not presion or not temperatura or not tiempo or not concentracion or not energia or not nombre_data:
                raise ValueError("Todos los campos de texto deben estar llenos")
            
            # Crear el objeto de unidades actualizadas
            nuevas_unidades = {
                "presion": presion,
                "temperatura": temperatura,
                "tiempo": tiempo,
                "concentracion": concentracion,
                "energia": energia,
                "r": r,
                "nombre_data": nombre_data,
            }

            # Intentar actualizar las unidades en la base de datos
            actualizar_resultado = self.RegistroUnidadesManejador.actualizar(id, nuevas_unidades)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Unidades actualizadas correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_unidades()
                self.buscar_unidades()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar las unidades", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al actualizar las unidades: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar las unidades: {e}", QMessageBox.StandardButton.Ok)

        finally:
            self.boton_activado()


        

    def seleccionar_unidades(self):
        columnas = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_registro_unidades, columnas, elementos_visuales)
        if datos:
            #self.statusbar.showMessage(f"Set de Unidades seleccionada id: {datos['id']}", 5000)
            print(f"Set de Unidades seleccionada id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    
    def borrar_unidades(self):
        fila_seleccionada = self.tabla_registro_unidades.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_registro_unidades.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroUnidadesManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_registro_unidades, 
                borrar_resultado, 
                "¿Estás seguro de eliminar las unidades?", 
                "Unidades eliminadas correctamente", 
                "Hubo un problema al eliminar las unidades", 
                self.RegistroUnidadesManejador.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_unidades
            )           
    def buscar_unidades(self):
        filtros = {
            "presion": self.presion_u_edit.text(),
            "temperatura": self.temperatura_u_edit.text(),
            "tiempo": self.tiempo_u_edit.text(),
            "concentracion": self.concentracion_u_edit.text(),
            "energia": self.energia_u_edit.text(),
            "r": self.r_u_edit.text(),
            "nombre_data": self.nombre_data_u_edit.text()

        }
        unidades = self.RegistroUnidadesManejador.consultar(filtros, "like")
        self.mostrar_unidades(unidades)

    def actualizar_valor_celda_unidades(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_unidades, self.RegistroUnidadesManejador, fila, columna)

    def mostrar_unidades(self,unidades):
        self.metodos_comunes.mostrar_unidades(self.tabla_registro_unidades, unidades)

    def limpiar_formulario_unidades(self):
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.nombre_data_u_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    
    def actualizar_valor_celda_datos_salida(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos_salida, self.RegistroDatosSalidaManejador, fila, columna)

    #refactor de tabla salida
    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados)
    
    def buscar_datos_salida(self):
        filtros = {
            "nombre_data_salida": self.nombre_ds_edit.text(),
            "fecha": self.fecha_ds_edit.text(),
            "id_nombre_data": self.id_nombre_data_ds_edit.text(),
            "id_condiciones_iniciales" : self.id_condiciones_iniciales_ds_edit.text(),
            "id_registro_unidades" : self.id_registro_unidades_ds_edit.text(),
            "r_utilizada" : self.r_ds_edit.text(),
            "nombre_data" : self.nombre_data_ds_edit.text(),
            "nombre_reaccion" : self.nombre_reaccion_ds_edit.text(),
            "delta_n_reaccion" : self.delta_n_ds_edit.text(),
            "epsilon_reactivo_limitante" : self.epsilon_rl_ds_edit.text(),
            "tipo_especie": self.tipo_especie_ds_edit.text(),
            "especie_quimica": self.especie_quimica_ds_edit.text(),
            "constante_cinetica": self.constante_cinetica_ds_edit.text(),
            "orden_reaccion": self.orden_reaccion_ds_edit.text(),
            "modelo_cinetico": self.modelo_cinetico_ds_edit.text(),
            "tipo_calculo": self.tipo_calculo_ds_edit.text(),
            "energia_activacion": self.energia_activacion_ds_edit.text(),
            "detalles": self.detalles_ds_edit.text(),
        }
        datos_salida = self.RegistroDatosSalidaManejador.consultar(filtros, "like")
        self.mostrar_datos_tabla_salida(datos_salida)
    
    def limpiar_formulario_datos_salida(self):
        self.nombre_ds_edit.clear()
        self.fecha_ds_edit.clear()
        self.id_nombre_data_ds_edit.clear()
        self.id_condiciones_iniciales_ds_edit.clear()
        self.id_registro_unidades_ds_edit.clear()
        self.r_ds_edit.clear()
        self.nombre_data_ds_edit.clear()
        self.nombre_reaccion_ds_edit.clear()
        self.delta_n_ds_edit.clear()
        self.epsilon_rl_ds_edit.clear()
        self.tipo_especie_ds_edit.clear()
        self.especie_quimica_ds_edit.clear()
        self.constante_cinetica_ds_edit.clear()
        self.orden_reaccion_ds_edit.clear()
        self.modelo_cinetico_ds_edit.clear()
        self.tipo_calculo_ds_edit.clear()
        self.energia_activacion_ds_edit.clear()
        self.detalles_ds_edit.clear()
    
    def seleccionar_datos_salida(self):
        seleccionar_fila = self.tabla_datos_salida.currentRow()
        if seleccionar_fila != -1:
            id = self.tabla_datos_salida.item(seleccionar_fila, 0).text().strip()
            nombre_data_salida = self.tabla_datos_salida.item(seleccionar_fila, 1).text().strip()
            fecha = self.tabla_datos_salida.item(seleccionar_fila, 2).text().strip()
            id_nombre_data = self.tabla_datos_salida.item(seleccionar_fila, 3).text().strip()
            id_condiciones_iniciales = self.tabla_datos_salida.item(seleccionar_fila, 4).text().strip()
            id_registro_unidades = self.tabla_datos_salida.item(seleccionar_fila, 5).text().strip()
            r_utilizada = self.tabla_datos_salida.item(seleccionar_fila, 6).text().strip()
            nombre_data = self.tabla_datos_salida.item(seleccionar_fila, 7).text().strip()
            nombre_reaccion = self.tabla_datos_salida.item(seleccionar_fila, 8).text().strip()
            delta_n_reaccion = self.tabla_datos_salida.item(seleccionar_fila, 9).text().strip()
            epsilon_reactivo_limitante = self.tabla_datos_salida.item(seleccionar_fila, 10).text().strip()
            tipo_especie = self.tabla_datos_salida.item(seleccionar_fila, 11).text().strip()
            especie_quimica = self.tabla_datos_salida.item(seleccionar_fila, 12).text().strip()
            constante_cinetica = self.tabla_datos_salida.item(seleccionar_fila, 13).text().strip()
            orden_reaccion = self.tabla_datos_salida.item(seleccionar_fila, 14).text().strip()
            modelo_cinetico = self.tabla_datos_salida.item(seleccionar_fila, 15).text().strip()
            tipo_calculo = self.tabla_datos_salida.item(seleccionar_fila, 16).text().strip()
            energia_activacion = self.tabla_datos_salida.item(seleccionar_fila, 17).text().strip()
            detalles = self.tabla_datos_salida.item(seleccionar_fila, 18).text().strip()

            self.nombre_ds_edit.setText(nombre_data_salida)
            self.fecha_ds_edit.setText(fecha)
            self.id_nombre_data_ds_edit.setText(id_nombre_data)
            self.id_condiciones_iniciales_ds_edit.setText(id_condiciones_iniciales)
            self.id_registro_unidades_ds_edit.setText(id_registro_unidades)
            self.r_ds_edit.setText(r_utilizada)
            self.nombre_data_ds_edit.setText(nombre_data)
            self.nombre_reaccion_ds_edit.setText(nombre_reaccion)
            self.delta_n_ds_edit.setText(delta_n_reaccion)
            self.epsilon_rl_ds_edit.setText(epsilon_reactivo_limitante)
            self.tipo_especie_ds_edit.setText(tipo_especie)
            self.especie_quimica_ds_edit.setText(especie_quimica)
            self.constante_cinetica_ds_edit.setText(constante_cinetica)
            self.orden_reaccion_ds_edit.setText(orden_reaccion)
            self.modelo_cinetico_ds_edit.setText(modelo_cinetico)
            self.tipo_calculo_ds_edit.setText(tipo_calculo)
            self.energia_activacion_ds_edit.setText(energia_activacion)
            self.detalles_ds_edit.setText(detalles)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    def borrar_datos_salida(self):
        fila_seleccionada = self.tabla_datos_salida.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_datos_salida.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroDatosSalidaManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_datos_salida, 
                borrar_resultado, 
                "¿Estás seguro de eliminar los datos de salida?", 
                "Datos de salida eliminados correctamente", 
                "Hubo un problema al eliminar los datos de salida", 
                self.RegistroDatosSalidaManejador.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_datos_salida
            )
    def actualizar_datos_salida(self):
        self.boton_desactivado()
        try:
            # Obtener el ID de los datos de salida seleccionados
            fila_seleccionada = self.tabla_datos_salida.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Seleccione una fila para actualizar", QMessageBox.StandardButton.Ok)
                return
            id = int(self.tabla_datos_salida.item(fila_seleccionada, 0).text().strip())

            # Validaciones
            nombre_data_salida=self.nombre_ds_edit.text()
            fecha_ds=self.fecha_ds_edit.text()
            id_nombre_data=int(self.id_nombre_data_ds_edit.text())
            id_condiciones_iniciales=int(self.id_condiciones_iniciales_ds_edit.text())
            id_registro_unidades=int(self.id_registro_unidades_ds_edit.text())
            r_utilizada=float(self.r_ds_edit.text())
            nombre_data=self.nombre_data_ds_edit.text()
            nombre_reaccion=self.nombre_reaccion_ds_edit.text()
            delta_n_reaccion=float(self.delta_n_ds_edit.text())
            epsilon_reactivo_limitante=float(self.epsilon_rl_ds_edit.text())
            tipo_especie=self.tipo_especie_ds_edit.text()
            especie_quimica=self.especie_quimica_ds_edit.text()
            constante_cinetica=float(self.constante_cinetica_ds_edit.text())
            orden_reaccion=float(self.orden_reaccion_ds_edit.text())
            modelo_cinetico=self.modelo_cinetico_ds_edit.text()
            tipo_calculo=self.tipo_calculo_ds_edit.text()
            energia_activacion=float(self.energia_activacion_ds_edit.text())
            detalles_ds=self.detalles_ds_edit.text()

            if not nombre_data_salida or not fecha_ds or not id_nombre_data or not id_condiciones_iniciales or not id_registro_unidades or not r_utilizada or not nombre_data or not delta_n_reaccion or not epsilon_reactivo_limitante or not tipo_especie or not especie_quimica or not constante_cinetica or not orden_reaccion or not modelo_cinetico or not tipo_calculo or not energia_activacion or not detalles_ds:
                raise ValueError("Todos los campos de texto deben estar llenos")
        
            # Crear el objeto de datos de salida actualizados
            nuevos_datos_salida = {
                "nombre_data_salida": nombre_data_salida,
                "fecha": fecha_ds,
                "id_nombre_data": id_nombre_data,
                "id_condiciones_iniciales": id_condiciones_iniciales,
                "id_registro_unidades": id_registro_unidades,
                "r_utilizada": r_utilizada,
                "nombre_data": nombre_data,
                "nombre_reaccion": nombre_reaccion,
                "delta_n_reaccion": delta_n_reaccion,
                "epsilon_reactivo_limitante": epsilon_reactivo_limitante,
                "tipo_especie": tipo_especie,
                "especie_quimica": especie_quimica,
                "constante_cinetica": constante_cinetica,
                "orden_reaccion": orden_reaccion,
                "modelo_cinetico": modelo_cinetico,
                "tipo_calculo": tipo_calculo,
                "energia_activacion": energia_activacion,
                "detalles": detalles_ds,
            }

            # Intentar actualizar los datos de salida en la base de datos
            actualizar_resultado = self.RegistroDatosSalidaManejador.actualizar(id, nuevos_datos_salida)

            if actualizar_resultado:
                QMessageBox.information(self, "Información", "Datos de salida actualizados correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_datos_salida()
                self.buscar_datos_salida()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al actualizar los datos de salida", QMessageBox.StandardButton.Ok)
            
        except ValueError as ve:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error("Error al actualizar los datos de salida: %s", str(e))
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar los datos de salida: {e}", QMessageBox.StandardButton.Ok)
        
        finally:
            self.boton_activado()
        
    def agregar_datos_salida(self):
        self.boton_desactivado()
        try:
            nombre_data_salida=self.nombre_ds_edit.text()
            fecha_ds=self.fecha_ds_edit.text()
            id_nombre_data=int(self.id_nombre_data_ds_edit.text())
            id_condiciones_iniciales=int(self.id_condiciones_iniciales_ds_edit.text())
            id_registro_unidades=int(self.id_registro_unidades_ds_edit.text())
            r_utilizada=float(self.r_ds_edit.text())
            nombre_data=self.nombre_data_ds_edit.text()
            nombre_reaccion=self.nombre_reaccion_ds_edit.text()
            delta_n_reaccion=float(self.delta_n_ds_edit.text())
            epsilon_reactivo_limitante=float(self.epsilon_rl_ds_edit.text())
            tipo_especie=self.tipo_especie_ds_edit.text()
            especie_quimica=self.especie_quimica_ds_edit.text()
            constante_cinetica=float(self.constante_cinetica_ds_edit.text())
            orden_reaccion=float(self.orden_reaccion_ds_edit.text())
            modelo_cinetico=self.modelo_cinetico_ds_edit.text()
            tipo_calculo=self.tipo_calculo_ds_edit.text()
            energia_activacion=float(self.energia_activacion_ds_edit.text())
            detalles_ds=self.detalles_ds_edit.text()

            #if not nombre_data_salida or not fecha_ds or not id_nombre_data or not id_condiciones_iniciales or not id_registro_unidades or not r_utilizada or not nombre_data or not delta_n_reaccion or not epsilon_reactivo_limitante :
            if not nombre_data_salida or not fecha_ds or not id_nombre_data or not id_condiciones_iniciales or not id_registro_unidades or not r_utilizada or not nombre_data or not delta_n_reaccion or not epsilon_reactivo_limitante or not tipo_especie or not especie_quimica or not constante_cinetica or not orden_reaccion or not modelo_cinetico or not tipo_calculo or not energia_activacion or not detalles_ds:
                raise ValueError("Todos los campos de texto deben estar llenos")
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return
        #crear el objeto datos_salida
        datos_salida=DatosSalida(
            nombre_data_salida=nombre_data_salida,
            fecha=fecha_ds,
            id_nombre_data=id_nombre_data,
            id_condiciones_iniciales=id_condiciones_iniciales,
            id_registro_unidades=id_registro_unidades,
            r_utilizada=r_utilizada,
            nombre_data=nombre_data,
            nombre_reaccion=nombre_reaccion,
            delta_n_reaccion=delta_n_reaccion,
            epsilon_reactivo_limitante=epsilon_reactivo_limitante,
            tipo_especie=tipo_especie,
            especie_quimica=especie_quimica,
            constante_cinetica=constante_cinetica,
            orden_reaccion=orden_reaccion,
            modelo_cinetico=modelo_cinetico,
            tipo_calculo=tipo_calculo,
            energia_activacion=energia_activacion,
            detalles=detalles_ds
        )

        #intentar agregar los datos de salida a la base de datos
        try:
            print("Intentando agregar datos de salida:", datos_salida)
            agregar_resultado = self.RegistroDatosSalidaManejador.agregar(datos_salida)

            if agregar_resultado:
                QMessageBox.information(self, "Información", "Datos de salida agregados correctamente", QMessageBox.StandardButton.Ok)
                self.limpiar_formulario_datos_salida()
                self.buscar_datos_salida()
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al agregar los datos de salida", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos de salida: {e}", QMessageBox.StandardButton.Ok)

        self.boton_activado()    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PantallaCrud()
    window.show()
    sys.exit(app.exec())
