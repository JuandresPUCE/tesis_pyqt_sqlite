from PyQt5.QtWidgets import QMessageBox

class TuClase:
    # Otras partes de tu código...

    def boton_desactivado(self):
        # Lógica para desactivar el botón
        pass

    def boton_activado(self):
        # Lógica para activar el botón
        pass

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        msg_box = QMessageBox()
        if tipo == 'info':
            msg_box.setIcon(QMessageBox.Information)
        elif tipo == 'advertencia':
            msg_box.setIcon(QMessageBox.Warning)
        elif tipo == 'error':
            msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.exec()

    def agregar_a_db(self, objeto, manejador, limpiar_funcion, buscar_funcion):

            # Validar que todos los campos estén llenos
            for campo, valor in objeto:
                if not valor:
                    raise ValueError(f"El campo '{campo}' está vacío. Por favor, llénelo.")

            # Intentar agregar el objeto a la base de datos
            agregar_resultado = manejador.agregar(objeto)

            if agregar_resultado:
                self.mostrar_mensaje('info', "Información", "Datos agregados correctamente")
                limpiar_funcion()
                buscar_funcion()  # Refrescar la tabla con los nuevos datos
            else:
                self.mostrar_mensaje('error', "Error", "Hubo un problema al agregar los datos")


    def agregar_dato(self):
        objeto = {
            'tiempo': float(self.tiempo.text()),
            'concentracion': float(self.concentracion.text()),
            'otra_propiedad': float(self.otra_propiedad.text()),
            'conversion_reactivo_limitante': float(self.conversion_reactivo_limitante.text()),
            'tipo_especie': self.tipo_especie.text(),
            'id_condiciones_iniciales': int(self.id_condiciones_iniciales.text()),
            'nombre_data': self.nombre_data.text(),
            'nombre_reaccion': self.nombre_reaccion.text(),
            'especie_quimica': self.especie_quimica.text(),
        }
        self.agregar_a_db(objeto, self.DatosCineticosManejador, self.limpiar_formulario, self.buscar_dato)

    def agregar_registro_data_experimental(self):
        objeto = {
            'nombre_data': self.nombre_data_experimental.text(),
            'fecha': self.fecha_data_experimental.text(),
            'detalle': self.detalle_data_experimental.text(),
        }
        self.agregar_a_db(objeto, self.RegistroDataExperimentalManejador, self.limpiar_formulario_registro_data_experimental, self.buscar_registros)

    def agregar_condiciones_iniciales(self):
        objeto = {
            'temperatura': self.temperatura_ci.text(),
            'tiempo': self.tiempo_ci.text(),
            'presion_total': self.presion_total_ci.text(),
            'presion_parcial': self.presion_parcial_ci.text(),
            'fraccion_molar': self.fraccion_molar_ci.text(),
            'especie_quimica': self.especie_quimica_ci.text(),
            'tipo_especie': self.tipo_especie_ci.text(),
            'detalle': self.detalle_ci.text(),
            'nombre_data': self.nombre_data_ci.text(),
        }
        self.agregar_a_db(objeto, self.CondicionesInicialesManejador, self.limpiar_formulario_ci, self.buscar_condiciones_iniciales)

    def agregar_reaccion_quimica(self):
        objeto = {
            'especie_quimica': self.especie_quimica_rq.text(),
            'formula': self.formula_rq.text(),
            'coeficiente_estequiometrico': self.coeficiente_estequiometro_rq.text(),
            'detalle': self.detalle_rq.text(),
            'tipo_especie': self.tipo_especie_rq.text(),
            'nombre_reaccion': self.nombre_reaccion_rq.text(),
        }
        self.agregar_a_db(objeto, self.ReaccionQuimicaManejador, self.limpiar_formulario_rq, self.buscar_reaccion_quimica)

    def agregar_unidades(self):
        presion = self.presion_u_edit.text()
        temperatura = self.temperatura_u_edit.text()
        tiempo = self.tiempo_u_edit.text()
        concentracion = self.concentracion_u_edit.text()
        energia = self.energia_u_edit.text()
        nombre_data = self.nombre_data_u_edit.text()

        objeto = {
            'presion': presion,
            'temperatura': temperatura,
            'tiempo': tiempo,
            'concentracion': concentracion,
            'energia': energia,
            'nombre_data': nombre_data,
        }
        self.agregar_a_db(objeto, self.RegistroUnidadesManejador, self.limpiar_formulario_unidades, self.buscar_unidades)

    def agregar_datos_salida(self):
        objeto = {
            'nombre_data_salida': self.nombre_ds_edit.text().strip(),
            'fecha': self.fecha_ds_edit.text().strip(),
            'id_nombre_data': int(self.id_nombre_data_ds_edit.text().strip()),
            'id_condiciones_iniciales': int(self.id_condiciones_iniciales_ds_edit.text().strip()),
            'id_registro_unidades': int(self.id_registro_unidades_ds_edit.text().strip()),
            'r_utilizada': float(self.r_ds_edit.text().strip()),
            'nombre_data': self.nombre_data_ds_edit.text().strip(),
            'nombre_reaccion': self.nombre_reaccion_ds_edit.text().strip(),
            'delta_n_reaccion': float(self.delta_n_ds_edit.text().strip()),
            'epsilon_reactivo_limitante': float(self.epsilon_rl_ds_edit.text().strip()),
        }
        self.agregar_a_db(objeto, self.RegistroDatosSalidaManejador, self.limpiar_formulario_datos_salida, self.buscar_datos_salida)


