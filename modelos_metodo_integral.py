from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

class MetodoIntegralModelos:
    
    @staticmethod
    def modelo_n_orden(t, k_ord_n, A_0, n):
        return ((A_0**(1-n))-(1-n)*k_ord_n * t)**(1/(1-n))
    
    
    @staticmethod
    def modelo_primer_orden(t, k_ord_1, A_0):
        return A_0*np.exp(-k_ord_1*t)
    
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
    def ajustar_modelo_primer_orden(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, estimacion_inicial_k, n, estimacion_inicial_A0=None):
        # Obtener los datos experimentales
        t_data = np.array((data_cinetica[columna_tiempo]))
        A_data = np.array(data_cinetica[columna_concentracion_reactivo_limitante])

        # Si estimacion_inicial_A0 es None, asignarle el valor de A_data[0]
        if estimacion_inicial_A0 is None:
            estimacion_inicial_A0 = A_data[0]

        # Ajustar el modelo a los datos experimentales para encontrar k_ord_n, A_0 y n
        params, covariance = curve_fit(MetodoIntegralModelos.modelo_primer_orden, t_data, A_data, p0=[estimacion_inicial_k, estimacion_inicial_A0])

        # Los valores óptimos de k_ord_n, A_0 y n
        k_ord_1_optimo, A_0_optimo = params

        n=1
        print('k_ord_n_optimo:', k_ord_1_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_ord_1_optimo, A_0_optimo, n
    
    @staticmethod
    def ajustar_modelo_segundo_orden(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, estimacion_inicial_k,n, estimacion_inicial_A0=None):
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
    
    @staticmethod
    def ajustar_modelo(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, estimacion_inicial_k, n, estimacion_inicial_A0=None):
        # Obtener los datos experimentales
        t_data = np.array(data_cinetica[columna_tiempo])
        A_data = np.array(data_cinetica[columna_concentracion_reactivo_limitante])

        # Si estimacion_inicial_A0 es None, asignarle el valor de A_data[0]
        if estimacion_inicial_A0 is None:
            estimacion_inicial_A0 = A_data[0]

        # Seleccionar el modelo basado en el orden n
        if n == 1:
            modelo = MetodoIntegralModelos.modelo_primer_orden
        elif n == 2:
            modelo = MetodoIntegralModelos.modelo_segundo_orden
        else:
            raise ValueError("Solo se admiten modelos de primer (n=1) y segundo (n=2) orden.")

        # Ajustar el modelo a los datos experimentales para encontrar k_ord_n y A_0
        params, covariance = curve_fit(modelo, t_data, A_data, p0=[estimacion_inicial_k, estimacion_inicial_A0])

        # Los valores óptimos de k_ord_n y A_0
        k_optimo, A_0_optimo = params

        print('k_ord_n_optimo:', k_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_optimo, A_0_optimo, n

class MetodoIntegralGraficador:
    @staticmethod
    def graficar_modelo_salida_opcional(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, k_ord_n_optimo, A_0_optimo, n_optimo, data_producto=None, columna_concentracion_producto=None, grafico=None, ax=None, canvas=None):
        # Graficos de los datos
        if grafico == "MatplotlibWidget":
            print("Iniciando graficado con MatplotlibWidget")
            print(f"Datos cinéticos: {data_cinetica}")
            print(f"k_ord_n_optimo: {k_ord_n_optimo}, A_0_optimo: {A_0_optimo}, n_optimo: {n_optimo}")
            
            ax.clear()  # Limpiar el eje para una nueva gráfica
            ax.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
            
            if data_producto is not None and columna_concentracion_producto is not None:
                ax.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

            # Grafica de la funcion 
            t_data_graf = data_cinetica[columna_tiempo]
            A_funcion_n_orden = MetodoIntegralGraficador.calcular_funcion_n_orden(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo)
            print("Valores calculados para la función n-orden:", A_funcion_n_orden)

            ax.plot(t_data_graf, A_funcion_n_orden, label='Modelo de n orden', color='green')
            ax.set_xlabel('tiempo')
            ax.set_ylabel('Concentracion ')
            ax.set_title('Modelo de datos: A vs t')
            ax.legend()
            canvas.draw()  # Actualizar el lienzo con el nuevo gráfico
        else:
            plt.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
            
            if data_producto is not None and columna_concentracion_producto is not None:
                plt.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

            # Grafica de la funcion 
            t_data_graf = data_cinetica[columna_tiempo]
            A_funcion_n_orden = MetodoIntegralGraficador.calcular_funcion_n_orden(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo)

            plt.plot(t_data_graf, A_funcion_n_orden, label='Modelo de n orden', color='green')
            plt.xlabel('tiempo')
            plt.ylabel('Concentracion ')
            plt.title('Modelo de datos: A vs t')
            plt.legend()
            plt.show()

    @staticmethod
    def calcular_funcion_n_orden(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo):
        if n_optimo == 1:
            return MetodoIntegralModelos.modelo_primer_orden(t_data_graf, k_ord_n_optimo, A_0_optimo)
        elif n_optimo == 2:
            return MetodoIntegralModelos.modelo_segundo_orden(t_data_graf, k_ord_n_optimo, A_0_optimo)
        else:
            return MetodoIntegralModelos.modelo_n_orden(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo)
        
    def graficar_modelo(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, data_producto, columna_concentracion_producto, k_ord_n_optimo, n_optimo):
        # Graficos de los datos
        plt.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
        plt.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

        # Grafica de la funcion 
        t_data_graf = data_cinetica[columna_tiempo]
        A_data_graf = data_cinetica[columna_concentracion_reactivo_limitante]
        A_0_data_graf = A_data_graf[0]

        A_funcion_n_orden = MetodoIntegralGraficador.calcular_funcion_n_orden(t_data_graf, k_ord_n_optimo, A_0_data_graf, n_optimo)

 
        plt.plot(t_data_graf, A_funcion_n_orden, label='Modelo de n orden', color='green')
        plt.xlabel('tiempo')
        plt.ylabel('Concentracion ')
        plt.title('Modelo de datos: A vs t')
        plt.legend()
        plt.show()
