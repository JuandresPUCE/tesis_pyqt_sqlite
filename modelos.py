from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import *
from sqlalchemy.ext import *
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
        return f"id: {self.id}, temperatura: {self.temperatura}, tiempo: {self.tiempo}, presion_total: {self.presion_total}, presion_parcial: {self.presion_parcial}, fraccion_molar: {self.fraccion_molar}, especie_quimica: {self.especie_quimica}, tipo_especie: {self.tipo_especie}, detalle: {self.detalle}, nombre_data: {self.nombre_data}"


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
       return f"id: {self.id}, tiempo: {self.tiempo}, concentracion: {self.concentracion}, otra_propiedad: {self.otra_propiedad}, conversion_reactivo_limitante: {self.conversion_reactivo_limitante}, tipo_especie: {self.tipo_especie}, id_condiciones_iniciales: {self.id_condiciones_iniciales}, nombre_data: {self.nombre_data}, nombre_reaccion: {self.nombre_reaccion}, especie_quimica: {self.especie_quimica}"

#   modelo de registro de data experimental
class RegistroDataExperimental(Base):
    __tablename__ = "registro_data_experimental"

    id = Column(Integer, primary_key=True)
    nombre_data = Column(String)
    fecha = Column(String)
    detalle = Column(String)

    def __str__(self):
        return f"id: {self.id}, nombre_data: {self.nombre_data}, fecha: {self.fecha}, detalle: {self.detalle}"

#   modelo de registro de reaccion química
class ReaccionQuimica(Base):
    __tablename__ = "reaccion_quimica"

    id = Column(Integer, primary_key=True)
    especie_quimica = Column(String)
    formula = Column(String)
    coeficiente_estequiometrico = Column(Float)
    detalle = Column(String)
    tipo_especie = Column(String)
    nombre_reaccion = Column(String)

    def __str__(self):
        return f"id: {self.id}, especie_quimica: {self.especie_quimica}, formula: {self.formula}, coeficiente_estequiometrico: {self.coeficiente_estequiometrico}, detalle: {self.detalle}, tipo_especie: {self.tipo_especie}, nombre_reaccion: {self.nombre_reaccion}"
    
#   modelo de registro de unidades
class RegistroUnidades(Base):
    __tablename__ = "registro_unidades"

    id = Column(Integer, primary_key=True)
    presion= Column(String)
    temperatura = Column(String)
    tiempo = Column(String)
    concentracion = Column(String)
    energia= Column(String)

    nombre_data = Column(String)

    def __str__(self):
        return f"id: {self.id}, presion: {self.presion}, temperatura: {self.temperatura}, tiempo: {self.tiempo}, concentracion: {self.concentracion}, energia: {self.energia}, nombre_data: {self.nombre_data}"

# modelo de datos de salida
class DatosSalida(Base):
    __tablename__ = "datos_salida"

    id = Column(Integer, primary_key=True)
    nombre_data_salida = Column(String)
    fecha = Column(String)
    id_nombre_data = Column(Integer)
    id_condiciones_iniciales = Column(Integer)
    id_registro_unidades = Column(Integer)
    r_utilizada = Column(Float)
    nombre_data = Column(String)
    nombre_reaccion = Column(String)
    delta_n_reaccion = Column(Float)
    epsilon_reactivo_limitante = Column(Float)
    tipo_especie = Column(String)
    especie_quimica = Column(String)
    constante_cinetica = Column(Float)
    orden_reaccion = Column(Float)
    modelo_cinetico = Column(String)
    tipo_calculo = Column(String)
    energia_activacion = Column(Float)
    detalles = Column(String)

    def __str__(self):
        return f"id: {self.id}, nombre_data_salida: {self.nombre_data_salida}, fecha: {self.fecha}, id_nombre_data: {self.id_nombre_data}, id_condiciones_iniciales: {self.id_condiciones_iniciales}, nombre_data: {self.nombre_data}, nombre_reaccion: {self.nombre_reaccion}, delta_n_reaccion: {self.delta_n_reaccion}, epsilon_reactivo_limitante: {self.epsilon_reactivo_limitante},tipo_especie: {self.tipo_especie}, especie_quimica: {self.especie_quimica}, constante_cinetica: {self.constante_cinetica}, orden_reaccion: {self.orden_reaccion}, modelo_cinetico: {self.modelo_cinetico}, tipo_calculo: {self.tipo_calculo}, energia_activacion: {self.energia_activacion}, detalles: {self.detalles}"