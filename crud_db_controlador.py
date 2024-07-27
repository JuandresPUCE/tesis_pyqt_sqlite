import os
import sys
import subprocess
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

#importe ui de la ventana principal
from crud_db_vista import Ui_MainWindow

# metodos comunes
from servicios import *
from componentes_auxiliares import *

#respaldos 
from respaldos import Respaldos


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
        self.init_ui_elementos_arrhenius()

        # Inicializar conexiones de señales y ranuras
        self.init_control_botones_datos()
        self.init_control_botones_experimental()
        self.init_control_botones_ci()
        self.init_control_botones_rq()
        self.init_control_botones_u()
        self.init_control_botones_ds()
        self.init_control_botones_arrhenius()

        # Cargar datos iniciales
        self.buscar_dato()
        self.buscar_registros()
        self.buscar_condiciones_iniciales()
        self.buscar_reaccion_quimica()
        self.buscar_unidades()
        self.buscar_datos_salida()
        self.buscar_datos_salida_arrhenius()

        self.ajustes_visuales_tabla()

        self.data_lista_btn = self.ui.data_lista_btn
        self.data_lista_btn.clicked.connect(self.reiniciar_aplicacion)

         # Conectar la señal cellChanged para actualizar la base de datos cuando cambie una celda
        self.tabla_datos.cellChanged.connect(self.actualizar_valor_celda_datos)
        self.tabla_registro_data_experimental.cellChanged.connect(self.actualizar_valor_celda_registro)
        self.tabla_condiciones_iniciales.cellChanged.connect(self.actualizar_valor_celda_ci)
        self.tabla_reaccion_quimica.cellChanged.connect(self.actualizar_valor_celda_reaccion)
        self.tabla_registro_unidades.cellChanged.connect(self.actualizar_valor_celda_unidades)
        self.tabla_datos_salida.cellChanged.connect(self.actualizar_valor_celda_datos_salida)
        self.tabla_datos_salida_arrhenius.cellChanged.connect(self.actualizar_valor_celda_datos_salida_arrhenius)
        

    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()
        self.RegistroDatosSalidaArrhenius = RegistroDatosSalidaArrhenius()           

        self.metodos_comunes = Servicios(self)
        self.componentes_auxiliares = ComponentesAuxiliares()

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

    def init_ui_elementos_arrhenius(self):
        self.nombre_caso_a_edit = self.ui.nombre_caso_a_edit
        self.fecha_a_edit = self.ui.fecha_a_edit
        self.id_nombre_data_salida_a=self.ui.id_nombre_data_salida_a
        self.id_nombre_data_a_edit = self.ui.id_nombre_data_a_edit
        self.temperatura_a_edit = self.ui.temperatura_a_edit
        self.rtemperatura_a_edit = self.ui.rtemperatura_a_edit
        self.constante_cinetica_a_edit = self.ui.constante_cinetica_a_edit
        self.ln_constante_cinetica_0_a_edit = self.ui.ln_constante_cinetica_0_a_edit
        self.energia_activacion_r_a_edit = self.ui.energia_activacion_r_a_edit
        self.energia_activacion_a_edit = self.ui.energia_activacion_a_edit
        self.constante_cinetica_0_a_edit = self.ui.constante_cinetica_0_a_edit
        self.ln_constante_cinetica_a_edit = self.ui.ln_constante_cinetica_a_edit
        self.r_a_edit = self.ui.r_a_edit
        self.detalles_a_edit = self.ui.detalles_a_edit

        #botones de arrhenius
        self.agregar_a_btn = self.ui.agregar_a_btn
        self.actualizar_a_btn = self.ui.actualizar_a_btn
        self.seleccionar_a_btn = self.ui.seleccionar_a_btn
        self.buscar_a_btn = self.ui.buscar_a_btn
        self.limpiar_a_btn = self.ui.limpiar_a_btn
        self.borrar_a_btn = self.ui.borrar_a_btn

        #tabla de arrhenius
        self.tabla_datos_salida_arrhenius = self.ui.datos_salida_tabla_2
        self.tabla_datos_salida_arrhenius.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame_a.findChildren(QPushButton)

    
    def init_control_botones_arrhenius(self):
        self.agregar_a_btn.clicked.connect(self.agregar_datos_salida_arrhenius)
        self.actualizar_a_btn.clicked.connect(self.actualizar_datos_salida_arrhenius)
        self.seleccionar_a_btn.clicked.connect(self.seleccionar_datos_salida_arrhenius)
        self.borrar_a_btn.clicked.connect(self.borrar_datos_salida_arrhenius)
        self.limpiar_a_btn.clicked.connect(self.limpiar_formulario_datos_salida_arrhenius)
        self.buscar_a_btn.clicked.connect(self.buscar_datos_salida_arrhenius)
  

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
        self.tabla_datos_salida.clearContents()
        self.tabla_datos_salida_arrhenius.clearContents()

                
        # Buscar los datos nuevamente y mostrarlos en la tabla
        self.buscar_dato()
        self.buscar_registros()
        self.buscar_condiciones_iniciales()
        self.buscar_reaccion_quimica()
        self.buscar_unidades()
        self.buscar_datos_salida()
        self.buscar_datos_salida_arrhenius()

    #metodos para desactivar y activar botones
    def boton_desactivado(self):
        for button in self.lista_botones:
            button.setDisabled(True)

    def boton_activado(self):
        for button in self.lista_botones:
            button.setDisabled(False)

    def ajustes_visuales_tabla(self):
        self.componentes_auxiliares.ajustar_tabla(self.tabla_registro_data_experimental, ["id", "Nombre\ndata", "Fecha", "Detalle"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_reaccion_quimica, ["id","Especie\nQuimica", "Fórmula", "Coeficiente\nEstequiométrico", "Detalle", "Tipo\nEspecie", "Nombre\nreaccion"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_registro_unidades, ["id", "Presión", "Temperatura", "Tiempo", "Concentración", "Energía", "R", "Nombre\ndata"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_condiciones_iniciales, ["id", "Temperatura", "Tiempo", "Presión\nTotal", "Presión\nParcial", "Fracción\nMolar", "Especie\nQuímica", "Tipo\nEspecie", "Detalle", "Nombre\ndata"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos, ["id", "Tiempo", "Concentración", "Otra\nPropiedad", "Conversión\nReactivo\nLimitante", "Tipo\nEspecie", "id\nCondiciones\nIniciales", "Nombre\ndata", "Nombre\nreacción", "Especie\nquímica"])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos_salida, ["id", "Nombre\ndata\nsalida", "Fecha", "id\nNombre\ndata", "id\nCondiciones\niniciales", "id\nRegistro\nunidades", "R\nutilizada", "Nombre\ndata", "Nombre\nreacción", "Δn\nreacción", "ε\nreactivo\nlimitante", "Tipo\nespecie", "Especie\nquímica", "Constante\ncinética", "Orden\nreacción", "Modelo\ncinético", "Tipo\ncálculo", "Detalles"])
        #self.componentes_auxiliares.ocultar_columnas(self.tabla_datos_salida, [11,12,13,14,15,16,17,18,19])
        self.componentes_auxiliares.ajustar_tabla(self.tabla_datos_salida_arrhenius, ["id","Nombre\ncaso","id\nNombre\ndata\nsalida","id\nNombre\ndata","Fecha","Temperatura","1/Temperatura absoluta","Constante\ncinética","ln\nConstante\ncinética\n0","Energía\nactivación\nR","R\nutilizada","Energía\nactivación","Constante\ncinética\n0","ln\nConstante\ncinética","Detalles"])
        

   
    #metodos para crud de datos cineticos
    def agregar_dato(self):
        try:
            columnas = ["tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
            elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
            tipos = [float, float, float, float, str, int, str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.DatosCineticosManejador,clase_objeto=DatosIngresadosCineticos,limpiar_func=self.limpiar_formulario,buscar_func=self.buscar_dato)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def limpiar_formulario(self):
        elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)

    def seleccionar_dato(self):
        columnas = ["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
        elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_datos, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Dato seleccionado id: {datos['id']}", 5000)
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
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def borrar_dato(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.DatosCineticosManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(self.tabla_datos, borrar_resultado, "¿Estás seguro de eliminar el dato?", "Dato eliminado correctamente", "Hubo un problema al eliminar el dato", self.DatosCineticosManejador.consultar, self.refrescar_datos_tabla, self.buscar_dato)
            self.statusBar().showMessage(f"Registro cinético eliminado de tabla_datos id: {id}", 5000)
    
    def buscar_dato(self):
        try:
            columnas = ["tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
            elementos_visuales = [self.tiempo, self.concentracion, self.otra_propiedad, self.conversion_reactivo_limitante, self.tipo_especie, self.id_condiciones_iniciales, self.nombre_data, self.nombre_reaccion, self.especie_quimica]
            aplicar_strip = [True, True, True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.DatosCineticosManejador, mostrar_func=self.mostrar_datos_tabla, like=True)
        except Exception as e:
            self.statusBar().showMessage(f"Error al buscar datos cinéticos: {e}", 5000)    

    def mostrar_datos_tabla(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla(self.tabla_datos, resultados)

    def actualizar_valor_celda_datos(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos, self.DatosCineticosManejador, fila, columna)

    # funciones crud para registro de data experimental
    # Registro de data experimental
    def mostrar_registros(self, registros):
        self.metodos_comunes.mostrar_registros(self.tabla_registro_data_experimental, registros)

    def agregar_registro_data_experimental(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            tipos = [str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDataExperimentalManejador,clase_objeto=RegistroDataExperimental,limpiar_func=self.limpiar_formulario_registro_data_experimental,buscar_func=self.buscar_registros)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)
   
    def limpiar_formulario_registro_data_experimental(self):
        elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def seleccionar_registro_data_experimental(self):
        columnas = ["id", "nombre_data", "fecha", "detalle"]
        elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_registro_data_experimental, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Registro seleccionado id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
    
    def actualizar_registro_data_experimental(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            tipos = [str, str, str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_registro_data_experimental,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDataExperimentalManejador,clase_objeto=RegistroDataExperimental,limpiar_func=self.limpiar_formulario_registro_data_experimental,buscar_func=self.buscar_registros)
        except ValueError as e:
            #QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}",5000)       

    def actualizar_valor_celda_registro(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_data_experimental, self.RegistroDataExperimentalManejador, fila, columna)

    def borrar_registro_data_experimental(self):
        fila_seleccionada = self.tabla_registro_data_experimental.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_registro_data_experimental.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroDataExperimentalManejador.borrar(id)
            self.metodos_comunes.borrar_elemento(self.tabla_registro_data_experimental,borrar_resultado,"¿Estás seguro de eliminar el registro?","Registro eliminado correctamente","Hubo un problema al eliminar el registro", self.RegistroDataExperimentalManejador.consultar, self.refrescar_datos_tabla, self.buscar_registros)
            self.statusBar().showMessage(f"Registro eliminado de tabla_registro_data_experimental id: {id}", 5000)
    
    def buscar_registros(self):
        try:
            columnas = ["nombre_data", "fecha", "detalle"]
            elementos_visuales = [self.nombre_data_experimental, self.fecha_data_experimental, self.detalle_data_experimental]
            aplicar_strip = [True, True, False]  # Ejemplo de configuración para aplicar strip solo a los dos primeros campos
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.RegistroDataExperimentalManejador, mostrar_func=self.mostrar_registros, like=True)
        except Exception as e:
            #print(f"Error al buscar registros: {e}")
            #Mostrar un mensaje de error en la interfaz de usuario
            self.statusBar().showMessage(f"Error al buscar registros: {e}" , 5000)


    # funciones crud para condiciones iniciales
    # Condiciones iniciales
    def mostrar_condiciones_iniciales(self, condiciones_iniciales):
        self.metodos_comunes.mostrar_condiciones_iniciales(self.tabla_condiciones_iniciales, condiciones_iniciales)
    
    def agregar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            tipos = [float, float, float, float, float, str, str, str,str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.CondicionesInicialesManejador,clase_objeto=CondicionesIniciales,limpiar_func=self.limpiar_formulario_ci,buscar_func=self.buscar_condiciones_iniciales)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def limpiar_formulario_ci(self):
        elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def seleccionar_condiciones_iniciales(self):
        columnas = ["id", "temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
        elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_condiciones_iniciales, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Condiciones iniciales seleccionadas id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return

    def actualizar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            tipos = [float, float, float, float, float, str, str, str,str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_condiciones_iniciales,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.CondicionesInicialesManejador,clase_objeto=CondicionesIniciales,limpiar_func=self.limpiar_formulario_ci,buscar_func=self.buscar_condiciones_iniciales)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

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
            self.statusBar().showMessage(f"Registro eliminado de tabla_condiciones_iniciales id: {id}", 5000)
    

    def buscar_condiciones_iniciales(self):
        try:
            columnas = ["temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
            elementos_visuales = [self.temperatura_ci, self.tiempo_ci, self.presion_total_ci, self.presion_parcial_ci, self.fraccion_molar_ci, self.especie_quimica_ci, self.tipo_especie_ci, self.detalle_ci, self.nombre_data_ci]
            aplicar_strip = [True, True, True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.CondicionesInicialesManejador, mostrar_func=self.mostrar_condiciones_iniciales, like=True)
        except Exception as e:
            self.statusBar().showMessage(f"Error al buscar datos de condiciones iniciales: {e}", 5000)
    
    
    # funciones crud para reaccion quimica
    # Reacción química
    def mostrar_reaccion_quimica(self, reaccion_quimica):
        self.metodos_comunes.mostrar_reacciones(self.tabla_reaccion_quimica, reaccion_quimica)
    
    def agregar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            tipos = [str, str, float, str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.ReaccionQuimicaManejador,clase_objeto=ReaccionQuimica,limpiar_func=self.limpiar_formulario_rq,buscar_func=self.buscar_reaccion_quimica)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def limpiar_formulario_rq(self):
        elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def seleccionar_reaccion_quimica(self):
        columnas = ["id", "especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
        elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
        datos = self.metodos_comunes.seleccionar_datos_visuales(self.tabla_reaccion_quimica, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Reacción química seleccionada id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return
        
    def actualizar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            tipos = [str, str, float, str, str, str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_reaccion_quimica,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.ReaccionQuimicaManejador,clase_objeto=ReaccionQuimica,limpiar_func=self.limpiar_formulario_rq,buscar_func=self.buscar_reaccion_quimica)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

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
            self.statusBar().showMessage(f"Registro eliminado de tabla_reaccion_quimica id: {id}", 5000)
    
    def buscar_reaccion_quimica(self):
        try:
            columnas = ["especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
            elementos_visuales = [self.especie_quimica_rq, self.formula_rq, self.coeficiente_estequiometro_rq, self.detalle_rq, self.tipo_especie_rq, self.nombre_reaccion_rq]
            aplicar_strip = [True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.ReaccionQuimicaManejador, mostrar_func=self.mostrar_reaccion_quimica, like=True)
        except Exception as e:
            self.statusBar().showMessage(f"Error al buscar datos de reacciones químicas: {e}", 5000)

    # funciones crud para registro de unidades
    # Registro de unidades
    def agregar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
            tipos = [str, str, str, str, str, float,str]
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroUnidadesManejador,clase_objeto=RegistroUnidades,limpiar_func=self.limpiar_formulario_unidades,buscar_func=self.buscar_unidades)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def actualizar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r" ,"nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
            tipos = [str, str, str, str, str, float,str]
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_registro_unidades,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroUnidadesManejador,clase_objeto=RegistroUnidades,limpiar_func=self.limpiar_formulario_unidades,buscar_func=self.buscar_unidades)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)

    def seleccionar_unidades(self):
        columnas = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_registro_unidades, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Set de Unidades seleccionada id: {datos['id']}", 5000)
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
            self.statusBar().showMessage(f"Registro eliminado de tabla_registro_unidades id: {id}", 5000)

    
    def buscar_unidades(self):
        try:
            columnas = ["presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
            elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.r_u_edit,self.nombre_data_u_edit]
            aplicar_strip = [True, True, True, True, True, True, True]  # Ejemplo de configuración para aplicar strip según sea necesario
            self.metodos_comunes.buscar_datos_db(columnas=columnas, elementos_visuales=elementos_visuales, aplicar_strip=aplicar_strip, manejador=self.RegistroUnidadesManejador, mostrar_func=self.mostrar_unidades, like=True)
        except Exception as e:
            self.statusBar().showMessage(f"Error al buscar datos de unidades: {e}", 5000)


    def actualizar_valor_celda_unidades(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_registro_unidades, self.RegistroUnidadesManejador, fila, columna)

    def mostrar_unidades(self,unidades):
        self.metodos_comunes.mostrar_unidades(self.tabla_registro_unidades, unidades)

    def limpiar_formulario_unidades(self):
        elementos_visuales = [self.presion_u_edit, self.temperatura_u_edit, self.tiempo_u_edit, self.concentracion_u_edit, self.energia_u_edit, self.nombre_data_u_edit, self.r_u_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def actualizar_valor_celda_datos_salida(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos_salida, self.RegistroDatosSalidaManejador, fila, columna)

    #refactor de tabla salida
    def mostrar_datos_tabla_salida(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_salida(self.tabla_datos_salida, resultados)
    
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

    def seleccionar_datos_salida(self):
        columnas = ["id", "nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", "tipo_calculo", "detalles"]
        elementos_visuales = [self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, self.tipo_calculo_ds_edit, self.detalles_ds_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_datos_salida, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Set de Datos de Salida seleccionados id: {datos['id']}", 5000)
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
            self.statusBar().showMessage(f"Datos de salida con id {id} eliminados", 5000)
    
    def actualizar_datos_salida(self):
        try:
            columnas = [
            "nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", 
            "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", 
            "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", 
            "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", 
            "tipo_calculo", "detalles"
        ]
            
            elementos_visuales = [
            self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, 
            self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, 
            self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, 
            self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, 
            self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, 
            self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, 
            self.tipo_calculo_ds_edit,self.detalles_ds_edit
        ]
            tipos = [str, str, int, int, int, float, str, str, float, float, str, str, float, float, str, str, str]
            self.metodos_comunes.actualizar_datos_db(self.tabla_datos_salida,columnas, elementos_visuales, tipos, self.RegistroDatosSalidaManejador,DatosSalida,self.limpiar_formulario_datos_salida, self.buscar_datos_salida) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al actualizar los datos de salida: {e}", QMessageBox.StandardButton.Ok)


    def agregar_datos_salida(self):
        try:
            columnas = [
            "nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", 
            "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", 
            "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", 
            "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", 
            "tipo_calculo", "detalles"
        ]
            elementos_visuales = [
            self.nombre_ds_edit, self.fecha_ds_edit, self.id_nombre_data_ds_edit, 
            self.id_condiciones_iniciales_ds_edit, self.id_registro_unidades_ds_edit, 
            self.r_ds_edit, self.nombre_data_ds_edit, self.nombre_reaccion_ds_edit, 
            self.delta_n_ds_edit, self.epsilon_rl_ds_edit, self.tipo_especie_ds_edit, 
            self.especie_quimica_ds_edit, self.constante_cinetica_ds_edit, 
            self.orden_reaccion_ds_edit, self.modelo_cinetico_ds_edit, 
            self.tipo_calculo_ds_edit,self.detalles_ds_edit
        ]
            tipos = [str, str, int, int, int, float, str, str, float, float, str, str, float, float, str, str, str]
            self.metodos_comunes.agregar_datos_db(columnas, elementos_visuales, tipos, self.RegistroDatosSalidaManejador,DatosSalida,self.limpiar_formulario_datos_salida, self.buscar_datos_salida) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos de salida: {e}", QMessageBox.StandardButton.Ok)

    # funciones crud para registro de datos de salida arrhenius
    # Registro de datos de salida Arrhenius
    def mostrar_datos_tabla_salida_arrhenius(self, resultados):
        self.metodos_comunes.mostrar_datos_tabla_arrhenius(self.tabla_datos_salida_arrhenius, resultados)
    
    def agregar_datos_salida_arrhenius(self):
        try:
            columnas = ["nombre_caso","id_nombre_data_salida","id_nombre_data","fecha","temperatura","reciproco_temperatura_absoluta","constante_cinetica","logaritmo_constante_cinetica","energia_activacion_r","r_utilizada","energia_activacion","constante_cinetica_0","logaritmo_constante_cinetica_0","detalles"]
            elementos_visuales = [self.nombre_caso_a_edit,self.id_nombre_data_salida_a,self.id_nombre_data_a_edit,self.fecha_a_edit,self.temperatura_a_edit,self.rtemperatura_a_edit,self.constante_cinetica_a_edit,self.ln_constante_cinetica_a_edit,self.energia_activacion_r_a_edit,self.r_a_edit,self.energia_activacion_a_edit,self.constante_cinetica_0_a_edit,self.ln_constante_cinetica_0_a_edit,self.detalles_a_edit]
            tipos = [str,int,int,str,float,float,float,float,float,float,float,float,float,str]            
            self.metodos_comunes.agregar_datos_db(columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDatosSalidaArrhenius,clase_objeto=DatosSalidaArrhenius,limpiar_func=self.limpiar_formulario_datos_salida_arrhenius,buscar_func=self.buscar_datos_salida_arrhenius)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def actualizar_datos_salida_arrhenius(self):
        try:
            columnas = ["nombre_caso","id_nombre_data_salida","id_nombre_data","fecha","temperatura","reciproco_temperatura_absoluta","constante_cinetica","logaritmo_constante_cinetica","energia_activacion_r","r_utilizada","energia_activacion","constante_cinetica_0","logaritmo_constante_cinetica_0","detalles"]
            elementos_visuales = [self.nombre_caso_a_edit,self.id_nombre_data_salida_a,self.id_nombre_data_a_edit,self.fecha_a_edit,self.temperatura_a_edit,self.rtemperatura_a_edit,self.constante_cinetica_a_edit,self.ln_constante_cinetica_a_edit,self.energia_activacion_r_a_edit,self.r_a_edit,self.energia_activacion_a_edit,self.constante_cinetica_0_a_edit,self.ln_constante_cinetica_0_a_edit,self.detalles_a_edit]
            tipos = [str,int,int,str,float,float,float,float,float,float,float,float,float,str]            
            self.metodos_comunes.actualizar_datos_db(tabla=self.tabla_datos_salida_arrhenius,columnas=columnas,elementos_visuales=elementos_visuales,tipos=tipos,manejador=self.RegistroDatosSalidaArrhenius,clase_objeto=DatosSalidaArrhenius,limpiar_func=self.limpiar_formulario_datos_salida_arrhenius,buscar_func=self.buscar_datos_salida_arrhenius)
        except ValueError as e:
            self.statusBar().showMessage(f"Datos inválidos o incompletos: {e}", 5000)
    
    def limpiar_formulario_datos_salida_arrhenius(self):
        elementos_visuales = [self.nombre_caso_a_edit,self.id_nombre_data_salida_a,self.id_nombre_data_a_edit,self.fecha_a_edit,self.temperatura_a_edit,self.rtemperatura_a_edit,self.constante_cinetica_a_edit,self.ln_constante_cinetica_a_edit,self.energia_activacion_r_a_edit,self.r_a_edit,self.energia_activacion_a_edit,self.constante_cinetica_0_a_edit,self.ln_constante_cinetica_0_a_edit,self.detalles_a_edit]
        self.metodos_comunes.limpiar_elementos_visuales(elementos_visuales)
    
    def seleccionar_datos_salida_arrhenius(self):
        columnas = ["id","nombre_caso","id_nombre_data_salida","id_nombre_data","fecha","temperatura","reciproco_temperatura_absoluta","constante_cinetica","logaritmo_constante_cinetica","energia_activacion_r","r_utilizada","energia_activacion","constante_cinetica_0","logaritmo_constante_cinetica_0","detalles"]
        elementos_visuales = [self.nombre_caso_a_edit,self.id_nombre_data_salida_a,self.id_nombre_data_a_edit,self.fecha_a_edit,self.temperatura_a_edit,self.rtemperatura_a_edit,self.constante_cinetica_a_edit,self.ln_constante_cinetica_a_edit,self.energia_activacion_r_a_edit,self.r_a_edit,self.energia_activacion_a_edit,self.constante_cinetica_0_a_edit,self.ln_constante_cinetica_0_a_edit,self.detalles_a_edit]
        datos=self.metodos_comunes.seleccionar_datos_visuales(self.tabla_datos_salida_arrhenius, columnas, elementos_visuales)
        if datos:
            self.statusBar().showMessage(f"Set de Datos de Salida Arrhenius seleccionados id: {datos['id']}", 5000)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
    
    def actualizar_valor_celda_datos_salida_arrhenius(self, fila, columna):
        self.metodos_comunes.actualizar_valor_celda(self.tabla_datos_salida_arrhenius, self.RegistroDatosSalidaArrhenius, fila, columna)
    
    def borrar_datos_salida_arrhenius(self):
        fila_seleccionada = self.tabla_datos_salida_arrhenius.currentRow()
        if fila_seleccionada != -1:
            id = self.tabla_datos_salida_arrhenius.item(fila_seleccionada, 0).text().strip()
            borrar_resultado = self.RegistroDatosSalidaArrhenius.borrar(id)
            self.metodos_comunes.borrar_elemento(
                self.tabla_datos_salida_arrhenius, 
                borrar_resultado, 
                "¿Estás seguro de eliminar los datos de salida Arrhenius?", 
                "Datos de salida Arrhenius eliminados correctamente", 
                "Hubo un problema al eliminar los datos de salida Arrhenius", 
                self.RegistroDatosSalidaArrhenius.consultar, 
                self.refrescar_datos_tabla, 
                self.buscar_datos_salida_arrhenius
            )
            self.statusBar().showMessage(f"Datos de salida Arrhenius con id {id} eliminados", 5000)

    def buscar_datos_salida_arrhenius(self):
        try:
            columnas = ["nombre_caso","id_nombre_data_salida","id_nombre_data","fecha","temperatura","reciproco_temperatura_absoluta","constante_cinetica","logaritmo_constante_cinetica","energia_activacion_r","r_utilizada","energia_activacion","constante_cinetica_0","logaritmo_constante_cinetica_0","detalles"]
            elementos_visuales = [self.nombre_caso_a_edit,self.id_nombre_data_salida_a,self.id_nombre_data_a_edit,self.fecha_a_edit,self.temperatura_a_edit,self.rtemperatura_a_edit,self.constante_cinetica_a_edit,self.ln_constante_cinetica_a_edit,self.energia_activacion_r_a_edit,self.r_a_edit,self.energia_activacion_a_edit,self.constante_cinetica_0_a_edit,self.ln_constante_cinetica_0_a_edit,self.detalles_a_edit]
            aplicar_strip = []
            self.metodos_comunes.buscar_datos_db(columnas, elementos_visuales,aplicar_strip, self.RegistroDatosSalidaArrhenius, self.mostrar_datos_tabla_salida_arrhenius,True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al buscar los datos de salida Arrhenius: {e}", QMessageBox.StandardButton.Ok)

    def reiniciar_aplicacion(self):
        self.componentes_auxiliares.reiniciar_aplicacion()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PantallaCrud()
    window.show()
    sys.exit(app.exec())
