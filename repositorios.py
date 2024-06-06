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
        try:
            session = self.Session()
            query = session.query(CondicionesIniciales)

            # Aplicar filtros si se proporcionan
            if not filtros:
                return query.all()
            
            condiciones = []
            for columna, valor in filtros.items():
                if not valor:
                    continue
                if formato == 'like':
                    # Registro con like similar
                    condiciones.append(getattr(CondicionesIniciales, columna).like(f'%{valor}%'))
                else:
                    # Registro exacto
                    condiciones.append(getattr(CondicionesIniciales, columna) == valor)
            
            if condiciones:
                query = query.filter(or_(*condiciones))
            
            return query.all()
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al consultar condición: {e}")
            print(f"Error al consultar datos: {e}")
            return None
        finally:
            session.close()



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
        try:
            condicion = session.query(CondicionesIniciales).filter(CondicionesIniciales.id == id).first()
            if condicion:
                for key, value in new_condicion.items():
                    setattr(condicion, key, value)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró la condición con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al actualizar condición: {e}")
            session.rollback()
            return False
        finally:
            session.close()



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
        try:
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
        
        except Exception as e:
            print(f"Error al consultar datos: {e}")
            return None
        
        finally:
            session.close()

    # Consultar datos por nombre/si no se usa eliminar
    def consultar_conjunto_datos_por_nombre(self, nombre_data):
        session = self.Session()
        datos = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.nombre_data == nombre_data)
        return datos
    
    def consultar_dato_por_id_conjunto_datos(self, id, nombre_data):
        session = self.Session()
        dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id, DatosIngresadosCineticos.nombre_data == nombre_data).first()
        return dato

    def borrar_dato(self, id):
        try:
            session = self.Session()
            # Buscar el dato por su ID
            dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
            
            # Verificar si el dato existe antes de intentar borrarlo
            if dato:
                session.delete(dato)
                session.commit()
                return True
            else:
                # Si el dato no existe, devolver False
                return False
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir durante la operación de borrado
            print(f"Error al borrar el dato: {e}")
            session.rollback()  # Deshacer la operación de borrado
            return False
        finally:
            session.close()  # Cerrar la sesión de la base de datos


    def actualizar_dato(self, id, new_dato):
        session = self.Session()
        try:
            dato = session.query(DatosIngresadosCineticos).filter(DatosIngresadosCineticos.id == id).first()
            if dato:
                for key, value in new_dato.items():
                    setattr(dato, key, value)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró el dato con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al actualizar dato: {e}")
            session.rollback()
            return False
        finally:
            session.close()

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
        try:
            session = self.Session()
            query = session.query(RegistroDataExperimental)

            # Primera cláusula de guarda: Si no se proporcionan filtros, no es necesario aplicar ninguna condición adicional.
            if not filtros:
                return query.all()

            # Aplicar filtros si se proporcionan
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

            # Segunda cláusula de guarda: Si no hay condiciones de filtro válidas definidas, no es necesario aplicar ninguna condición adicional.
            if not condiciones:
                return query.all()

            # Unir todas las condiciones con OR
            query = query.filter(or_(*condiciones))

            # Ejecutar la consulta
            datos = query.all()
            return datos
        except SQLAlchemyError as e:
            # Manejar la excepción SQLAlchemyError
            print("Error de SQLAlchemy:", e)
            # Puedes lanzar una nueva excepción personalizada o retornar un valor predeterminado
            return None
        finally:
            session.close()

    
    def consultar_registro_por_nombre(self, nombre_data):
        session = self.Session()
        datos = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.nombre_data == nombre_data)
        return datos

    def borrar_registro(self, id):
        try:
            session = self.Session()
            # Buscar el registro por su ID
            registro = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.id == id).first()
            
            # Verificar si el registro existe antes de intentar borrarlo
            if registro:
                session.delete(registro)
                session.commit()
                return True
            else:
                # Si el registro no existe, devolver False
                return False
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir durante la operación de borrado
            print(f"Error al borrar el registro: {e}")
            session.rollback()  # Deshacer la operación de borrado
            return False
        finally:
            session.close()  # Cerrar la sesión de la base de datos
    
    def actualizar_registro(self, id, new_registro):
        session = self.Session()
        try:
            registro = session.query(RegistroDataExperimental).filter(RegistroDataExperimental.id == id).first()
            if registro:
                for key, value in new_registro.items():
                    setattr(registro, key, value)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró el registro con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al actualizar registro: {e}")
            session.rollback()
            return False
        finally:
            session.close()

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
        try:
            session = self.Session()
            query = session.query(ReaccionQuimica)

            # Primera cláusula de guarda: Si no se proporcionan filtros, no es necesario aplicar ninguna condición adicional.
            if not filtros:
                return query.all()

            # Aplicar filtros si se proporcionan
            condiciones = []
            for columna, valor in filtros.items():
                if valor:
                    condiciones.append(getattr(ReaccionQuimica, columna).like(f'%{valor}%'))

            # Segunda cláusula de guarda: Si no hay condiciones de filtro válidas definidas, no es necesario aplicar ninguna condición adicional.
            if not condiciones:
                return query.all()

            # Unir todas las condiciones con OR
            query = query.filter(or_(*condiciones))

            # Ejecutar la consulta
            datos = query.all()
            return datos
        except SQLAlchemyError as e:
            # Manejar la excepción SQLAlchemyError
            print("Error de SQLAlchemy:", e)
            # Puedes lanzar una nueva excepción personalizada o retornar un valor predeterminado
            return None
        finally:
            session.close()


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
        try:
            reaccion = session.query(ReaccionQuimica).filter(ReaccionQuimica.id == id).first()
            if reaccion:
                for key, value in new_reaccion.items():
                    setattr(reaccion, key, value)
                session.commit()
                return True
            else:
                logging.warning(f"No se encontró la reacción con id {id}")
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error de SQLAlchemy al actualizar reacción: {e}")
            session.rollback()
            return False
        finally:
            session.close()