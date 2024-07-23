from PyQt6.QtWidgets import QMessageBox, QComboBox

class YourClassName:  # Cambia esto por el nombre real de tu clase
    def __init__(self, parent=None):
        self.parent = parent
        self.filtro_datos_box = QComboBox()  # Asegúrate de inicializar tu combo box
        self.filtro_datos_box_2 = QComboBox()  # Asegúrate de inicializar tu combo box
        self.filtro_datos_box_3 = QComboBox()  # Asegúrate de inicializar tu combo box
        self.DatosCineticosManejador = DatosCineticosManejador()

    def desplegar_datos_combo_box_catalogo(self, combo_box, elementos, mensaje_error, tipo_elemento_catalogo):
        try:
            combo_box.clear()
            combo_box.addItem("Seleccione una opción", -1)
            combo_box.addItem("otro")  # Agregar la opción "otro" al final de la lista
            if elementos:
                for elemento in elementos:
                    combo_box.addItem(str(elemento.get(tipo_elemento_catalogo)), str(elemento.get("id")))
            else:
                QMessageBox.information(self.parent, "No hay elementos", mensaje_error, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al mostrar elementos: {e}", QMessageBox.StandardButton.Ok)
    
    def filtro_desplegar_datos_combo_box_catalogo(self, combo_box, consulta_func, mensaje_error, atributo, tipo_elemento_catalogo):
        try:
            # Consultar los datos utilizando la función proporcionada
            datos = consulta_func()

            if datos:
                # Formatear los datos en una estructura compatible
                elementos = [{"id": getattr(dato, atributo), tipo_elemento_catalogo: getattr(dato, atributo)} for dato in datos]
                # Llamar al método de despliegue
                self.desplegar_datos_combo_box_catalogo(combo_box, elementos, mensaje_error, tipo_elemento_catalogo)
            else:
                QMessageBox.information(self.parent, "No hay datos", mensaje_error, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al filtrar datos: {e}", QMessageBox.StandardButton.Ok)

    def filtrar_datos(self):
        self.filtro_desplegar_datos_combo_box_catalogo(
            self.filtro_datos_box,
            self.DatosCineticosManejador.consultar,
            "No se encontraron datos en la base de datos.",
            "tipo_especie",
            "tipo_especie"
        )

    def filtrar_especie_quimica(self):
        self.filtro_desplegar_datos_combo_box_catalogo(
            self.filtro_datos_box_2,
            self.DatosCineticosManejador.consultar,
            "No se encontraron datos en la base de datos.",
            "especie_quimica",
            "especie_quimica"
        )

    def filtrar_datos_id_condiciones_iniciales(self):
        self.filtro_desplegar_datos_combo_box_catalogo(
            self.filtro_datos_box_3,
            self.DatosCineticosManejador.consultar,
            "No se encontraron datos en la base de datos.",
            "id_condiciones_iniciales",
            "id_condiciones_iniciales"
        )

# Ejemplo de uso
# Crea una instancia de tu clase
tu_clase = YourClassName()
# Llama a los métodos
tu_clase.filtrar_datos()
tu_clase.filtrar_especie_quimica()
tu_clase.filtrar_datos_id_condiciones_iniciales()
