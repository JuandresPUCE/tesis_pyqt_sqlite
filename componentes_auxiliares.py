import os
import sys
import subprocess
from datetime import datetime

from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox


from servicios import *
from repositorios import *


class ComponentesAuxiliares:
    def __init__(self, parent=None):
        self.parent = parent  # Guardar referencia al widget padre
        self.mensaje = "Metodos comunes para los controladores"
        self.titulo = "Componentes Auxiliares"
        self.metodos_comunes = Servicios()

    def reiniciar_aplicacion(self):
        try:
            # Cerrar la aplicación actual
            QApplication.quit()

            # Obtener el nombre del archivo de script actual (main.py)
            script_name = os.path.abspath(sys.argv[0])

            # Volver a ejecutar el script
            subprocess.Popen([sys.executable, script_name])

            # Salir del proceso actual
            sys.exit()

        except Exception as e:
            # Mostrar un mensaje de error en caso de excepción
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al reiniciar la aplicación: {e}")

    def crear_base_datos(self):
        try:
            self.metodos_comunes.nueva_configuracion_db()
            
            # Confirmar al usuario que la aplicación se reiniciará
            reply = QMessageBox.question(
                self.parent, 
                'Reinicio necesario', 
                'Se ha creado una nueva configuración de la base de datos. La aplicación se reiniciará para aplicar los cambios.',
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Ok
            )
            
            if reply == QMessageBox.StandardButton.Ok:
                self.reiniciar_aplicacion()
        
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al crear la base de datos: {e}")
    
    def cambiar_config_base_datos(self):
        try:
            self.metodos_comunes.cambiar_configuracion_db()

            # Confirmar al usuario que la aplicación se reiniciará
            reply = QMessageBox.question(
                self.parent, 
                'Reinicio necesario', 
                'La configuración de la base de datos se ha actualizado. La aplicación se reiniciará para aplicar los cambios.',
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Ok
            )

            if reply == QMessageBox.StandardButton.Ok:
                self.reiniciar_aplicacion()

        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al cambiar la configuración de la base de datos: {e}")
    
    def respaldar_base_datos(self):
        try:
            self.metodos_comunes.respaldar_db()

            # Mostrar mensaje de éxito
            #QMessageBox.information(self.parent, "Respaldo exitoso", "La base de datos se ha respaldado correctamente.")
        
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al respaldar la base de datos: {e}")
    
    def manejadores_base(self):
        
        # manejadores de base
        self.RegistroDataExperimentalManejador = RegistroDataExperimentalManejador()
        self.CondicionesInicialesManejador = CondicionesInicialesManejador()
        self.DatosCineticosManejador = DatosCineticosManejador()
        self.ReaccionQuimicaManejador = ReaccionQuimicaManejador()
        self.RegistroUnidadesManejador = RegistroUnidadesManejador()
        self.RegistroDatosSalidaManejador = RegistroDatosSalidaManejador()
        self.RegistroDatosSalidaArrhenius = RegistroDatosSalidaArrhenius()           

        self.metodos_comunes = Servicios()
        self.componentes_auxiliares = ComponentesAuxiliares()

    def ajustar_tabla(self, tabla: QTableWidget, titulos_columnas: list):
        tabla.setHorizontalHeaderLabels(titulos_columnas)
        tabla.resizeColumnsToContents()

    def ocultar_columnas(self, tabla: QTableWidget, columnas_ocultas: list):
        for col in columnas_ocultas:
            tabla.hideColumn(col)
    
    def establecer_fecha_sistema(self,fecha_edit):
        # Obtener la fecha actual del sistema
        self.fecha_actual = datetime.now().date()

        # Convertir la fecha a una cadena en el formato dd/mm/yyyy
        self.fecha_str = self.fecha_actual.strftime("%d/%m/%Y")

        fecha_edit.setText(self.fecha_str)