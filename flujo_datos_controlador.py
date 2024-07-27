import os
import sys
import subprocess
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
from componentes_auxiliares import *

#respaldos 
from respaldos import Respaldos

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
        self.ocultar_elementos_vista()

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
        self.ajustes_visuales_tabla()
        # Completar los campos vacíos opcionales
        self.completar_campos_vacios()
        self.init_panel_menu()

        #refactor direccion con datos json
        #json_tipo_especie = r"data\tipo_especie.json"
        #self.cargar_datos_json(r"data\tipo_especie.json")
        self.json_unidades=r"data\unidades.json"
        self.cargar_datos_json_tipo_especie(r"data\tipo_especie.json")
        self.cargar_datos_json_unidades_temperatura(self.json_unidades)
        self.cargar_datos_json_unidades_presion(self.json_unidades)
        self.cargar_datos_json_unidades_tiempo(self.json_unidades)
        self.cargar_datos_json_unidades_concentracion(self.json_unidades)
        self.cargar_datos_json_unidades_energia(self.json_unidades)
        self.cargar_datos_json_constante_r(r"data\constante_R.json")
        

        #mensajes barra de estado
        self.statusbar=self.ui.statusbar
        self.statusbar.showMessage("Bienvenido al sistema de flujo de datos")
        self.statusbar.messageChanged.connect(self.cambiar_estilo_statusbar)

    def cambiar_estilo_statusbar(self):
        # Cambiar el estilo de statusbar a fondo negro con letra blanca
        self.statusbar.setStyleSheet("QStatusBar {background: black; color: white;}")
        # Usar QTimer para llamar a restablecer_estilo_statusbar después de 5 segundos
        QTimer.singleShot(7000, self.restablecer_estilo_statusbar)

    def restablecer_estilo_statusbar(self):
        # Restablecer el estilo de statusbar a su configuración original
        self.statusbar.setStyleSheet("")

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


    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()     

        self.metodos_comunes = Servicios(self)
        self.componentes_auxiliares = ComponentesAuxiliares()

    def init_ui_menu_derecho(self):
        #nombre_data_general_edit
        self.nombre_data = self.ui.nombre_data_general_edit
        #nombre_reaccion_dc_edit
        self.id_nombre_data_general_edit = self.ui.id_nombre_data_general_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_general_edit
        self.nombre_data_experimental = self.ui.nombre_data_general_edit
        self.nombre_data_ci = self.ui.nombre_data_general_edit
        self.nombre_reaccion_rq = self.ui.nombre_reaccion_general_edit
