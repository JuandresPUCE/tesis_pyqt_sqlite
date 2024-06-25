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
    def __init__(self,parent=None):
        self.parent = parent
        super(FlujoDatos, self).__init__(parent)
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
        self.init_ui_menu_derecho()

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

        #iniciar funciones diferentes a crud
        self.establecer_fecha_sistema()

        json_tipo_especie = r"data\tipo_especie.json"

        self.cargar_datos_json(json_tipo_especie)

        #mensajes barra de estado
        self.statusbar=self.ui.statusbar
        self.statusbar.showMessage("Bienvenido al sistema de flujo de datos")


    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()     

        self.metodos_comunes = Servicios(self)


    def init_ui_menu_derecho(self):
        #nombre_data_general_edit
        self.nombre_data = self.ui.nombre_data_general_edit
        #nombre_reaccion_dc_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_general_edit
        self.nombre_data_experimental = self.ui.nombre_data_general_edit
        self.nombre_data_ci = self.ui.nombre_data_general_edit
        self.nombre_reaccion_rq = self.ui.nombre_reaccion_general_edit

        #configuracion unidades
        self.nombre_data_u_edit = self.ui.nombre_data_general_edit
        #data salida
        self.r_ds_edit =self.ui.r_u_edit
    
        self.nombre_reaccion_ds_edit=self.ui.nombre_reaccion_general_edit
        self.nombre_data_ds_edit=self.ui.nombre_data_general_edit

                #botones
        self.marcar_ci_btn = self.ui.marcar_ci_btn
        self.epsilon_a_btn = self.ui.epsilon_a_btn
        self.epsilon_reactivo_limitante_calculo = self.ui.epsilon_reactivo_limitante_calculo
        self.concentracion_irl_btn=self.ui.concentracion_irl_btn

        self.funciones=Funciones()

         #objetos test dc
        self.calculo1=self.ui.marcar_a0_btn
        self.calculo0=self.ui.marcar_producto0_btn
        self.calculo2=self.ui.marcar_coeficiente_producto_btn
        self.calculo3=self.ui.marcar_coeficiente_reactivo_btn
        self.calculo4=self.ui.calcular_xa
        self.calculo5=self.ui.calcular_a
        self.calculo6=self.ui.calcular_producto
        self.calculo7=self.ui.conversion_gas_epsilon_a
        self.calculo8=self.ui.concentracion_irl_btn

        self.coeficiente_estequiometro_producto = self.ui.coeficiente_estequiometrico_producto_edit
        self.coeficiente_estequiometro_reactivo = self.ui.coeficiente_estequiometrico_reactivo_edit
        self.concentracion_inicial_reactivo_limitante = self.ui.concentracion_reactivo_limitante_edit
        self.concentracion_inicial_producto = self.ui.concentracion_producto_edit
        self.concentracion_producto_calculo = self.ui.concentracion_producto_calculo_edit
        self.concentracion_reactivo_limitante_calculo = self.ui.concentracion_reactivo_limitante_calculo
        self.conversion_reactivo_limitante_calculo = self.ui.conversion_reactivo_limitante_dc_edit_2
        self.otra_propiedad_inicial = self.ui.otra_propiedad_inicial_edit
        self.conversion_reactivo_limitante_gas = self.ui.conversion_reactivo_limitante_dc_edit_3
        self.concentracion_reactivo_limitante_calculo_2=self.ui.concentracion_reactivo_limitante_calculo_2
        self.agregar_dc_archivo_btn=self.ui.agregar_dc_archivo_btn

        #objetos test rq

        #box en calculos rq
        self.nombre_reaccion_rq_box=self.ui.nombre_reaccion_rq_box
        self.filtrar_reaccion_quimica()
        
        #self.especie_quimica_rq_box.currentIndexChanged.connect(self.)
        
        self.calcular_delta_n = self.ui.delta_n_btn

        self.delta_n_rq = self.ui.delta_n_edit

        #calculos
        
        self.calculo0.clicked.connect(self.marcar_quimico_inicial)
        self.calculo1.clicked.connect(self.marcar_quimico_inicial)
        self.calculo2.clicked.connect(self.marcar_coeficiente)
        self.calculo3.clicked.connect(self.marcar_coeficiente)
        self.calculo4.clicked.connect(self.calcular_conversion_reactivo_limitante_dado_producto)
        self.calculo5.clicked.connect(self.calcular_concentracion_reactivo_limitante_dado_conversion)
        self.calculo6.clicked.connect(self.calcular_concentracion_producto_dado_conversion)
        self.calculo7.clicked.connect(self.calcular_conversion_reactivo_limitante_dado_epsilon_a_presion)
        self.calculo8.clicked.connect(self.calcular_conversion_reactivo_limitante_dado_concentracion_gas)

        self.agregar_dc_archivo_btn.clicked.connect(self.cargar_datos_btn_click)
            
        self.epsilon_a_btn.clicked.connect(self.calcular_epsilon_reactivo_limitante)
        #calculos reaccion quimica
        self.calcular_delta_n.clicked.connect(self.calculo_delta_n)


    def init_ui_elementos_dc(self):
        # Datos cinéticos
        self.tiempo = self.ui.tiempo_dc_edit
        self.concentracion = self.ui.concentracion_dc_edit
        self.otra_propiedad = self.ui.otra_propiedad_dc_edit
        self.conversion_reactivo_limitante = self.ui.conversion_reactivo_limitante_dc_edit
        self.tipo_especie = self.ui.tipo_especie_dc_edit
        self.id_condiciones_iniciales = self.ui.id_condiciones_iniciales_dc_edit
        #nombre_reaccion_dc_edit
        #self.nombre_data = self.ui.nombre_data_dc_edit
        #nombre_reaccion_dc_edit
        #self.nombre_reaccion = self.ui.nombre_reaccion_dc_edit
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

        #objetos test rq

        #box en calculos rq
        self.nombre_reaccion_rq_box=self.ui.nombre_reaccion_rq_box
        self.filtrar_reaccion_quimica()
        
        #self.especie_quimica_rq_box.currentIndexChanged.connect(self.)
        
        self.calcular_delta_n = self.ui.delta_n_btn

        self.delta_n_rq = self.ui.delta_n_edit

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
        #self.nombre_data_ds_edit=self.ui.nombre_data_ds_edit
        self.id_nombre_data_ds_edit = self.ui.id_nombre_data_ds_edit
        self.id_condiciones_iniciales_ds_edit = self.ui.id_condiciones_iniciales_ds_edit
        self.id_registro_unidades_ds_edit = self.ui.id_registro_unidades_ds_edit

        #self.r_ds_edit=self.ui.r_ds_edit

        #self.nombre_reaccion_ds_edit=self.ui.nombre_reaccion_ds_edit
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


        #tabla tabla_datos_salida
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
        #self.nombre_data_u_edit = self.ui.nombre_data_u_edit
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
        self.marcar_ci_btn.clicked.connect(self.marcar_condiciones_iniciales)


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
        self.tabla_registro_unidades.clearContents()
                
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
#revisare version refactor de crud_db_controlador
    def borrar_dato(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar dato", "¿Estás seguro de eliminar el dato?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.DatosCineticosManejador.borrar(id)
                if borrar_resultado:
                    
                    QMessageBox.information(self, "Información", "Dato eliminado correctamente", QMessageBox.StandardButton.Ok)
                    self.DatosCineticosManejador.consultar()
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

        datos_resultados = self.DatosCineticosManejador.consultar(filtros,"like")
        self.mostrar_datos_tabla(datos_resultados)
    

    def mostrar_datos_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

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
            if self.DatosCineticosManejador.actualizar(id, new_dato):
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
            if self.RegistroDataExperimentalManejador.actualizar(id, new_registro):
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
                borrar_resultado = self.RegistroDataExperimentalManejador.borrar(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Registro eliminado correctamente", QMessageBox.StandardButton.Ok)
                    self.RegistroDataExperimentalManejador.consultar()
                    self.buscar_registros()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar el registro", QMessageBox.StandardButton.Ok)

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
            if self.CondicionesInicialesManejador.actualizar(id, new_condiciones_iniciales):
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
                borrar_resultado = self.CondicionesInicialesManejador.borrar(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Condiciones iniciales eliminadas correctamente", QMessageBox.StandardButton.Ok)
                    self.CondicionesInicialesManejador.consultar()
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
            if self.ReaccionQuimicaManejador.actualizar(id, new_reaccion_quimica):
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
                borrar_resultado = self.ReaccionQuimicaManejador.borrar(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Reacción química eliminada correctamente", QMessageBox.StandardButton.Ok)
                    self.ReaccionQuimicaManejador.consultar()
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
        reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros, "like")
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
                self.tipo_especie_rq_box.addItem(item["Descripcion"], item["id"])
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
    
    #empuja la seleccion al line edit
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



        #calcula la conversion de XA con respecto al la concentracion del producto 
    def calcular_conversion_reactivo_limitante_dado_producto(self):
        try:
            # Verificar individualmente cada campo y lanzar una excepción si está vacío
            if not self.concentracion.text().strip():
                raise ValueError("El campo 'Concentración datos cinéticos de la pestaña' está vacío. Por favor, llénelo.")
            if not self.concentracion_inicial_producto.text().strip():
                raise ValueError("El campo 'Concentración Inicial del Producto del panel' está vacío. Por favor, llénelo.")
            if not self.concentracion_inicial_reactivo_limitante.text().strip():
                raise ValueError("El campo 'Concentración Inicial del Reactivo Limitante del panel' está vacío. Por favor, llénelo.")
            if not self.coeficiente_estequiometro_producto.text().strip():
                raise ValueError("El campo 'Coeficiente Estequiométrico del Producto del panel' está vacío. Por favor, llénelo.")
            if not self.coeficiente_estequiometro_reactivo.text().strip():
                raise ValueError("El campo 'Coeficiente Estequiométrico Reactivo del panel' está vacío. Por favor, llénelo.")

            # Continuar con la conversión a float y el cálculo
            funciones = Funciones()
            concentracion = float(self.concentracion.text())
            concentracion_inicial_producto = float(self.concentracion_inicial_producto.text())
            concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
            coeficiente_estequiometro_producto = float(self.coeficiente_estequiometro_producto.text())
            coeficiente_estequiometro_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
            xa = funciones.conversion_reactivo_limitante_dado_producto(concentracion, concentracion_inicial_producto, concentracion_inicial_reactivo_limitante, coeficiente_estequiometro_producto, coeficiente_estequiometro_reactivo)
            self.conversion_reactivo_limitante.setText(str(xa))
            self.conversion_reactivo_limitante_calculo.setText(str(xa))
            self.statusbar.showMessage(f"la conversion del reactivo limitante es x reactivo limitante= {xa} .", 5000)
        except ValueError as e:
            # Mostrar el mensaje de error específico para el campo vacío
            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)
        

    #calcula A con Xa y la Concentracion inicial
    def calcular_concentracion_reactivo_limitante_dado_conversion(self):
        try:
            # Verificar individualmente cada campo y lanzar una excepción si está vacío
            if not self.concentracion_inicial_reactivo_limitante.text().strip():
                raise ValueError("El campo 'Concentración Inicial del Reactivo Limitante del panel' está vacío. Por favor, llénelo.")
            if not self.conversion_reactivo_limitante.text().strip():
                raise ValueError("El campo 'Conversión del Reactivo Limitante de la pestaña datos cinéticos' está vacío. Por favor, llénelo.")

            # Continuar con la conversión a float y el cálculo
            funciones = Funciones()
            concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
            conversion_reactivo_limitante = float(self.conversion_reactivo_limitante.text())
            A = funciones.concentracion_reactivo_funcion_conversion(concentracion_inicial_reactivo_limitante, conversion_reactivo_limitante)
            print(A)
            self.concentracion.setText(str(A))
            self.concentracion_reactivo_limitante_calculo.setText(str(A))
            self.statusbar.showMessage(f"la conversion del reactivo limitante es x reactivo limitante= {A} .", 5000)
        except ValueError as e:
            # Mostrar el mensaje de error específico para el campo vacío
            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    def calcular_concentracion_producto_dado_conversion(self):
        try:
            # Verificar individualmente cada campo y lanzar una excepción si está vacío
            if not self.concentracion_inicial_producto.text().strip():
                raise ValueError("El campo 'Concentración Inicial del Producto' está vacío. Por favor, llénelo.")
            if not self.concentracion_inicial_reactivo_limitante.text().strip():
                raise ValueError("El campo 'Concentración Inicial del Reactivo Limitante' está vacío. Por favor, llénelo.")
            if not self.conversion_reactivo_limitante.text().strip():
                raise ValueError("El campo 'Conversión del Reactivo Limitante' está vacío. Por favor, llénelo.")
            if not self.coeficiente_estequiometro_producto.text().strip():
                raise ValueError("El campo 'Coeficiente Estequiométrico del Producto' está vacío. Por favor, llénelo.")
            if not self.coeficiente_estequiometro_reactivo.text().strip():
                raise ValueError("El campo 'Coeficiente Estequiométrico del Reactivo' está vacío. Por favor, llénelo.")

            # Continuar con la conversión a float y el cálculo
            funciones = Funciones()
            concentracion_inicial_producto = float(self.concentracion_inicial_producto.text())
            concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
            conversion_reactivo_limitante = float(self.conversion_reactivo_limitante.text())
            coeficiente_estequiometro_producto = float(self.coeficiente_estequiometro_producto.text())
            coeficiente_estequiometro_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
            producto = funciones.concentracion_Producto(concentracion_inicial_producto, coeficiente_estequiometro_producto, coeficiente_estequiometro_reactivo, conversion_reactivo_limitante, concentracion_inicial_reactivo_limitante)
            print(producto)
            self.concentracion.setText(str(producto))
            self.concentracion_producto_calculo.setText(str(producto))
            self.statusbar.showMessage(f"La concentración del producto dada la conversión es: {producto}", 5000)
        except ValueError as e:
            # Mostrar el mensaje de error específico para el campo vacío
            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)
    
    def filtrar_reaccion_quimica(self):
        self.nombre_reaccion_rq_box.clear()
        self.nombre_reaccion_rq_box.addItem("Seleccione una opción", -1)

        reaccion_quimica = self.ReaccionQuimicaManejador.consultar()

        if reaccion_quimica:
            nombre_reaccion = set(registro.nombre_reaccion for registro in reaccion_quimica)
            for item in nombre_reaccion:
                self.nombre_reaccion_rq_box.addItem(item)
        else:
            QMessageBox.information(self, "No hay datos", "No se encontraron datos en la base de datos.", QMessageBox.StandardButton.Ok)


        #calcular despues
    def calculo_delta_n(self):
        try:
            funciones = Funciones()
            nombre_reaccion_seleccionada = self.nombre_reaccion_rq_box.currentText()
            # Consultar los datos de la reacción química seleccionada
            filtros = {"nombre_reaccion": nombre_reaccion_seleccionada}
            reaccion_quimica = self.ReaccionQuimicaManejador.consultar(filtros)
            
            if not reaccion_quimica:
                self.statusbar.showMessage("No se encontraron datos para la reacción seleccionada")
                return
            
            # Convertir los datos de la reacción química a un DataFrame de pandas
            df_reaccion_quimica = pd.DataFrame.from_records([r.__dict__ for r in reaccion_quimica])
            print(df_reaccion_quimica)
            coeficientes_productos = df_reaccion_quimica[df_reaccion_quimica["tipo_especie"] == "producto"]["coeficiente_estequiometrico"].tolist()
            coeficientes_reactivos = df_reaccion_quimica[(df_reaccion_quimica["tipo_especie"] == "reactivo_limitante") | (df_reaccion_quimica["tipo_especie"] == "reactivo")]["coeficiente_estequiometrico"].tolist()
            delta_n = funciones.calcular_delta_n(coeficientes_productos, coeficientes_reactivos)
            print(delta_n)
            self.delta_n_rq.setText(str(delta_n))
            self.delta_n_ds_edit.setText(str(delta_n))
            self.statusbar.showMessage(f"Delta n calculado: {delta_n}")
        except Exception as e:
            print(f"Ocurrió un error al calcular delta_n: {e}")
            self.statusbar.showMessage("Error al calcular")

    def marcar_condiciones_iniciales(self):
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

    def calcular_epsilon_reactivo_limitante(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.fraccion_molar_ci.text():
                self.statusbar.showMessage("El campo 'Fracción Molar de condiciones iniciales' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.delta_n_rq.text():
                self.statusbar.showMessage("El campo 'Delta n de la reacción quimica' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.coeficiente_estequiometro_reactivo.text():
                self.statusbar.showMessage("El campo del 'Coeficiente Estequiométrico del Reactivo' está vacío. Por favor, llénelo.", 5000)
                return
            
            fraccion_molar_inicial = float(self.fraccion_molar_ci.text())
            delta_n = float(self.delta_n_rq.text())
            coeficiente_estequiometrico_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
            epsilon_a = funciones.calcular_epsilon_A(fraccion_molar_inicial, delta_n, coeficiente_estequiometrico_reactivo)
            self.epsilon_reactivo_limitante_calculo.setText(str(epsilon_a))
            self.epsilon_rl_ds_edit.setText(str(epsilon_a))
            self.statusbar.showMessage(f"epsilon del reactivo limintante es e_rl= {epsilon_a} .", 5000)
        except ValueError as e:
            self.statusbar.showMessage(f"Error al convertir a float: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)
            
    def calcular_conversion_reactivo_limitante_dado_epsilon_a_presion(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.otra_propiedad_inicial.text():
                self.statusbar.showMessage("El campo 'Otra Propiedad Inicial del panel' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.otra_propiedad.text():
                self.statusbar.showMessage("El campo 'Otra Propiedad de la pestaña datos cinéticos' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.epsilon_reactivo_limitante_calculo.text():
                self.statusbar.showMessage("El campo 'Epsilon Reactivo Limitante del panel' está vacío. Por favor, llénelo.", 5000)
                return
            
            otra_propiedad_inicial = float(self.otra_propiedad_inicial.text())
            otra_propiedad = float(self.otra_propiedad.text())
            epsilon_a = float(self.epsilon_reactivo_limitante_calculo.text())
            gas_conversion_componente_principal = funciones.gas_conversion_componente_principal_epsilon_a(otra_propiedad, otra_propiedad_inicial, epsilon_a)
            
            self.conversion_reactivo_limitante_gas.setText(str(gas_conversion_componente_principal))
            self.statusbar.showMessage(f" La conversion del reactivo limitante es x reactivo limitante= {gas_conversion_componente_principal} .", 5000)
        except ValueError as e:
            self.statusbar.showMessage(f"Error al convertir a float: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    def calcular_conversion_reactivo_limitante_dado_concentracion_gas(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.temperatura_ci.text():
                self.statusbar.showMessage("El campo 'Temperatura condiciones iniciales' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.presion_total_ci.text():
                self.statusbar.showMessage("El campo 'Presión Total  de condiciones iniciales' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.fraccion_molar_ci.text():
                self.statusbar.showMessage("El campo 'Fracción Molar  de condiciones iniciales' está vacío. Por favor, llénelo.", 5000)
                return
            if not self.temperatura_u_edit.text():
                self.statusbar.showMessage("El campo 'Unidad de Temperatura de condiciones iniciales' está vacío. Por favor, llénelo.", 5000)
                return
            
            if not self.r_u_edit.text():
                self.statusbar.showMessage("El valor de R está vacío. Por favor, llénelo.", 5000)
                return
            
            temperatura = float(self.temperatura_ci.text())
            presion_total = float(self.presion_total_ci.text())
            fraccion_molar = float(self.fraccion_molar_ci.text())
            unidad_temperatura = self.temperatura_u_edit.text()
            
            concentracion_gas = funciones.gas_concentracion_componente(1, fraccion_molar, presion_total, self.r_u_edit, temperatura, unidad_temperatura)
            print(concentracion_gas)
            self.concentracion_reactivo_limitante_calculo_2.setText(str(concentracion_gas))
            self.statusbar.showMessage(f"La concentración inicial del gas reactivo limitante es: {concentracion_gas}", 5000)
        except ValueError as e:
            self.statusbar.showMessage(f"Error al convertir a float: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    def agregar_unidades(self):
        self.boton_desactivado()
        #validar que todos los campos esten llenos
        try:
            presion=self.presion_u_edit.text()
            temperatura=self.temperatura_u_edit.text()
            tiempo=self.tiempo_u_edit.text()
            concentracion=self.concentracion_u_edit.text()
            energia=self.energia_u_edit.text()
            nombre_data=self.nombre_data_u_edit.text()
        
            if not presion or not temperatura or not tiempo or not concentracion or not energia or not nombre_data:
                raise ValueError("Todos los campos de texto deben estar llenos")
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return
        #crear el objeto unidades
        unidades=RegistroUnidades(
            presion=presion,
            temperatura=temperatura,
            tiempo=tiempo,
            concentracion=concentracion,
            energia=energia,
            nombre_data=nombre_data
        )

        #intentar agregar las unidades a la base de datos
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
        seleccionar_fila = self.tabla_registro_unidades.currentRow()
        if seleccionar_fila != -1:
            id=self.tabla_registro_unidades.item(seleccionar_fila, 0).text().strip()
            presion=self.tabla_registro_unidades.item(seleccionar_fila, 1).text().strip()
            temperatura=self.tabla_registro_unidades.item(seleccionar_fila, 2).text().strip()
            tiempo=self.tabla_registro_unidades.item(seleccionar_fila, 3).text().strip()
            concentracion=self.tabla_registro_unidades.item(seleccionar_fila, 4).text().strip()
            energia=self.tabla_registro_unidades.item(seleccionar_fila, 5).text().strip()
            nombre_data=self.tabla_registro_unidades.item(seleccionar_fila, 6).text().strip()

            self.presion_u_edit.setText(presion)
            self.temperatura_u_edit.setText(temperatura)
            self.tiempo_u_edit.setText(tiempo)
            self.concentracion_u_edit.setText(concentracion)
            self.energia_u_edit.setText(energia)
            self.nombre_data_u_edit.setText(nombre_data)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    
    def borrar_unidades(self):
        fila_seleccionada = self.tabla_registro_unidades.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar unidades", "¿Estás seguro de eliminar las unidades?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_registro_unidades.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.RegistroUnidadesManejador.borrar(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Unidades eliminadas correctamente", QMessageBox.StandardButton.Ok)
                    self.RegistroUnidadesManejador.consultar()
                    self.buscar_unidades()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar las unidades", QMessageBox.StandardButton.Ok)


    def buscar_unidades(self):
        filtros = {
            "presion": self.presion_u_edit.text(),
            "temperatura": self.temperatura_u_edit.text(),
            "tiempo": self.tiempo_u_edit.text(),
            "concentracion": self.concentracion_u_edit.text(),
            "energia": self.energia_u_edit.text(),
            "nombre_data": self.nombre_data_u_edit.text()
        }
        unidades = self.RegistroUnidadesManejador.consultar(filtros, "like")
        self.mostrar_unidades(unidades)

    def actualizar_valor_celda_unidades(self, fila, columna):
        try:
            item = self.tabla_registro_unidades.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return
            
            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return
            
            # Verificar si la celda debe contener un número y convertirla
            header_text = self.tabla_registro_unidades.horizontalHeaderItem(columna).text().lower()
            if header_text in ['presion', 'temperatura', 'tiempo', 'concentracion', 'energia']:
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return
                
            # Obtener el ID de las unidades a actualizar
            id_item = self.tabla_registro_unidades.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return
            
            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            new_unidades = {header_text: nuevo_valor}

            # Intentar actualizar las unidades en la base de datos
            if self.RegistroUnidadesManejador.actualizar(id, new_unidades):
                logging.info(f"Unidades con ID {id} actualizadas correctamente")
            else:
                logging.error(f"No se pudo actualizar las unidades con ID {id}")
        
        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)

    def mostrar_unidades(self,unidades):
        self.metodos_comunes.mostrar_unidades(self.tabla_registro_unidades, unidades)

    def limpiar_formulario_unidades(self):
        self.presion_u_edit.clear()
        self.temperatura_u_edit.clear()
        self.tiempo_u_edit.clear()
        self.concentracion_u_edit.clear()
        self.energia_u_edit.clear()
        self.nombre_data_u_edit.clear()

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
            #tipo_especie=self.tipo_especie_ds_edit.text()
            #especie_quimica=self.especie_quimica_ds_edit.text()
            #constante_cinetica=float(self.constante_cinetica_ds_edit.text())
            #orden_reaccion=float(self.orden_reaccion_ds_edit.text())
            #modelo_cinetico=self.modelo_cinetico_ds_edit.text()
            #tipo_calculo=self.tipo_calculo_ds_edit.text()
            #energia_activacion=float(self.energia_activacion_ds_edit.text())
            #detalles_ds=self.detalles_ds_edit.text()

            if not nombre_data_salida or not fecha_ds or not id_nombre_data or not id_condiciones_iniciales or not id_registro_unidades or not r_utilizada or not nombre_data or not delta_n_reaccion or not epsilon_reactivo_limitante :
            #if not nombre_data_salida or not fecha_ds or not id_nombre_data or not id_condiciones_iniciales or not id_registro_unidades or not r_utilizada or not nombre_data or not delta_n_reaccion or not epsilon_reactivo_limitante or not tipo_especie or not especie_quimica or not constante_cinetica or not orden_reaccion or not modelo_cinetico or not tipo_calculo or not energia_activacion or not detalles_ds:
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
            #tipo_especie=tipo_especie,
            #especie_quimica=especie_quimica,
            #constante_cinetica=constante_cinetica,
            #orden_reaccion=orden_reaccion,
            #modelo_cinetico=modelo_cinetico,
            #tipo_calculo=tipo_calculo,
            #energia_activacion=energia_activacion,
            #detalles=detalles_ds
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

    #refactor de tabla salida
    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados)

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

    def actualizar_valor_celda_datos_salida(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos_salida, self.RegistroDatosSalidaManejador, fila, columna)


    def insertar_datos_cineticos_archivo(self, ruta_archivo):
        # Leer el archivo
        if ruta_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        elif ruta_archivo.endswith('.xlsx'):
            df = pd.read_excel(ruta_archivo)
        else:
            raise ValueError("Formato de archivo no soportado")

        # Iterar sobre cada fila del DataFrame
        for _, fila in df.iterrows():
            # Crear el objeto DatosIngresadosCineticos
            dato = DatosIngresadosCineticos(
                tiempo=float(fila['tiempo']),
                concentracion=float(fila['concentracion']),
                otra_propiedad=float(fila['otra_propiedad']),
                conversion_reactivo_limitante=float(fila['conversion_reactivo_limitante']),
                tipo_especie=fila['tipo_especie'],
                id_condiciones_iniciales=int(fila['id_condiciones_iniciales']),
                nombre_data=fila['nombre_data'],
                nombre_reaccion=fila['nombre_reaccion'],
                especie_quimica=fila['especie_quimica'],
            )

            # Intentar agregar el dato a la base de datos
            try:
                agregar_resultado = self.DatosCineticosManejador.agregar(dato)
                if not agregar_resultado:
                    QMessageBox.critical(self, "Error", "Hubo un problema al agregar los datos ", QMessageBox.StandardButton.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos: {e}", QMessageBox.StandardButton.Ok)

        QMessageBox.information(self, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
        self.buscar_dato()  # Refrescar la tabla con los nuevos datos



    def cargar_datos_btn_click(self):
        # Abrir la ventana de diálogo para seleccionar el archivo
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")

        # Si el usuario seleccionó un archivo (es decir, no hizo clic en "Cancelar")
        if ruta_archivo:
            # Llamar a tu función con la ruta del archivo seleccionado
            self.insertar_datos_cineticos_archivo(ruta_archivo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlujoDatos()
    window.show()
    sys.exit(app.exec())