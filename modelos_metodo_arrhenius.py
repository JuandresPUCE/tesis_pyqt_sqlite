from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

class ArrheniusModelos:

    @staticmethod
    def modelo_arrhenius_lineal_multiple(T, k_0, energia_activacion_R, escala_temperatura):
        # Convertir T a T_absolutas
        if escala_temperatura == 'C':
            T_absoluta = T + 273.15  # Convertir a Kelvin
        elif escala_temperatura == 'F':
            T_absoluta = T + 459.67  # Convertir a Rankine
        #asignar Tabsolutas
        elif escala_temperatura == 'K':
            T_absoluta = T
        elif escala_temperatura == 'R':
            T_absoluta = T
        else:
            raise ValueError("Escala de temperatura no reconocida. Elija entre 'C', 'F', 'K' o 'R'.")
        # cambiar temperatura_absoluta a su reciproco
        reciproco_T = (1/T_absoluta)
        # relacion de Arrhenius
        lnk_0= np.log(k_0)
        
        lnk=lnk_0 - energia_activacion_R * (reciproco_T)
        return lnk

class ArrheniusAjustador:

    @staticmethod
    def ajustar_modelo_arrhenius_lineal_multiple(data_cinetica,columna_temperatura,columna_contante_cinetica, escala_temperatura):
        # Extraer datos
        T_data = np.array(data_cinetica[columna_temperatura])
        k_data = np.array(data_cinetica[columna_contante_cinetica])
        # Tomar el logaritmo natural de k
        ln_k = np.log(k_data)
        # Ajustar los datos usando curve_fit
        popt, pcov = curve_fit(lambda T, k_0, energia_activacion_R: ArrheniusModelos.modelo_arrhenius_lineal_multiple(T, k_0, energia_activacion_R, escala_temperatura), T_data, ln_k)
        k_0, energia_activacion_R = popt
        ln_k0 = np.log(k_0)
        print(f"K0: {k_0:.6e}")
        print(f"ln(K0): {ln_k0}")
        print(f"EA/R: {energia_activacion_R}")
        
        return k_0,ln_k0, energia_activacion_R

class ArrheniusGraficador:
    
    @staticmethod
    def graficar_modelo_arrhenius_lineal_multiple(data_cinetica, columna_temperatura, columna_contante_cinetica, escala_temperatura, k_0, energia_activacion_R):

        pass