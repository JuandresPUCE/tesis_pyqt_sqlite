from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

# van primero
# modelos de la base de datos


# modelo condiciones iniciales
class CondicionesIniciales(Base):
    __tablename__ = "condiciones_iniciales"

    id = Column(Integer, primary_key=True)
    temperatura = Column(Float)
    tiempo = Column(Float)
    presion_total = Column(Float)
    presion_parcial = Column(Float)
    fraccion_molar = Column(Float)
    especie_quimica = Column(String)
    tipo_especie = Column(String)
    detalle = Column(String)
    nombre_data = Column(String)

    def __str__(self):
        return f"ID: {self.id}, Temperatura: {self.temperatura}, Tiempo: {self.tiempo}, Presión Total: {self.presion_total}, Presión Parcial: {self.presion_parcial}, Fracción Molar: {self.fraccion_molar}, Especie Química: {self.especie_quimica}, Tipo de Especie: {self.tipo_especie}, Detalle: {self.detalle}, Nombre de Data: {self.nombre_data}"


# modelo datos cineticos ingresados
class DatosIngresadosCineticos(Base):
    __tablename__ = "datos_ingresados_cineticos"

    id = Column(Integer, primary_key=True)
    tiempo = Column(Float, nullable=False)
    concentracion = Column(Float)
    otra_propiedad = Column(Float)
    conversion_reactivo_limitante = Column(Float)
    tipo_especie = Column(String)
    id_condiciones_iniciales = Column(Integer)
    nombre_data = Column(String)
    nombre_reaccion = Column(String)
    especie_quimica = Column(String)

    def __str__(self):
        return f"ID: {self.id}, Tiempo: {self.tiempo}, Concentración: {self.concentracion}, Otra Propiedad: {self.otra_propiedad}, Conversión Reactivo Limitante: {self.conversion_reactivo_limitante}, Tipo de Especie: {self.tipo_especie}, ID Condiciones Iniciales: {self.id_condiciones_iniciales}, Nombre de Data: {self.nombre_data}, Nombre de Reacción: {self.nombre_reaccion}, Especie Química: {self.especie_quimica}"

class RegistroDataExperimental(Base):
    __tablename__ = "registro_data_experimental"

    id = Column(Integer, primary_key=True)
    nombre_data = Column(String)
    fecha = Column(String)
    detalle = Column(String)

    def __str__(self):
        return f"ID: {self.id}, Nombre Data: {self.nombre_data}, Fecha: {self.fecha}, Detalle: {self.detalle}"

