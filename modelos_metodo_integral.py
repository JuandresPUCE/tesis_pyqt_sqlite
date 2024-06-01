from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

class MetodoIntegralModelos:
    
    @staticmethod
    def modelo_n_orden(t, k_ord_n, A_0, n):
        return ((A_0**(1-n))-(1-n)*k_ord_n * t)**(1/(1-n))
    
    @staticmethod
    def modelo_segundo_orden(t, k_ord_2, A_0):
        return 1/((1/A_0) + k_ord_2*t)

    
class MetodoIntegralAjustador:

    @staticmethod
    def ajustar_modelo_n_orden(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, estimacion_inicial_k, n_orden, estimacion_inicial_A0=None):
        # Obtener los datos experimentales
        t_data = np.array((data_cinetica[columna_tiempo]))
        A_data = np.array(data_cinetica[columna_concentracion_reactivo_limitante])

        # Si estimacion_inicial_A0 es None, asignarle el valor de A_data[0]
        if estimacion_inicial_A0 is None:
            estimacion_inicial_A0 = A_data[0]

        # Ajustar el modelo a los datos experimentales para encontrar k_ord_n, A_0 y n
        params, covariance = curve_fit(MetodoIntegralModelos.modelo_n_orden, t_data, A_data, p0=[estimacion_inicial_k, estimacion_inicial_A0, n_orden])

        # Los valores óptimos de k_ord_n, A_0 y n
        k_ord_n_optimo, A_0_optimo, n_optimo = params

        print('k_ord_n_optimo:', k_ord_n_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n_optimo)

        return k_ord_n_optimo, A_0_optimo, n_optimo
    
    @staticmethod
    def ajustar_modelo_segundo_orden(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, estimacion_inicial_k, estimacion_inicial_A0=None):
        # Obtener los datos experimentales
        t_data = np.array((data_cinetica[columna_tiempo]))
        A_data = np.array(data_cinetica[columna_concentracion_reactivo_limitante])

        # Si estimacion_inicial_A0 es None, asignarle el valor de A_data[0]
        if estimacion_inicial_A0 is None:
            estimacion_inicial_A0 = A_data[0]

        # Ajustar el modelo a los datos experimentales para encontrar k_ord_n, A_0 y n
        params, covariance = curve_fit(MetodoIntegralModelos.modelo_segundo_orden, t_data, A_data, p0=[estimacion_inicial_k, estimacion_inicial_A0])

        # Los valores óptimos de k_ord_n, A_0 y n
        k_ord_2_optimo, A_0_optimo = params

        n=2
        print('k_ord_n_optimo:', k_ord_2_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_ord_2_optimo, A_0_optimo, n

class MetodoIntegralGraficador:
    @staticmethod
    def graficar_modelo(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, data_producto, columna_concentracion_producto, k_ord_n_optimo, n_optimo):
        # Graficos de los datos
        plt.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
        plt.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

        # Grafica de la funcion 
        t_data_graf = data_cinetica[columna_tiempo]
        A_data_graf = data_cinetica[columna_concentracion_reactivo_limitante]
        A_0_data_graf = A_data_graf[0]

        A_funcion_n_orden = MetodoIntegralModelos.modelo_n_orden(t_data_graf, k_ord_n_optimo, A_0_data_graf, n_optimo)

 
        plt.plot(t_data_graf, A_funcion_n_orden, label='Modelo de n orden', color='green')
        plt.xlabel('tiempo')
        plt.ylabel('Concentracion ')
        plt.title('Modelo de datos: A vs t')
        plt.legend()
        plt.show()