#revisar esta parte
        #configuracion unidades
        self.nombre_data_u_edit = self.ui.nombre_data_general_edit
        #data salida
        self.r_ds_edit =self.ui.r_ds_edit
    
        self.nombre_reaccion_ds_edit=self.ui.nombre_reaccion_general_edit
        self.nombre_data_ds_edit=self.ui.nombre_data_general_edit

                #botones
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
        self.calculo7=self.ui.conversion_propiedad_epsilon_a
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
        self.respaldar_btn = self.ui.respaldar_btn
        self.data_lista_btn = self.ui.data_lista_btn

        self.calculos_adicionales_btn=self.ui.calculos_adicionales_btn

        #objetos test rq

        #box en calculos rq
        self.nombre_reaccion_rq_box=self.ui.nombre_reaccion_rq_box
        self.filtrar_reaccion_quimica()
        
        #self.especie_quimica_rq_box.currentIndexChanged.connect(self.)
        
        self.calcular_delta_n = self.ui.delta_n_btn

        self.delta_n_rq = self.ui.delta_n_edit

        self.conversion_propiedad_aumenta = self.ui.conversion_propiedad_aumenta
        self.conversion_propiedad_disminuye = self.ui.conversion_propiedad_disminuye
        self.conversion_propiedad_aumenta.clicked.connect(lambda: self.calcular_conversion_reactivo_limitante_otra_propiedad(aumento=True))
        self.conversion_propiedad_disminuye.clicked.connect(lambda: self.calcular_conversion_reactivo_limitante_otra_propiedad(aumento=False))


        #calculos
        
        self.calculo0.clicked.connect(self.marcar_quimico_inicial)
        self.calculo1.clicked.connect(self.marcar_quimico_inicial)
        self.calculo2.clicked.connect(self.marcar_coeficiente)
        self.calculo3.clicked.connect(self.marcar_coeficiente)
        self.calculo4.clicked.connect(self.calcular_conversion)

        self.calculo5.clicked.connect(self.calcular_concentracion_reactivo_limitante_dado_conversion)
        self.calculo6.clicked.connect(self.calcular_concentracion_producto_dado_conversion)
        self.calculo7.clicked.connect(self.calcular_conversion_reactivo_limitante_dado_epsilon_a_presion)
        self.calculo8.clicked.connect(self.calcular_concentracion_reactivo_limitante_dado_concentracion_gas)
        

        self.agregar_dc_archivo_btn.clicked.connect(self.cargar_datos_btn_click)
        self.calculos_adicionales_btn.clicked.connect(self.calculos_adicionales)
            
        self.epsilon_a_btn.clicked.connect(self.calcular_epsilon_reactivo_limitante)
        #calculos reaccion quimica
        self.calcular_delta_n.clicked.connect(self.calculo_delta_n)

        self.nombre_data_experimental.textChanged.connect(self.buscar_registros_id)
        self.nombre_data_experimental.editingFinished.connect(self.buscar_registros_id)

        # conexion self.buscar_unidades_nombre_data()
        self.nombre_data_experimental.textChanged.connect(self.buscar_unidades_nombre_data)
        self.nombre_data_experimental.editingFinished.connect(self.buscar_unidades_nombre_data)

        self.respaldar_btn.clicked.connect(self.generar_respaldo)

        self.data_lista_btn.clicked.connect(self.reiniciar_aplicacion)

    def ocultar_elementos_vista(self):
        # Lista de nombres de elementos a ocultar
        elementos_ocultar = ['groupBox_33', 'nombre_data_rde_edit','nombre_reaccion_rq_edit','groupBox_41','nombre_data_ci_edit','groupBox_61','nombre_data_dc_edit','groupBox_60','nombre_reaccion_dc_edit','groupBox_14','groupBox_2', 'groupBox_3', 'groupBox_4', 'groupBox_5','groupBox_21','groupBox_17','groupBox_22','groupBox_24','groupBox_25','groupBox_29','groupBox_30','groupBox_31','groupBox_32','groupBox_52','group_box_computo']
        for nombre in elementos_ocultar:
            getattr(self.ui, nombre).hide()

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

        #box
        self.tipo_especie_dc_box = self.ui.tipo_especie_dc_box
        self.tipo_especie_dc_box.currentIndexChanged.connect(self.actualizar_lineedit_tipo_especie)

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

        #box
        self.tipo_especie_ci_box=self.ui.tipo_especie_ci_box
        self.tipo_especie_ci_box.currentIndexChanged.connect(self.actualizar_lineedit_tipo_especie)
    
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
        self.tipo_especie_rq_box.currentIndexChanged.connect(self.actualizar_lineedit_tipo_especie) 

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

        self.r_ds_edit=self.ui.r_ds_edit

        #self.nombre_reaccion_ds_edit=self.ui.nombre_reaccion_ds_edit
        self.delta_n_ds_edit=self.ui.delta_n_ds_edit
       
        self.epsilon_rl_ds_edit=self.ui.epsilon_rl_ds_edit

        self.tipo_especie_ds_edit=self.ui.tipo_especie_ds_edit
        self.especie_quimica_ds_edit=self.ui.especie_quimica_ds_edit

        self.constante_cinetica_ds_edit=self.ui.constante_cinetica_ds_edit
        self.orden_reaccion_ds_edit=self.ui.orden_reaccion_ds_edit
        self.modelo_cinetico_ds_edit=self.ui.modelo_cinetico_ds_edit
        self.tipo_calculo_ds_edit=self.ui.tipo_calculo_ds_edit
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

        #box unidades
        self.presion_box=self.ui.presion_box
        self.temperatura_box=self.ui.temperatura_box
        self.tiempo_box=self.ui.tiempo_box
        self.concentracion_box=self.ui.concentracion_box
        self.energia_box=self.ui.energia_box
        self.r_box=self.ui.r_box

        #conxiones box unidades
        self.presion_box.currentIndexChanged.connect(self.actualizar_lineedit_unidades_presion)
        self.temperatura_box.currentIndexChanged.connect(self.actualizar_lineedit_unidades_temperatura)
        self.tiempo_box.currentIndexChanged.connect(self.actualizar_lineedit_unidades_tiempo)
        self.concentracion_box.currentIndexChanged.connect(self.actualizar_lineedit_unidades_concentracion)
        self.energia_box.currentIndexChanged.connect(self.actualizar_lineedit_unidades_energia)
        self.r_box.currentIndexChanged.connect(self.actualizar_lineedit_constante_r)   

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

    # funciones crud para registro de data experimental
    # Registro de data experimental
    def mostrar_registros(self, registros):
        self.metodos_comunes.mostrar_registros(self.tabla_registro_data_experimental, registros)
    
    def agregar_registro_data_experimental(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            tipos = [str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDataExperimentalManejador,clase_objeto=RegistroDataExperimental,limpiar_func=self.limpiar_formulario_registro_data_experimental_agregar,buscar_func=self.buscar_registros)
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def actualizar_registro_data_experimental(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            tipos = [str, str, str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_registro_data_experimental,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDataExperimentalManejador,clase_objeto=RegistroDataExperimental,limpiar_func=self.limpiar_formulario_registro_data_experimental,buscar_func=self.buscar_registros)
        except ValueError as e:
            #QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}",5000)
    
    def limpiar_formulario_registro_data_experimental(self):
        elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    #elimina solo campos del flujo de datos experimental para los casos de agregar por primera vez
    def limpiar_formulario_registro_data_experimental_agregar(self):
        elementos_visuales = [self.fecha_data_experimental, self.detalle_data_experimental]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def seleccionar_registro_data_experimental(self):
        columnas = ["id", "nombre_data", "fecha", "detalle"]
        elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_registro_data_experimental, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Registro seleccionado id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return

    def actualizar_valor_celda_registro(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_data_experimental, self.RegistroDataExperimentalManejador, fila, columna)
        
    def borrar_registro_data_experimental(self):
        fila_seleccionada = self.tabla_registro_data_experimental.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_registro_data_experimental.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroDataExperimentalManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(self.tabla_registro_data_experimental,borrar_resultado,"¿Estás seguro de eliminar el registro?","Registro eliminado correctamente","Hubo un problema al eliminar el registro", self.RegistroDataExperimentalManejador.consultar, self.refrescar_datos_tabla, self.buscar_registros)
            self.statusbar.showMessage(f"Registro eliminado de tabla_registro_data_experimental id: {id}", 5000)

    def buscar_registros(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            aplicar_strip = [True, True, False]  # Ejemplo de configuración para aplicar strip solo a los dos primeros campos
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.RegistroDataExperimentalManejador, mostrar_func=self.mostrar_registros, like=True)
        except Exception as e:
            #print(f"Error al buscar registros: {e}")
            #Mostrar un mensaje de error en la interfaz de usuario
            self.statusbar.showMessage(f"Error al buscar registros: {e}" , 5000)

    #muestra el registro seleccionado en el formulario, no refactorizado
    def buscar_registros_id(self):
        # Verifica si nombre_data_experimental está vacío
        if not self.nombre_data_experimental.text().strip():
            self.id_nombre_data_general_edit.setText("")
            return  # Termina la ejecución del método aquí
        try:
            filtros = {"nombre_data": self.nombre_data_experimental.text()}
            registros = self.RegistroDataExperimentalManejador.consultar(filtros=filtros)
            if registros:  # Verifica si la lista no está vacía
                # Accede al atributo 'id' del registro directamente
                self.id_nombre_data_general_edit.setText(str(registros[0].id))
                self.ui.id_nombre_data_ds_edit.setText(str(registros[0].id))
            else:
                self.id_nombre_data_general_edit.setText("")
        except Exception as e:
            # Mostrar un mensaje de error en la interfaz de usuario
            self.statusbar.showMessage(f"Error al buscar registros por ID: {e}", 5000)

    # funciones crud para reaccion quimica
    # Reacción química
    def mostrar_reaccion_quimica(self, reaccion_quimica):
        self.metodos_comunes.mostrar_reacciones(self.tabla_reaccion_quimica, reaccion_quimica)
    
    def agregar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            tipos = [str, str, float, str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.ReaccionQuimicaManejador,clase_objeto=ReaccionQuimica,limpiar_func=self.limpiar_formulario_rq_agregar,buscar_func=self.buscar_reaccion_quimica)
            self.filtrar_reaccion_quimica()
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
            
        
    def actualizar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            tipos = [str, str, float, str, str, str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_reaccion_quimica,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.ReaccionQuimicaManejador,clase_objeto=ReaccionQuimica,limpiar_func=self.limpiar_formulario_rq,buscar_func=self.buscar_reaccion_quimica)
            self.filtrar_reaccion_quimica()
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
   
    def limpiar_formulario_rq(self):
        elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def limpiar_formulario_rq_agregar(self):
        elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def seleccionar_reaccion_quimica(self):
        columnas = ["id", "especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
        elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_reaccion_quimica, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Reacción química seleccionada id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return

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
            self.statusbar.showMessage(f"Registro eliminado de tabla_reaccion_quimica id: {id}", 5000)

    def buscar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            aplicar_strip = [True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.ReaccionQuimicaManejador, mostrar_func=self.mostrar_reaccion_quimica, like=True)
        except Exception as e:
            self.statusbar.showMessage(f"Error al buscar datos de reacciones químicas: {e}", 5000)

    # funciones crud para unidades

    def agregar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_experimental]
            tipos = [str, str, str, str, str, float,str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroUnidadesManejador,clase_objeto=RegistroUnidades,limpiar_func=self.limpiar_formulario_unidades_agregar,buscar_func=self.buscar_unidades)
            self.buscar_unidades_nombre_data()
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def actualizar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r" ,"nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_experimental]
            tipos = [str, str, str, str, str, float,str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_registro_unidades,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroUnidadesManejador,clase_objeto=RegistroUnidades,limpiar_func=self.limpiar_formulario_unidades,buscar_func=self.buscar_unidades)
            self.buscar_unidades_nombre_data()
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def seleccionar_unidades(self):
        columnas = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_registro_unidades, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Set de Unidades seleccionada id: {datos['id']}", 5000)
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
            self.statusbar.showMessage(f"Registro eliminado de tabla_registro_unidades id: {id}", 5000)

    def buscar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
            aplicar_strip = [True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.RegistroUnidadesManejador, mostrar_func=self.mostrar_unidades, like=True)
        except Exception as e:
            self.statusbar.showMessage(f"Error al buscar datos de unidades: {e}", 5000)

    def actualizar_valor_celda_unidades(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_unidades, self.RegistroUnidadesManejador, fila, columna)
 
    def mostrar_unidades(self,unidades):
        self.metodos_comunes.mostrar_unidades(self.tabla_registro_unidades, unidades)
    
    def limpiar_formulario_unidades(self):
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit, self.nombre_data_u_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def limpiar_formulario_unidades_agregar(self):
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    # funciones crud para condiciones iniciales
    def mostrar_condiciones_iniciales(self, condiciones_iniciales):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.tabla_condiciones_iniciales, condiciones_iniciales)
    
    def agregar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            tipos = [float, float, float, float, float, str, str, str,str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.CondicionesInicialesManejador,clase_objeto=CondicionesIniciales,limpiar_func=self.limpiar_formulario_ci_agregar,buscar_func=self.buscar_condiciones_iniciales)
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def actualizar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            tipos = [float, float, float, float, float, str, str, str,str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_condiciones_iniciales,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.CondicionesInicialesManejador,clase_objeto=CondicionesIniciales,limpiar_func=self.limpiar_formulario_ci,buscar_func=self.buscar_condiciones_iniciales)
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def limpiar_formulario_ci(self):
        elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def limpiar_formulario_ci_agregar(self):
        elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def seleccionar_condiciones_iniciales(self):
        columnas = ["id", "temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
        elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_condiciones_iniciales, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Condiciones iniciales seleccionadas id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return

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
            self.statusbar.showMessage(f"Registro eliminado de tabla_condiciones_iniciales id: {id}", 5000)
    
    def buscar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            aplicar_strip = [True, True, True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.CondicionesInicialesManejador, mostrar_func=self.mostrar_condiciones_iniciales, like=True)
        except Exception as e:
            self.statusbar.showMessage(f"Error al buscar datos de condiciones iniciales: {e}", 5000)
    
    def buscar_unidades_nombre_data(self):
        # Verifica si nombre_data_experimental está vacío
        if not self.nombre_data_experimental.text().strip():
            self.ui.temp_ci_l.setText("T")
            self.ui.t_ci_l.setText("t")
            self.ui.p_ci_l.setText("P")
            self.ui.pi_ci_l.setText("P")
            self.ui.t_dc_label.setText("t")
            self.ui.c_dc_label.setText("[C]")
            return  # Termina la ejecución del método aquí
        try:
            filtros = {"nombre_data": self.nombre_data_experimental.text()}
            registros = self.RegistroUnidadesManejador.consultar(filtros=filtros)
            if registros:  # Verifica si la lista no está vacía
                # Accede al atributo 'id' del registro directamente

                self.ui.temp_ci_l.setText(str(registros[0].temperatura))
                self.ui.t_ci_l.setText(str(registros[0].tiempo))
                self.ui.p_ci_l.setText(str(registros[0].presion))
                self.ui.pi_ci_l.setText(str(registros[0].presion))
                self.ui.t_dc_label.setText(str(registros[0].tiempo))
                self.ui.c_dc_label.setText(str(registros[0].concentracion))
                self.ui.r_ds_edit.setText(str(registros[0].r))
                self.ui.id_registro_unidades_ds_edit.setText(str(registros[0].id))
            else:
                self.ui.temp_ci_l.setText("T")
                self.ui.t_ci_l.setText("t")
                self.ui.p_ci_l.setText("P")
                self.ui.pi_ci_l.setText("P")
                self.ui.c_dc_label.setText("[C]")
        except Exception as e:
            # Mostrar un mensaje de error en la interfaz de usuario
            self.statusbar.showMessage(f"Error al buscar registros por ID: {e}", 5000)
    
   
    # funciones crud para datos
    #metodos para crud de datos cineticos
    def agregar_dato(self):
        try:
            columnas = ["tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
            elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
            tipos = [float, float, float, float, str, int, str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.DatosCineticosManejador,clase_objeto=DatosIngresadosCineticos,limpiar_func=self.limpiar_formulario_agregar,buscar_func=self.buscar_dato)
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)
       
    def limpiar_formulario(self):
        elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def limpiar_formulario_agregar(self):
        elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.especie_quimica, self.id_condiciones_iniciales]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def seleccionar_dato(self):
        columnas = ["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
        elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_datos, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Dato seleccionado id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
            
    def actualizar_dato(self):
        try:
            columnas = ["tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
            elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
            tipos = [float, float, float, float, str, int, str, str, str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_datos,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.DatosCineticosManejador,clase_objeto=DatosIngresadosCineticos,limpiar_func=self.limpiar_formulario,buscar_func=self.buscar_dato)
        except ValueError as e:
            self.statusbar.showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def borrar_dato(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.DatosCineticosManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(self.tabla_datos, borrar_resultado, "¿Estás seguro de eliminar el dato?", "Dato eliminado correctamente", "Hubo un problema al eliminar el dato", self.DatosCineticosManejador.consultar, self.refrescar_datos_tabla, self.buscar_dato)
            self.statusbar.showMessage(f"Registro cinético eliminado de tabla_datos id: {id}", 5000)
    
    def buscar_dato(self):
        try:
            columnas = ["tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
            elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
            aplicar_strip = [True, True, True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.DatosCineticosManejador, mostrar_func=self.mostrar_datos_tabla, like=True)
        except Exception as e:
            self.statusbar.showMessage(f"Error al buscar datos cinéticos: {e}", 5000)

    def mostrar_datos_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

    def actualizar_valor_celda_datos(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos, self.DatosCineticosManejador, fila, columna)

    # funciones especiales para datos
    def establecer_fecha_sistema(self):
        self.componentes_auxiliares.establecer_fecha_sistema(self.fecha_ds_edit)
        self.componentes_auxiliares.establecer_fecha_sistema(self.ui.fecha_rde_edit)


    def ajustes_visuales_tabla(self):
        self.componentes_auxiliares.ajustar_tabla(self.tabla_registro_data_experimental, ["id", "Nombre\ndata", "Fecha", "Detalle"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_reaccion_quimica, ["id","Especie\nQuimica", "Fórmula", "Coeficiente\nEstequiométrico", "Detalle", "Tipo\nEspecie", "Nombre\nreaccion"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_registro_unidades, ["id", "Presión", "Temperatura", "Tiempo", "Concentración", "Energía", "R", "Nombre\ndata"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_condiciones_iniciales, ["id", "Temperatura", "Tiempo", "Presión\nTotal", "Presión\nParcial", "Fracción\nMolar", "Especie\nQuímica", "Tipo\nEspecie", "Detalle", "Nombre\ndata"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos, ["id", "Tiempo", "Concentración", "Otra\nPropiedad", "Conversión\nReactivo\nLimitante", "Tipo\nEspecie", "id\nCondiciones\nIniciales", "Nombre\ndata", "Nombre\nreacción", "Especie\nquímica"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos_salida, ["id", "Nombre\ndata\nsalida", "Fecha", "id\nNombre\ndata", "id\nCondiciones\niniciales", "id\nRegistro\nunidades", "R\nutilizada", "Nombre\ndata", "Nombre\nreacción", "Δn\nreacción", "ε\nreactivo\nlimitante", "Tipo\nespecie", "Especie\nquímica", "Constante\ncinética", "Orden\nreacción", "Modelo\ncinético", "Tipo\ncálculo", "Detalles"])
        self.componentes_auxiliares.ocultar_columnas(self.tabla_datos_salida, [11,12,13,14,15,16,17,18,19])
        #self.componentes_auxiliares.ajustar_tabla(self.tabla_datos_salida_arrhenius, ["id","Nombre\ncaso","id\nNombre\ndata\nsalida","id\nNombre\ndata","Fecha","Temperatura","1/Temperatura absoluta","Constante\ncinética","ln\nConstante\ncinética\n0","Energía\nactivación\nR","R\nutilizada","Energía\nactivación","Constante\ncinética\n0","ln\nConstante\ncinética","Detalles"])


    
    def cargar_datos_json_unidades_temperatura(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "unidades_temperatura", self.temperatura_box, "simbolo")
        #self.temperatura_box.addItem("otro") # Agregar la opción "otro" al final de la lista
        
    def cargar_datos_json_unidades_presion(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "unidades_presion", self.presion_box, "simbolo")
        #self.presion_box.addItem("otro") # Agregar la opción "otro" al final de la lista
    
    def cargar_datos_json_unidades_tiempo(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "unidades_tiempo", self.tiempo_box, "simbolo")
        #self.tiempo_box.addItem("otro") # Agregar la opción "otro" al final de la lista
    
    def cargar_datos_json_unidades_concentracion(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "unidades_concentracion", self.concentracion_box, "simbolo")
        #self.concentracion_box.addItem("otro") # Agregar la opción "otro" al final de la lista
    
    def cargar_datos_json_unidades_energia(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "unidades_energia", self.energia_box, "simbolo")
        #self.energia_box.addItem("otro") # Agregar la opción "otro" al final de la lista
    
    def cargar_datos_json_constante_r(self, archivo):
        #self.metodos_comunes.cargar_datos_json_box(archivo, "constante_R_gases", self.r_box, "valor")
        self.metodos_comunes.cargar_datos_json_box_group_box(archivo, "constante_R_gases", self.r_box, "valor",self.ui.groupBox_11)
        #self.constante_r_box.addItem("otro") # Agregar la opción "otro" al final de la lista
    
    def actualizar_lineedit_unidades_temperatura(self):
        self.metodos_comunes.actualizar_lineedit(self.temperatura_box, self.temperatura_u_edit,True)
        
    def actualizar_lineedit_unidades_presion(self):
        self.metodos_comunes.actualizar_lineedit(self.presion_box, self.presion_u_edit,True)
    
    def actualizar_lineedit_unidades_tiempo(self):
        self.metodos_comunes.actualizar_lineedit(self.tiempo_box, self.tiempo_u_edit,True)
    
    def actualizar_lineedit_unidades_concentracion(self):
        self.metodos_comunes.actualizar_lineedit(self.concentracion_box, self.concentracion_u_edit,True)
    
    def actualizar_lineedit_unidades_energia(self):
        self.metodos_comunes.actualizar_lineedit(self.energia_box, self.energia_u_edit,True)
    
    def actualizar_lineedit_constante_r(self):
        self.metodos_comunes.actualizar_lineedit(self.r_box, self.r_u_edit,True)
        self.actualizar_lineedit_unidades()

    def actualizar_lineedit_unidades(self):
        # Obtener el objeto JSON seleccionado en el QComboBox de la constante R
        elemento_seleccionado = self.r_box.currentData()

        if isinstance(elemento_seleccionado, dict):
            # Actualizar los QLineEdit con las unidades correspondientes
            self.presion_u_edit.setText(elemento_seleccionado.get('presion', ''))
            self.concentracion_u_edit.setText(elemento_seleccionado.get('concentracion', ''))
            self.energia_u_edit.setText(elemento_seleccionado.get('energia', ''))
        else:
            # Limpiar los QLineEdit si no hay selección o datos
            self.energia_u_edit.clear()
            self.concentracion_u_edit.clear()
            self.presion_u_edit.clear()
    
    # se requiere inyectar el catálogo y a donde dirigir la información
    def cargar_datos_json_tipo_especie(self, archivo):
        self.metodos_comunes.cargar_datos_json_box(archivo, "tipo_especie_catalogo", self.tipo_especie_rq_box, "Descripcion")
        self.metodos_comunes.cargar_datos_json_box(archivo, "tipo_especie_catalogo", self.tipo_especie_ci_box, "Descripcion")
        self.metodos_comunes.cargar_datos_json_box(archivo, "tipo_especie_catalogo", self.tipo_especie_dc_box, "Descripcion")

    #empuja la seleccion al line edit
    def actualizar_lineedit_tipo_especie(self):
        self.metodos_comunes.actualizar_lineedit(self.tipo_especie_rq_box, self.tipo_especie_rq,True)
        self.metodos_comunes.actualizar_lineedit(self.tipo_especie_ci_box, self.tipo_especie_ci,True)
        self.metodos_comunes.actualizar_lineedit(self.tipo_especie_dc_box, self.tipo_especie,True)

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
            QMessageBox.information(self, "Información", "Seleccione en la pestaña de Datos cinéticos el valor inicial correspondiente o si lo conoce digítelo ", QMessageBox.StandardButton.Ok)
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
    #similar a seleccionar reaccion qumica
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
            QMessageBox.information(self, "Información", "Dirijase a la pestaña de reacción química y seleccione una fila", QMessageBox.StandardButton.Ok)
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

    
        #calcula la conversion de XA
    def calcular_conversion(self):
        try:
            funciones = Funciones()
            tipo_especie = self.tipo_especie.text().strip()

            if not tipo_especie:
                raise ValueError("Seleccione el 'Tipo de Especie' y verifique que no esté vacío. Por favor, llénelo.")

            #conversion_reactivo_limitante_dado_producto(self,concentracion_producto,concentracion_inicial_producto,concentracion_inicial_reactivo_limitante, coeficiente_producto, coeficiente_reactivo_limitante )
            #(concentracion_producto - concentracion_inicial_producto) / ((coeficiente_producto / coeficiente_reactivo_limitante) * concentracion_inicial_reactivo_limitante)
            if tipo_especie == "producto":
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
                concentracion = float(self.concentracion.text())
                concentracion_inicial_producto = float(self.concentracion_inicial_producto.text())
                concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
                coeficiente_estequiometro_producto = float(self.coeficiente_estequiometro_producto.text())
                coeficiente_estequiometro_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
                xa = funciones.conversion_reactivo_limitante_dado_producto(concentracion, concentracion_inicial_producto, concentracion_inicial_reactivo_limitante, coeficiente_estequiometro_producto, coeficiente_estequiometro_reactivo)
                self.conversion_reactivo_limitante.setText(str(xa))
                self.conversion_reactivo_limitante_calculo.setText(str(xa))
                self.statusbar.showMessage(f"La conversión del reactivo limitante es: {xa}", 5000)
            #conversion_reactivo_limitante(self,concentracion_inicial_reactivo_limitante,concentracion_reactivo_limitante):
            # 1 - (concentracion_reactivo_limitante / concentracion_inicial_reactivo_limitante)
            elif tipo_especie == "reactivo_limitante":
                # Verificar individualmente cada campo y lanzar una excepción si está vacío
                if not self.concentracion_inicial_reactivo_limitante.text().strip():
                    raise ValueError("El campo 'Concentración Inicial del Reactivo Limitante del panel' está vacío. Por favor, llénelo.")
                if not self.concentracion.text().strip():
                    raise ValueError("El campo 'Concentración de la pestaña datos cinéticos' está vacío. Por favor, llénelo.")

                # Continuar con la conversión a float y el cálculo
                concentracion_inicial_reactivo_limitante = float(self.concentracion_inicial_reactivo_limitante.text())
                concentracion_reactivo_limitante = float(self.concentracion.text())
                xa = funciones.conversion_reactivo_limitante(concentracion_inicial_reactivo_limitante, concentracion_reactivo_limitante)
                self.conversion_reactivo_limitante.setText(str(xa))
                self.conversion_reactivo_limitante_calculo.setText(str(xa))
                self.statusbar.showMessage(f"La conversión del reactivo limitante es: {xa}", 5000)

            else:
                raise ValueError("Tipo de especie no reconocido.")
        
        except ValueError as e:
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    #calcula A con Xa y la Concentracion inicial A = A0 * (1 - XA)
    #concentracion_inicial_reactivo*(1-conversion_reactivo_limitante)
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
            self.concentracion_reactivo_limitante_calculo.setText(str(A))
            # Obtener el tipo de especie
            tipo_especie = self.tipo_especie.text().strip()

            # Asignar el valor a self.concentracion solo si tipo_especie es "reactivo_limitante" o está vacío
            if tipo_especie == "reactivo_limitante" or not tipo_especie:
                self.concentracion.setText(str(A))           
            
            self.statusbar.showMessage(f"La conversión del reactivo limitante es: {A}", 5000)
        
        except ValueError as e:
            # Mostrar el mensaje de error específico para el campo vacío
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    #Producto = Producto_0 + (coeficiente_producto / a) * (A0 * XA)
    #concentracion_Producto(self,Producto_0, coeficiente_producto, a, XA, A0):
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
            producto = funciones.concentracion_producto(concentracion_inicial_producto, coeficiente_estequiometro_producto, coeficiente_estequiometro_reactivo, conversion_reactivo_limitante, concentracion_inicial_reactivo_limitante)
            #print(producto)

            self.concentracion_producto_calculo.setText(str(producto))
            self.statusbar.showMessage(f"La concentración del producto dada la conversión es: {producto}", 5000)
            
            # Obtener el tipo de especie
            tipo_especie = self.tipo_especie.text().strip()

            # Asignar el valor a self.concentracion solo si tipo_especie es "producto" o está vacío
            if tipo_especie == "producto" or not tipo_especie:
                self.concentracion.setText(str(producto))  

        except ValueError as e:
            # Mostrar el mensaje de error específico para el campo vacío
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)
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
                raise ValueError("Verifique que haya seleccionado una reacción química válida. Por favor, seleccione una.")
          
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
        except ValueError as e:
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"Error: {e}", 5000)
        except Exception as e:
            print(f"Ocurrió un error al calcular delta_n: {e}")
            self.statusbar.showMessage("Error al calcular")

    def calcular_epsilon_reactivo_limitante(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.fraccion_molar_ci.text():
                raise ValueError("El campo 'Fracción Molar de condiciones iniciales' está vacío. Por favor, llénelo.")
                
            if not self.delta_n_rq.text():
                raise ValueError("El campo 'Delta n de la reacción quimica' está vacío. Por favor, llénelo.")
                
            if not self.coeficiente_estequiometro_reactivo.text():
                raise ValueError("El campo del 'Coeficiente Estequiométrico del Reactivo' está vacío. Por favor, llénelo.")

            
            fraccion_molar_inicial = float(self.fraccion_molar_ci.text())
            delta_n = float(self.delta_n_rq.text())
            coeficiente_estequiometrico_reactivo = float(self.coeficiente_estequiometro_reactivo.text())
            epsilon_a = funciones.calcular_epsilon_A(fraccion_molar_inicial, delta_n, coeficiente_estequiometrico_reactivo)
            self.epsilon_reactivo_limitante_calculo.setText(str(epsilon_a))
            self.epsilon_rl_ds_edit.setText(str(epsilon_a))
            self.statusbar.showMessage(f"epsilon del reactivo limintante es e_rl= {epsilon_a} .", 5000)
        except ValueError as e:
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"Error: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)
            
    def calcular_conversion_reactivo_limitante_dado_epsilon_a_presion(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.otra_propiedad_inicial.text():
                raise ValueError("El campo 'Propiedad Inicial del panel' está vacío. Por favor, llénelo.")
                
            if not self.otra_propiedad.text():
                raise ValueError("El campo 'Propiedad de la pestaña datos cinéticos' está vacío. Por favor, llénelo.")
                
            if not self.epsilon_reactivo_limitante_calculo.text():
                raise ValueError("El campo 'Epsilon Reactivo Limitante del panel' está vacío. Por favor, llénelo.")
                
            
            otra_propiedad_inicial = float(self.otra_propiedad_inicial.text())
            otra_propiedad = float(self.otra_propiedad.text())
            epsilon_a = float(self.epsilon_reactivo_limitante_calculo.text())
            gas_conversion_componente_principal = funciones.gas_conversion_componente_principal_epsilon_a(otra_propiedad, otra_propiedad_inicial, epsilon_a)
            
            self.conversion_reactivo_limitante_gas.setText(str(gas_conversion_componente_principal))
            self.statusbar.showMessage(f" La conversion del reactivo limitante es x reactivo limitante= {gas_conversion_componente_principal} .", 5000)
        except ValueError as e:
            QMessageBox.warning(self, "Revisar", f" {e}", QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"Error al convertir a float: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    def calcular_conversion_reactivo_limitante_otra_propiedad(self,aumento):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.otra_propiedad_inicial.text():
                raise ValueError("El campo 'Propiedad Inicial del panel' está vacío. Por favor, llénelo.")
                
            if not self.otra_propiedad.text():
                raise ValueError("El campo 'Propiedad de la pestaña datos cinéticos' está vacío. Por favor, llénelo.")
            
            otra_propiedad_inicial = float(self.otra_propiedad_inicial.text())
            otra_propiedad = float(self.otra_propiedad.text())
            
            # Verificar si el campo epsilon_reactivo_limitante_calculo está vacío
            if self.epsilon_reactivo_limitante_calculo.text():
                epsilon_a = float(self.epsilon_reactivo_limitante_calculo.text())
            else:
                epsilon_a = None
            
            # Realizar el cálculo de conversión del reactivo limitante
            conversion_reactivo_limitante = funciones.propiedad_conversion_reactivo_limitante_fluctuante(
                propiedad=otra_propiedad,
                propiedad_inicial=otra_propiedad_inicial,
                epsilon_a=epsilon_a,
                aumento=aumento
            )
            
            self.ui.conversion_RL_otra_propiedad.setText(str(conversion_reactivo_limitante))
            self.statusbar.showMessage(f"La conversión del reactivo limitante es: {conversion_reactivo_limitante}", 5000)
        except ValueError as e:
            QMessageBox.warning(self, "Revisar", f"{e}", QMessageBox.StandardButton.Ok)
            self.statusbar.showMessage(f"Error al convertir a float: {e}", 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)


    def calcular_concentracion_reactivo_limitante_dado_concentracion_gas(self):
        try:
            funciones = Funciones()
            # Verificar individualmente cada campo y mostrar un mensaje específico si está vacío
            if not self.temperatura_ci.text():
                raise ValueError("El campo 'Temperatura condiciones iniciales' está vacío. Por favor, llénelo.")

            if not self.presion_total_ci.text():
                raise ValueError("El campo 'Presión Total  de condiciones iniciales' está vacío. Por favor, llénelo.")
            if not self.fraccion_molar_ci.text():
                raise ValueError("El campo 'Fracción Molar  de condiciones iniciales' está vacío. Por favor, llénelo.")

            #verifica unidad de temperatura
            if not (self.ui.temp_ci_l.text().strip() or self.temperatura_u_edit.text()):
                raise ValueError("No se han agregado unidades. Por favor, Agrege")
            
            if not self.r_ds_edit.text():
                raise ValueError("El valor de R está vacío. Por favor, llénelo.")
           
            temperatura = float(self.temperatura_ci.text())
            presion_total = float(self.presion_total_ci.text())
            fraccion_molar = float(self.fraccion_molar_ci.text())
            unidad_temperatura = self.ui.temp_ci_l.text()
            
            concentracion_gas = funciones.gas_concentracion_componente(1, fraccion_molar, presion_total, self.r_ds_edit, temperatura, unidad_temperatura)
            print(concentracion_gas)
            self.concentracion_reactivo_limitante_calculo_2.setText(str(concentracion_gas))
            self.statusbar.showMessage(f"La concentración inicial del gas reactivo limitante es: {concentracion_gas}", 5000)
            
        except ValueError as e:
            QMessageBox.information(self, "Error", str(e), QMessageBox.StandardButton.Ok)

            self.statusbar.showMessage(str(e), 5000)
        except Exception as e:
            self.statusbar.showMessage(f"Error inesperado: {e}", 5000)

    def completar_campos_vacios(self):
        # Obtener valores de los campos de referencia
        delta_n_rq_valor = self.delta_n_rq.text()
        epsilon_rl_calculo_valor = self.epsilon_reactivo_limitante_calculo.text()
        
        # Verificar y completar delta_n_ds_edit
        if not self.delta_n_ds_edit.text():
            if delta_n_rq_valor:
                self.delta_n_ds_edit.setText(delta_n_rq_valor)
            else:
                self.delta_n_ds_edit.setText('0')
        
        # Verificar y completar epsilon_rl_ds_edit
        if not self.epsilon_rl_ds_edit.text():
            if epsilon_rl_calculo_valor:
                self.epsilon_rl_ds_edit.setText(epsilon_rl_calculo_valor)
            else:
                self.epsilon_rl_ds_edit.setText('0')

    # crud datos de salida
    def agregar_datos_salida(self):
        try:
            columnas= ["nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante"]
            elementos_visuales= [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit]
            tipos = [str, str, int, int, int, float, str, str, float, float]
            self.metodos_comunes.agregar_datos_db(columnas, elementos_visuales, tipos, self.RegistroDatosSalidaManejador,DatosSalida,self.limpiar_formulario_datos_salida, self.buscar_datos_salida) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos de salida: {e}", QMessageBox.StandardButton.Ok)
    
    def actualizar_datos_salida(self):
        try:
            columnas= ["nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante"]
            elementos_visuales= [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit]
            tipos = [str, str, int, int, int, float, str, str, float, float]
            self.metodos_comunes.actualizar_datos_db(self.tabla_datos_salida,columnas, elementos_visuales, tipos, self.RegistroDatosSalidaManejador,DatosSalida,self.limpiar_formulario_datos_salida, self.buscar_datos_salida) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar los datos de salida: {e}", QMessageBox.StandardButton.Ok)

    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados)
    
    def seleccionar_datos_salida(self):
        columnas = ["id", "nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", "tipo_calculo", "detalles"]
        elementos_visuales = [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, self.tipo_calculo_ds_edit, self.detalles_ds_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_datos_salida, columnas, elementos_visuales)
        if datos:
            self.statusbar.showMessage(f"Set de Datos de Salida seleccionados id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
        
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
            self.statusbar.showMessage(f"Datos de salida con id {id} eliminados", 5000)

    def buscar_datos_salida(self):
        try:
            columnas = ["nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie, especie_quimica, constante_cinetica, orden_reaccion, modelo_cinetico, tipo_calculo, detalles"]
            elementos_visuales = [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, self.tipo_calculo_ds_edit, self.detalles_ds_edit]
            aplicar_strip = []
            self.metodos_comunes.buscar_datos_db(columnas, elementos_visuales,aplicar_strip, self.RegistroDatosSalidaManejador, self.mostrar_datos_tabla_salida,True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al buscar los datos de salida: {e}", QMessageBox.StandardButton.Ok)
    
    def limpiar_formulario_datos_salida(self):
        elementos_visuales = [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, self.tipo_calculo_ds_edit, self.detalles_ds_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def limpiar_formulario_datos_salida_agregar(self):
        elementos_visuales = [self.nombre_ds_edit, self.fecha_ds_edit, self.id_condiciones_iniciales_ds_edit, self.r_ds_edit, self.tipo_especie_ds_edit, self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, self.tipo_calculo_ds_edit, self.detalles_ds_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def actualizar_valor_celda_datos_salida(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos_salida, self.RegistroDatosSalidaManejador, fila, columna)


    def seleccionar_archivo_datos(self):
            # Abre un cuadro de diálogo para seleccionar el archivo de datos
        fileName, _ = QFileDialog.getOpenFileName(self.parent, "Selecciona el archivo de datos", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if fileName:
            self.insertar_datos_cineticos_archivo(fileName)

    def insertar_datos_cineticos_archivo(self, ruta_archivo):
        # Función auxiliar para leer el archivo con un delimitador específico
        def leer_archivo_con_delimitador(ruta_archivo, delimitador):
            try:
                return pd.read_csv(ruta_archivo, delimiter=delimitador)
            except pd.errors.ParserError:
                return None

        # Leer el archivo
        df = None
        if ruta_archivo.endswith('.csv'):
            df = leer_archivo_con_delimitador(ruta_archivo, ';')
            if df is None:
                df = leer_archivo_con_delimitador(ruta_archivo, ',')
        elif ruta_archivo.endswith('.xlsx'):
            df = pd.read_excel(ruta_archivo)
        else:
            QMessageBox.critical(self.parent, "Error", "Formato de archivo no soportado", QMessageBox.StandardButton.Ok)
            return

        if df is None:
            QMessageBox.critical(self.parent, "Error", "Error al leer el archivo CSV con ambos delimitadores (';' y ',')", QMessageBox.StandardButton.Ok)
            return

        # Verificar los nombres de las columnas
        columnas_esperadas = ['tiempo', 'concentracion', 'otra_propiedad', 'conversion_reactivo_limitante', 
                            'tipo_especie', 'id_condiciones_iniciales', 'nombre_data', 
                            'nombre_reaccion', 'especie_quimica']
        columnas_faltantes = [col for col in columnas_esperadas if col not in df.columns]

        if columnas_faltantes:
            QMessageBox.critical(self.parent, "Error", f"Faltan las siguientes columnas en el archivo: {', '.join(columnas_faltantes)}", QMessageBox.StandardButton.Ok)
            return

        # Iterar sobre cada fila del DataFrame
        for _, fila in df.iterrows():
            # Convertir los valores a cadenas y reemplazar comas por puntos en las columnas numéricas
            fila['tiempo'] = str(fila['tiempo']).replace(',', '.')
            fila['concentracion'] = str(fila['concentracion']).replace(',', '.')
            fila['otra_propiedad'] = str(fila['otra_propiedad']).replace(',', '.')
            fila['conversion_reactivo_limitante'] = str(fila['conversion_reactivo_limitante']).replace(',', '.')

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
                    QMessageBox.critical(self.parent, "Error", "Hubo un problema al agregar los datos", QMessageBox.StandardButton.Ok)
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Se produjo un error al agregar los datos: {e}", QMessageBox.StandardButton.Ok)

        QMessageBox.information(self.parent, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
        self.buscar_dato()  # Refrescar la tabla con los nuevos datos al cargar un CSV o Excel



    def cargar_datos_btn_click(self):
        # Abrir la ventana de diálogo para seleccionar el archivo
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")

        # Si el usuario seleccionó un archivo (es decir, no hizo clic en "Cancelar")
        if ruta_archivo:
            # Llamar a tu función con la ruta del archivo seleccionado
            self.insertar_datos_cineticos_archivo(ruta_archivo)

    def calculos_adicionales(self):
        # Lista de nombres de elementos a alternar visibilidad
        elementos_ocultos = ['groupBox_2', 'groupBox_3', 'groupBox_4', 'groupBox_5','group_box_computo']
        
        for nombre_elemento in elementos_ocultos:
            elemento = getattr(self.ui, nombre_elemento)  # Obtiene el objeto del elemento por su nombre
            if elemento.isVisible():
                elemento.hide()  # Oculta el elemento si está visible
            else:
                elemento.show()  # Muestra el elemento si está oculto

    def generar_respaldo(self):
        try:
            # Obtén la ruta del directorio actual
            current_dir = os.path.dirname(os.path.abspath(__file__))

            metodos_comunes = Servicios()
            dir_db = r"config\config.json"
            db_path = metodos_comunes.cargar_configuracion_json(dir_db, "db_path")

            engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
            Session = sessionmaker(bind=engine)
            session = Session()

            # Crear una instancia de la clase Respaldos y guardar el archivo
            respaldos = Respaldos(session)
            respaldos.guardar_archivo()
        except Exception as e:
            #print(f"Ocurrió un error al generar el respaldo: {e}")
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar el respaldo: {e}", QMessageBox.StandardButton.Ok)

    def reiniciar_aplicacion(self):
        self.componentes_auxiliares.reiniciar_aplicacion()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlujoDatos()
    window.show()
    sys.exit(app.exec())

#nota falta para datos otros calcular x o A a partir de su propia concentracion y su propio dato inicial
#agregar calculos para XA solo con XA