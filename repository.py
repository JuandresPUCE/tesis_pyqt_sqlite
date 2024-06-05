from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import logging
from sqlalchemy.exc import SQLAlchemyError

import os

from models import *

# Obtén la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define la ruta relativa al archivo de la base de datos
#relative_path = os.path.join(current_dir, 'dataReactor', 'tesis_flet_sqlite', 'tesis_flet_sqlite', 'data', 'data_reactor1.db')

#db_path = relative_path
#absolute
#db_path = r"D:\candidatos_proyectof\tesis_tec\dataReactor\tesis_GUI_sqlite\tesis_pyqt_sqlite\data\data_reactor1.db"
#realtive
db_path = r"data\data_reactor1.db"


# crud SQLalchemy

class CondicionesInicialesManejador:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
        self.Session = sessionmaker(bind=self.engine)

    def agregar_condicion(self, condicion):
        session = self.Session()
        try:
            session.add(condicion)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al agregar condición: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def consultar_condicion(self, filtros=None, formato=None):
        session = self.Session()
        query = session.query(CondicionesIniciales)

        # Aplicar filtros si se proporcionan
        if filtros:
            condiciones = []
            for columna, valor in filtros.items():
                if valor:
                    #registro exacto
                    condiciones.append(getattr(CondicionesIniciales, columna) == valor)
                    #registro con like similar
                    #condiciones.append(getattr(CondicionesIniciales, columna).like(f'%{valor}%'))

            # Unir todas las condiciones con OR
            if condiciones:
                query = query.filter(or_(*condiciones))

        # Ejecutar la consulta
        if formato == 'pandas':
            datos = query.all()
        else:
            datos = query.all()
        return datos

    def borrar_condicion(self, id):
        session = self.Session()
        condicion = session.query(CondicionesIniciales).filter(CondicionesIniciales.id == id).first()
        if condicion:
            session.delete(condicion)
            session.commit()
            return True
        return False

    def actualizar_condicion(self, id, new_condicion):
        session = self.Session()
        condicion = session.query(CondicionesIniciales).filter(CondicionesIniciales.id == id).first()
        if condicion:
            for key, value in new_condicion.items():
                setattr(condicion, key, value)
            session.commit()
            print(f"Condition with ID {id} updated successfully.")  # Debugging line
        else:
            print(f"No se encontró la condición con id {id}")

class DatosCineticosManejador:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
        self.Session = sessionmaker(bind=self.engine)

    def agregar_dato(self, dato):
        session = self.Session()
        try:
            session.add(dato)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al agregar dato: {e}")
            session.rollback()
            return False
        finally:
            session.close()


    def consultar_datos(self, filtros=None, formato=None):
        session = self.Session()
        query = session.query(DatosIngresadosCineticos)
        if not filtros:
            return query.all()
        condiciones = []
        for columna, valor in filtros.items():
            if not valor:
                continue
            if formato == 'like':
                # Registro con like similar
                condiciones.append(getattr(DatosIngresadosCineticos, columna).like(f'%{valor}%'))
            else:
                # Registro exacto
                condiciones.append(getattr(DatosIngresadosCineticos, columna) == valor)
        if condiciones:
            query = query.filter(or_(*condiciones))
        return query.all()
    
    def consultar_conjunto_datos_por_nombre(self, nombre_data):
        session = self.Session()
        datos = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.nombre_data == nombre_data)
        return datos
    
    def consultar_dato_por_id_conjunto_datos(self, id, nombre_data):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id, DatosIngresadosCineticos.nombre_data == nombre_data).first()
        return dato

    def borrar_dato(self, id):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
        if dato:
            session.delete(dato)
            session.commit()
            return True
        return False

    def actualizar_dato(self, id, new_dato):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
        if dato:
            for key, value in new_dato.items():
                setattr(dato, key, value)
            session.commit()
            #print(f"Condition with ID {id} updated successfully.")  # Linea para check en consola
            return True
        else:
            #print(f"No se encontró la condición con id {id}")     # Linea para check en consola
            return False

class RegistroDataExperimentalManejador:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
        self.Session = sessionmaker(bind=self.engine)    
    
    def agregar_registro(self, registro):
        session = self.Session()
        try:
            session.add(registro)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al agregar registro: {e}")
            session.rollback()
            return False
        finally:
            session.close()

       
    def consultar_registro(self, filtros=None, formato=None):
        session = self.Session()
        query = session.query(RegistroDataExperimental)

        # Aplicar filtros si se proporcionan
        if filtros:
            condiciones = []
            for columna, valor in filtros.items():
                if not valor:
                    continue
                if formato == 'like':
                    # Registro con like similar
                    condiciones.append(getattr(RegistroDataExperimental, columna).like(f'%{valor}%'))
                else:
                    # Registro exacto
                    condiciones.append(getattr(RegistroDataExperimental, columna) == valor)

            # Unir todas las condiciones con OR
            if condiciones:
                query = query.filter(or_(*condiciones))

        # Ejecutar la consulta
        datos = query.all()
        return datos
    
    def consultar_registro_por_nombre(self, nombre_data):
        session = self.Session()
        datos = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.nombre_data == nombre_data)
        return datos

    def borrar_registro(self, id):
        session = self.Session()
        registro = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.id == id).first()
        if registro:
            session.delete(registro)
            session.commit()
            return True
        return False    
    
    def actualizar_registro(self, id, new_registro):
        session = self.Session()
        registro = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.id == id).first()
        if registro:
            for key, value in new_registro.items():
                setattr(registro, key, value)
            session.commit()
            #print(f"Condition with ID {id} updated successfully.")  # Linea para check en consola
            return True
        else:
            #print(f"No se encontró la condición con id {id}")     # Linea para check en consola
            return False
        
class ReaccionQuimicaManejador:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
        self.Session = sessionmaker(bind=self.engine)

    def agregar_reaccion(self, reaccion):
        session = self.Session()
        try:
            session.add(reaccion)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al agregar reacción: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def consultar_reaccion(self, filtros=None, formato=None):
        session = self.Session()
        query = session.query(ReaccionQuimica)

        # Aplicar filtros si se proporcionan
        if filtros:
            condiciones = []
            for columna, valor in filtros.items():
                if valor:
                    condiciones.append(getattr(ReaccionQuimica, columna).like(f'%{valor}%'))

            # Unir todas las condiciones con OR
            if condiciones:
                query = query.filter(or_(*condiciones))

        # Ejecutar la consulta
        if formato == 'pandas':
            datos = query.all()
        else:
            datos = query.all()
        return datos

    def borrar_reaccion(self, id):
        session = self.Session()
        reaccion = session.query(ReaccionQuimica).filter(ReaccionQuimica.id == id).first()
        if reaccion:
            session.delete(reaccion)
            session.commit()
            return True
        return False
    
    def actualizar_reaccion(self, id, new_reaccion):
        session = self.Session()
        reaccion = session.query(ReaccionQuimica).filter(ReaccionQuimica.id == id).first()
        if reaccion:
            for key, value in new_reaccion.items():
                setattr(reaccion, key, value)
            session.commit()
            #print(f"Condition with ID {id} updated successfully.")  # Linea para check en consola
            return True
        else:
            #print(f"No se encontró la condición con id {id}")     # Linea para check en consola
            return False