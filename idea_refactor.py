from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import logging
from sqlalchemy.exc import SQLAlchemyError

import os

from modelos import *

# Obtén la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define la ruta relativa al archivo de la base de datos
#relative_path = os.path.join(current_dir, 'dataReactor', 'tesis_flet_sqlite', 'tesis_flet_sqlite', 'data', 'data_reactor1.db')

#db_path = relative_path
#absolute
#db_path = r"D:\candidatos_proyectof\tesis_tec\dataReactor\tesis_GUI_sqlite\tesis_pyqt_sqlite\data\data_reactor1.db"
#realtive
#db_path = r"data\data_reactor1.db"
db_path = r"data\data_reactor2.db"
engine = create_engine(f'sqlite:///{db_path}')

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
        # Aquí puedes agregar lógica para manejar los filtros y el formato
        return query

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


class ReaccionQuimicaManejador(BaseManejador):
    def __init__(self):
        super().__init__(ReaccionQuimica)


class RegistroUnidadesManejador(BaseManejador):
    def __init__(self):
        super().__init__(RegistroUnidades)