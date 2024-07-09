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
    def graficar_modelo_arrhenius_lineal_multiple(data_cinetica, columna_temperatura, columna_contante_cinetica, escala_temperatura, k_0, energia_activacion_R, grafico=None, ax=None, canvas=None):
        # Extraer datos
        T_data = np.array(data_cinetica[columna_temperatura])
        k_data = np.array(data_cinetica[columna_contante_cinetica])
        # Tomar el logaritmo natural de k
        ln_k = np.log(k_data)
        T_fit = np.linspace(min(T_data), max(T_data), 100)

        # Convertir T a T_absolutas
        if escala_temperatura == 'C':
            T_absoluta = T_data + 273.15  # Convertir a Kelvin
            T_fit_absoluta = T_fit + 273.15
        elif escala_temperatura == 'F':
            T_absoluta = T_data + 459.67  # Convertir a Rankine
            T_fit_absoluta = T_fit + 459.67
        #asignar Tabsolutas
        elif escala_temperatura == 'K':
            T_absoluta = T_data
            T_fit_absoluta = T_fit
        elif escala_temperatura == 'R':
            T_absoluta = T_data
            T_fit_absoluta = T_fit
        else:
            raise ValueError("Escala de temperatura no reconocida. Elija entre 'C', 'F', 'K' o 'R'.")
        
        reciproco_T = 1 / T_absoluta
        reciproco_T_fit = 1 / T_fit_absoluta
        # Generar datos ajustados usando el modelo ajustado

        lnK_fit = ArrheniusModelos.modelo_arrhenius_lineal_multiple(T_fit, k_0, energia_activacion_R, escala_temperatura)

        
        if grafico == "MatplotlibWidget":
            print("Iniciando graficado con MatplotlibWidget")
            print(f"Datos cinéticos: {data_cinetica}")
            
            ax.clear()  # Limpiar el eje para una nueva gráfica
            ax.scatter(reciproco_T, ln_k, label='Datos experimentales', color='orange', marker='o')
            ax.plot(reciproco_T_fit, lnK_fit, label='Ajuste del modelo', color='green')
            ax.set_xlabel('1/T (K⁻¹)')
            ax.set_ylabel('ln(k)')
            ax.set_title('Modelo de Arrhenius')
            ax.legend()                       
            canvas.draw()  # Actualizar el lienzo con el nuevo gráfico
        else:
            plt.scatter(reciproco_T, ln_k, label='Datos experimentales', color='orange', marker='o')
            plt.plot(reciproco_T_fit, T_fit_absoluta, label='Ajuste del modelo', color='green')
            plt.xlabel('1/T (K⁻¹)')
            plt.ylabel('ln(k)')
            plt.title('Modelo de Arrhenius')
            plt.legend()
            plt.show()