import pandas as pd
import matplotlib.pyplot as plt

#para encontrar curvas
from scipy.optimize import curve_fit
import numpy as np

class Funciones:

    def leer_csv(self, archivo, formato_separacion):
        datos_tabulados = pd.read_csv(archivo, sep=formato_separacion) 
        return datos_tabulados
    
        
    # es A o CA en funcion de la conversion

    def concentracion_producto_principal(concentracion_inicial_producto_principal,conversion_producto_principal):
        return concentracion_inicial_producto_principal*(1-conversion_producto_principal)
    
    
    #documentados

    def graficar_datos_experimentales_iniciales(self, datos_eje_horizontal, datos_eje_vertical,
                                                 etiqueta_horizontal, etiqueta_vertical, titulo,componente):
        """
        Grafica los datos experimentales iniciales.

        Esta función grafica los datos experimentales iniciales proporcionados
        en un diagrama de dispersión.

        Args:
            datos_eje_horizontal (array-like): Datos del eje horizontal, como el tiempo.
            datos_eje_vertical (array-like): Datos del eje vertical, como la concentración.
            etiqueta_horizontal (str): Etiqueta del eje horizontal.
            etiqueta_vertical (str): Etiqueta del eje vertical.
            titulo (str): Título del gráfico.

        Returns:
            None
        """
        plt.plot(datos_eje_horizontal, datos_eje_vertical, linestyle=':', label=componente, color='orange', linewidth=5)        
        plt.xlabel(etiqueta_horizontal)  # Tiempo ('t (s)')
        plt.ylabel(etiqueta_vertical)    # Concentración ('Concentracion (mol/L)')
        plt.title(titulo)                # Título del gráfico ('Modelo de datos: A vs t' o similar)
        plt.legend()
        plt.show()


    def concentracion_producto_principal(self,A0, XA):
        """
        Calcula la concentración del producto principal.

        Esta función calcula la concentración del producto principal
        utilizando la concentración inicial del producto principal y
        la conversión de la reacción.

        Args:
            A0 (float): Concentración inicial del producto principal.
            XA conversión del producto principal (float): Conversión de la reacción de 0 a 1 en tanto por uno.

        Returns:
            float: La concentración del producto principal.
        """
        return A0 * (1 - XA)
    
    def conversion_A(self,A0, A):
        """
        Calcula la conversión del producto principal A de la reacción.

        Esta función calcula la conversión de la reacción utilizando
        la concentración inicial del producto principal y la concentración
        actual del producto principal.

        Args:
            A0 (float): Concentración inicial del producto principal.
            A (float): Concentración actual del producto principal.

        Returns:
            float: La conversión de la reacción.
        """
        return 1 - (A / A0)
    
    def concentracion_Producto(self,Producto_0, coeficiente_producto, a, XA, A0):
        """
        Calcula la concentración de un producto de una reacción química.

        Esta función calcula la concentración de un producto de una reacción química
        utilizando la concentración inicial del producto, el coeficiente estequiométrico
        del producto, el coeficiente estequiométrico del reactivo limitante, la conversión
        de la reacción y la concentración inicial del reactivo limitante.

        Args:
            Producto_0 (float): Concentración inicial del producto.
            coeficiente_producto (int): Coeficiente estequiométrico del producto en la ecuación balanceada de la reacción.
            a (int): Coeficiente estequiométrico del reactivo limitante en la ecuación balanceada de la reacción.
            XA (float): Conversión de la reacción.
            A0 (float): Concentración inicial del reactivo limitante.

        Returns:
            float: La concentración del producto en el estado deseado.
        """
        return Producto_0 + (coeficiente_producto / a) * (A0 * XA)
    
    def calcular_delta_n(self,coeficientes_productos, coeficientes_reactivos):
        """
        Calcula el cambio en el número de moles de gas en una reacción química.

        Esta función calcula Δ𝑛 = [ ΣCoeficiente de los Productos] − [ΣCoeficiente de los Reactivos]
        para una reacción química.

        Args:
            coeficientes_productos (list): Lista de coeficientes de los productos en la ecuación química.
            coeficientes_reactivos (list): Lista de coeficientes de los reactivos en la ecuación química.

        Returns:
            int: El cambio en el número de moles de gas.
        """
        suma_productos = sum(coeficientes_productos)
        suma_reactivos = sum(coeficientes_reactivos)
        delta_n = suma_productos - suma_reactivos
        return delta_n

    def calcular_epsilon_A(self,y_A0, delta_n, a):
        """
        Calcula el cambio en la fracción molar del componente A en una mezcla.

        Esta función calcula 𝜀𝐴 = 𝑦𝐴0 * 𝛥𝑛 / 𝑎, donde 𝑦𝐴0 es la fracción molar inicial de A,
        Δ𝑛 es el cambio en el número de moles y 𝑎 es el coeficiente estequiométrico de A.

        Args:
            y_A0 (float): Fracción molar inicial del componente A.
            delta_n (int): Cambio en el número de moles de gas.
            a (int): Coeficiente estequiométrico de A.

        Returns:
            float: El cambio en la fracción molar del componente A en la mezcla.
        """
        epsilon_A = y_A0 * delta_n / a
        return epsilon_A


    def modelo_arrenius_dos_puntos(self,k1, T1, T2, Energia_activacion, escala_temp='K', unidades='J', R_custom=None):
        if escala_temp == 'K':
            T1_absoluta = T1 + 273.15  # Convertir a Kelvin
            T2_absoluta = T2 + 273.15  # Convertir a Kelvin
        elif escala_temp == 'R':
            T1_absoluta = T1 + 459.67  # Convertir a Rankine
            T2_absoluta = T2 + 459.67  # Convertir a Rankine
        else:
            raise ValueError("Escala de temperatura no reconocida. Elija entre 'K' o 'R'.")

        if R_custom is not None:
            R = R_custom
        else:
            if unidades == 'J':
                R = 8.314  # J/(mol K)
            elif unidades == 'atm':
                R = 0.0821  # atm L/(mol K)
            elif unidades == 'cal':
                R = 1.987  # cal/(mol K)
            elif unidades == 'psia*ft3':
                R = 10.73   # psia*ft3/(lbmol R)
            else:
                raise ValueError("Unidades no reconocidas. Elija entre 'J', 'atm', 'cal' o 'psia*ft3'.")

        k2 = k1 * np.exp((-Energia_activacion/R)*(1/T2_absoluta - 1/T1_absoluta))
        
        return k2
    
    def gas_concentracion_componente(self,coeficiente_gas_Z,y_A0,Presion_total,R,Temperatura,escala_temp='K'):
    
        if escala_temp == 'K':
            T_absoluta = Temperatura + 273.15  # Convertir a Kelvin
        elif escala_temp == 'R':
            T_absoluta = Temperatura + 459.67  # Convertir a Rankine
        
        else:
            raise ValueError("Escala de temperatura no reconocida. Elija entre 'K' o 'R'.")

        Presion_parcial_componente = Presion_total*y_A0
        
        concentracion_componente=coeficiente_gas_Z*Presion_parcial_componente/(R*T_absoluta)
        return concentracion_componente