"""
    def agregar_unidades(self):
        self.boton_desactivado()
        try:
            presion = self.presion_u_edit.text()
            temperatura = self.temperatura_u_edit.text()
            tiempo = self.tiempo_u_edit.text()
            concentracion = self.concentracion_u_edit.text()
            energia = self.energia_u_edit.text()
            nombre_data = self.nombre_data_u_edit.text()

            self.unidades = RegistroUnidades(
                presion=presion,
                temperatura=temperatura,
                tiempo=tiempo,
                concentracion=concentracion,
                energia=energia,
                nombre_data=nombre_data
            )
            self.metodos_comunes.agregar_objeto_db(self.unidades,self.RegistroUnidadesManejador, self.limpiar_formulario_unidades, self.buscar_unidades)
        finally:
            self.boton_activado()
"""

def agregar_a_db(self, objeto, manejador, limpiar_funcion, buscar_funcion):
    self.boton_desactivado()
    
    # Validar que todos los campos del objeto estén llenos
    for campo, valor in objeto.__dict__.items():
        if campo != '_sa_instance_state' and not valor:
            QMessageBox.warning(self, "Advertencia", f"El campo '{campo}' está vacío. Por favor, llénelo.", QMessageBox.StandardButton.Ok)
            self.boton_activado()
            return
    
    # Intentar agregar el objeto a la base de datos
    try:
        agregar_resultado = manejador.agregar(objeto)

        if agregar_resultado:
            QMessageBox.information(self, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
            limpiar_funcion()
            buscar_funcion()  # Refrescar la tabla con los nuevos datos
        else:
            QMessageBox.critical(self, "Error", "Hubo un problema al agregar los datos", QMessageBox.StandardButton.Ok)
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Se produjo un error al agregar los datos: {e}", QMessageBox.StandardButton.Ok)
    
    self.boton_activado()


def agregar_dato(self):
    try:
        dato = DatosIngresadosCineticos(
            tiempo=float(self.tiempo.text()),
            concentracion=float(self.concentracion.text()),
            otra_propiedad=float(self.otra_propiedad.text()),
            conversion_reactivo_limitante=float(self.conversion_reactivo_limitante.text()),
            tipo_especie=self.tipo_especie.text(),
            id_condiciones_iniciales=int(self.id_condiciones_iniciales.text()),
            nombre_data=self.nombre_data.text(),
            nombre_reaccion=self.nombre_reaccion.text(),
            especie_quimica=self.especie_quimica.text()
        )
    except ValueError as e:
        QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
        self.boton_activado()
        return

    self.agregar_a_db(dato, self.DatosCineticosManejador, self.limpiar_formulario, self.buscar_dato)

def agregar_registro_data_experimental(self):
    try:
        registro = RegistroDataExperimental(
            nombre_data=self.nombre_data_experimental.text(),
            fecha=self.fecha_data_experimental.text(),
            detalle=self.detalle_data_experimental.text()
        )
    except ValueError as e:
        QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
        self.boton_activado()
        return

    self.agregar_a_db(registro, self.RegistroDataExperimentalManejador, self.limpiar_formulario_registro_data_experimental, self.buscar_registros)

def agregar_condiciones_iniciales(self):
    try:
        condiciones_iniciales = CondicionesIniciales(
            temperatura=self.temperatura_ci.text(),
            tiempo=self.tiempo_ci.text(),
            presion_total=self.presion_total_ci.text(),
            presion_parcial=self.presion_parcial_ci.text(),
            fraccion_molar=self.fraccion_molar_ci.text(),
            especie_quimica=self.especie_quimica_ci.text(),
            tipo_especie=self.tipo_especie_ci.text(),
            detalle=self.detalle_ci.text(),
            nombre_data=self.nombre_data_ci.text()
        )
    except ValueError as e:
        QMessageBox.warning(self, "Advertencia", f"Datos inválidos o incompletos: {e}", QMessageBox.StandardButton.Ok)
        self.boton_activado()
        return

    self.agregar_a_db(condiciones_iniciales, self.CondicionesInicialesManejador, self.limpiar_formulario_ci, self.buscar_condiciones_iniciales)