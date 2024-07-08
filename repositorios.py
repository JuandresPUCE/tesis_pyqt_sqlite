from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import logging
from sqlalchemy.exc import SQLAlchemyError
import os
from modelos import *
from servicios import *

# Obtén la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

metodos_comunes = Servicios()

dir_db = r"config\config.json"       
db_path=metodos_comunes.cargar_configuracion_json(dir_db,"db_path")

engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)

# Crear todas las tablas
Base.metadata.create_all(engine)

class BaseManejador:
    def __init__(self, model):
        self.model = model
        self.engine = create_engine(f'sqlite:///{db_path}', poolclass=QueuePool, pool_size=20, max_overflow=0)
        self.Session = sessionmaker(bind=self.engine)

    def agregar(self, item):
        session = self.Session()
        try:
            session.add(item)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al agregar {self.model.__name__}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def consultar(self, filtros=None, formato=None):
        session = self.Session()
        query = session.query(self.model)
        try:
            if not filtros:
                return query.all()

            condiciones = []
            for columna, valor in filtros.items():
                if valor:
                    if formato == 'like':
                        condiciones.append(getattr(self.model, columna).like(f'%{valor}%'))
                    else:
                        condiciones.append(getattr(self.model, columna) == valor)

            if condiciones:
                query = query.filter(or_(*condiciones))

            return query.all()
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al consultar {self.model.__name__}: {e}")
            return None
        finally:
            session.close()

    def borrar(self, id):
        session = self.Session()
        try:
            item = session.query(self.model).filter(self.model.id == id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró {self.model.__name__} con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al borrar {self.model.__name__}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def actualizar(self, id, new_data):
        session = self.Session()
        try:
            item = session.query(self.model).filter(self.model.id == id).first()
            if item:
                for key, value in new_data.items():
                    setattr(item, key, value)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró {self.model.__name__} con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al actualizar {self.model.__name__}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

# Definir manejadores específicos para cada modelo

class CondicionesInicialesManejador(BaseManejador):
    def __init__(self):
        super().__init__(CondicionesIniciales)

class DatosCineticosManejador(BaseManejador):
    def __init__(self):
        super().__init__(DatosIngresadosCineticos)

class RegistroDataExperimentalManejador(BaseManejador):
    def __init__(self):
        super().__init__(RegistroDataExperimental)

class ReaccionQuimicaManejador(BaseManejador):
    def __init__(self):
        super().__init__(ReaccionQuimica)

class RegistroUnidadesManejador(BaseManejador):
    def __init__(self):
        super().__init__(RegistroUnidades)

class RegistroDatosSalidaManejador(BaseManejador):
    def __init__(self):
        super().__init__(DatosSalida)
