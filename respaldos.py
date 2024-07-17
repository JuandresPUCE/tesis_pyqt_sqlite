import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QApplication
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
import sys
from sqlalchemy.orm import Session
from modelos import *
from servicios import Servicios
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker

class Respaldos:
    def __init__(self, session: Session, parent=None):
        self.parent = parent 
        self.session = session

    def obtener_datos(self):
        try:
            # Definir un helper para convertir a DataFrame
            def to_dataframe(query_result):
                data = [vars(obj) for obj in query_result]
                df = pd.DataFrame(data)
                if '_sa_instance_state' in df.columns:
                    df = df.drop(columns='_sa_instance_state')
                return df

            condiciones_iniciales_data = self.session.query(CondicionesIniciales).all()
            datos_cineticos_data = self.session.query(DatosIngresadosCineticos).all()
            registro_data_experimental_data = self.session.query(RegistroDataExperimental).all()
            reaccion_quimica_data = self.session.query(ReaccionQuimica).all()
            registro_unidades_data = self.session.query(RegistroUnidades).all()
            datos_salida_data = self.session.query(DatosSalida).all()
            datos_salida_arrhenius_data = self.session.query(DatosSalidaArrhenius).all()

            df_condiciones_iniciales = to_dataframe(condiciones_iniciales_data)
            df_datos_cineticos = to_dataframe(datos_cineticos_data)
            df_registro_data_experimental = to_dataframe(registro_data_experimental_data)
            df_reaccion_quimica = to_dataframe(reaccion_quimica_data)
            df_registro_unidades = to_dataframe(registro_unidades_data)
            df_datos_salida = to_dataframe(datos_salida_data)
            df_datos_salida_arrhenius = to_dataframe(datos_salida_arrhenius_data)

            return {
                "condiciones_iniciales": df_condiciones_iniciales,
                "datos_cineticos": df_datos_cineticos,
                "registro_data_experimental": df_registro_data_experimental,
                "reaccion_quimica": df_reaccion_quimica,
                "registro_unidades": df_registro_unidades,
                "datos_salida": df_datos_salida,
                "datos_salida_arrhenius": df_datos_salida_arrhenius
            }
        except Exception as e:
            print(f"Ocurrió un error al obtener los datos: {e}")
            return {}



    def exportar_datos(self, filename, delimiter, dataframes):
        try:
            if filename.endswith('.csv'):
                with open(filename, 'w', newline='') as csvfile:
                    for name, df in dataframes.items():
                        csvfile.write(f"# {name}\n")
                        df.to_csv(csvfile, sep=delimiter, index=False)
                        csvfile.write("\n")
                print(f"Datos exportados exitosamente a {filename}")
                QMessageBox.information(self.parent, "Datos exportados", f"Datos exportados exitosamente a {filename}")
            elif filename.endswith('.xlsx'):
                with pd.ExcelWriter(filename) as writer:
                    for sheet_name, df in dataframes.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Datos exportados exitosamente a {filename}")
                QMessageBox.information(self.parent, "Datos exportados", f"Datos exportados exitosamente a {filename}")
            else:
                print("Formato de archivo no soportado. Por favor, elija .csv o .xlsx.")
                QMessageBox.warning(self.parent, "Formato de archivo no soportado", "Por favor, elija .csv o .xlsx.")
        except Exception as e:
            print(f"Ocurrió un error al exportar los datos: {e}")
            QMessageBox.critical(self.parent, "Error al exportar datos", f"Ocurrió un error al exportar los datos: {e}")

    def guardar_archivo(self):
        try:
            # Obtiene el path del archivo usando un cuadro de diálogo
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar Archivo",
                "",
                "CSV files (*.csv);;Excel files (*.xlsx)"
            )

            if file_path:
                delimiter = ';' if file_path.endswith('.csv') else None
                dataframes = self.obtener_datos()
                if dataframes:
                    self.exportar_datos(file_path, delimiter, dataframes)
        except Exception as e:
            print(f"Ocurrió un error al guardar el archivo: {e}")
            QMessageBox.critical(self.parent, "Error al guardar archivo", f"Ocurrió un error al guardar el archivo: {e}")

    def generar_respaldo(self):
        try:
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
            print(f"Ocurrió un error al generar el respaldo: {e}")
            QMessageBox.critical(None, "Error al generar respaldo", f"Ocurrió un error al generar el respaldo: {e}")