# graficas

    def graficar_datos_experimentales_iniciales_widget(self, datos_eje_horizontal, datos_eje_vertical,
                                                    etiqueta_horizontal, etiqueta_vertical, titulo, componente):
            """
            Grafica los datos experimentales iniciales en el lienzo de Matplotlib.

            Args:
                datos_eje_horizontal (array-like): Datos del eje horizontal, como el tiempo.
                datos_eje_vertical (array-like): Datos del eje vertical, como la concentración.
                etiqueta_horizontal (str): Etiqueta del eje horizontal.
                etiqueta_vertical (str): Etiqueta del eje vertical.
                titulo (str): Título del gráfico.
                componente (str): Etiqueta de la curva en el gráfico.

            Returns:
                None
            """
            # Borrar cualquier gráfico previo en el lienzo
            self.ax.clear()

            # Graficar los datos en el lienzo
            self.ax.plot(datos_eje_horizontal, datos_eje_vertical, linestyle=':', label=componente, color='orange', linewidth=5)
            
            # Configurar etiquetas y título
            self.ax.set_xlabel(etiqueta_horizontal)
            self.ax.set_ylabel(etiqueta_vertical)
            self.ax.set_title(titulo)
            
            # Mostrar la leyenda
            self.ax.legend()

            # Actualizar el lienzo para que se muestre el nuevo gráfico
            self.canvas.draw()

# revisar R https://cruzfierro.com/formularios/R.pdf