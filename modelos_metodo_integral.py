from scipy.optimize import curve_fit
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
import pandas as pd

class MetodoIntegralModelos:
    
    @staticmethod
    def modelo_n_orden(t, k_ord_n, A_0, n):
        return ((A_0**(1-n))-(1-n)*k_ord_n * t)**(1/(1-n))
    
    @staticmethod
    def modelo_cero_orden(t, k_ord_0, A_0, n=None):
        return A_0-k_ord_0*t

    @staticmethod
    def modelo_primer_orden(t, k_ord_1, A_0,n=None):
        return A_0*np.exp(-k_ord_1*t)
    
    @staticmethod
    def modelo_segundo_orden(t, k_ord_2, A_0,n=None):
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

        # Generar la cadena de texto con la ecuación del modelo ajustado
        ecuacion_texto = f'$A(t) = \\left(\\left({A_0_optimo:.4e}^{{(1-{n_optimo:.4f})}}\\right) - (1-{n_optimo:.4f}) \cdot {k_ord_n_optimo:.4e} \cdot t\\right)^{{\\frac{{1}}{{1-{n_optimo:.4f}}}}}$'
        ecuacion_texto_cadena = f"A(t) = ({A_0_optimo:.4e}^(1-{n_optimo:.4f}) - (1-{n_optimo:.4f}) * {k_ord_n_optimo:.4e} * t)^(1/(1-{n_optimo:.4f}))"

        print('k_ord_n_optimo:', k_ord_n_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n_optimo)


        return k_ord_n_optimo, A_0_optimo, n_optimo, 'modelo_n_orden' , ecuacion_texto,ecuacion_texto_cadena
    
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

        # Generar la cadena de texto con la ecuación del modelo ajustado
        ecuacion_texto = f'$A(t) = {A_0_optimo:.4e} \cdot e^{{-{k_ord_1_optimo:.4e} \cdot t}}$'
        ecuacion_texto_cadena = f"A(t) = {A_0_optimo:.4e} * e^(-{k_ord_1_optimo:.4e} * t)"

        print('k_ord_n_optimo:', k_ord_1_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_ord_1_optimo, A_0_optimo, n, 'modelo_primer_orden' , ecuacion_texto,ecuacion_texto_cadena
    
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
        # Generar la cadena de texto con la ecuación del modelo ajustado
        ecuacion_texto = (f'$A(t) = \\frac{{1}}{{\\left(\\frac{{1}}{{{A_0_optimo:.4e}}}\\right) + {k_ord_2_optimo:.4e} \cdot t}}$')
        ecuacion_texto_cadena = f"A(t) = 1/((1/{A_0_optimo:.4e}) + {k_ord_2_optimo:.4e} * t)"

        print('k_ord_n_optimo:', k_ord_2_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_ord_2_optimo, A_0_optimo, n , 'modelo_segundo_orden', ecuacion_texto,ecuacion_texto_cadena
    
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
            nombre_modelo = 'modelo_primer_orden'
        elif n == 2:
            modelo = MetodoIntegralModelos.modelo_segundo_orden
            nombre_modelo = 'modelo_segundo_orden'
        elif n == 0:
            modelo = MetodoIntegralModelos.modelo_cero_orden
            nombre_modelo = 'modelo_cero_orden'
        else:
            raise ValueError("Solo se admiten modelos de primer (n=1), segundo (n=2) orden y orden cero (n=0).")

        # Ajustar el modelo a los datos experimentales para encontrar k_ord_n y A_0
        params, covariance = curve_fit(modelo, t_data, A_data, p0=[estimacion_inicial_k, estimacion_inicial_A0])

        # Los valores óptimos de k_ord_n y A_0
        k_optimo, A_0_optimo = params

        if nombre_modelo == 'modelo_n_orden':
            ecuacion_texto = f'$A(t) = \\left(\\left({A_0_optimo:.4e}^{{(1-{n:.4e})}}\\right) - (1-{n}) \cdot {k_optimo:.4e} \cdot t\\right)^{{\\frac{{1}}{{1-{n:.4e}}}}}$'
            ecuacion_texto_cadena = f"A(t) = ({A_0_optimo:.4e}^(1-{n:.4e}) - (1-{n:.4e}) * {k_optimo:.4e} * t)^(1/(1-{n:.4e}))"
        elif nombre_modelo == 'modelo_cero_orden':
            ecuacion_texto = f'$A(t) = {A_0_optimo:.4e} - {k_optimo:.4e} \cdot t$'
            ecuacion_texto_cadena = f"A(t) = {A_0_optimo:.4e} - {k_optimo:.4e} * t"
        elif nombre_modelo == 'modelo_primer_orden':
            ecuacion_texto = f'$A(t) = {A_0_optimo:.4e} \cdot e^{{-{k_optimo:.4e} \cdot t}}$'
            ecuacion_texto_cadena = f"A(t) = {A_0_optimo:.4e} * e^(-{k_optimo:.4e} * t)"
        elif nombre_modelo == 'modelo_segundo_orden':
            ecuacion_texto = (f'$A(t) = \\frac{{1}}{{\\left(\\frac{{1}}{{{A_0_optimo:.4e}}}\\right) + {k_optimo:.4e} \cdot t}}$')
            ecuacion_texto_cadena = f"A(t) = 1/((1/{A_0_optimo:.4e}) + {k_optimo:.4e} * t)"
            

        print('k_ord_n_optimo:', k_optimo)
        print('A_0_optimo:', A_0_optimo)
        print('n_optimo:', n)

        return k_optimo, A_0_optimo, n , nombre_modelo , ecuacion_texto,ecuacion_texto_cadena
    @staticmethod
    def ajustar_modelo_bimolecular(data_cinetica, columna_tiempo, columna_conversion, estimacion_inicial_k, coeficiente_a, coeficiente_b, data_auxiliar,n=None, m=None):
        # Solicitar el valor de n al usuario si no se proporciona
        if n is None:
            while True:
                try:
                    n, ok_n = QInputDialog.getDouble(None, "Entrada de Valor", "Ingrese el valor de n:", decimals=4)
                    if not ok_n:
                        QMessageBox.warning(None, "Advertencia", "Operación cancelada por el usuario.")
                        return None
                    break  # Salir del bucle si la entrada es válida
                except ValueError:
                    QMessageBox.critical(None, "Error", "Por favor, ingrese un número válido para n.")

        # Solicitar el valor de m al usuario si no se proporciona
        if m is None:
            while True:
                try:
                    m, ok_m = QInputDialog.getDouble(None, "Entrada de Valor", "Ingrese el valor de estimacion_inicial_m:", decimals=4)
                    if not ok_m:
                        QMessageBox.warning(None, "Advertencia", "Operación cancelada por el usuario.")
                        return None
                    break  # Salir del bucle si la entrada es válida
                except ValueError:
                    QMessageBox.critical(None, "Error", "Por favor, ingrese un número válido para estimacion_inicial_m.")

        t_data = data_cinetica[columna_tiempo]
        conversiones_data = data_cinetica[columna_conversion]
        A_concentracion = data_cinetica['concentracion']

        filtro_A0 = (data_auxiliar['tipo_especie'] == 'reactivo_limitante') & (data_auxiliar['tiempo'] == 0) & (data_auxiliar['conversion_reactivo_limitante'] == 0)
        filtro_B0 = (data_auxiliar['tipo_especie'] == 'reactivo') & (data_auxiliar['tiempo'] == 0) & (data_auxiliar['conversion_reactivo_limitante'] == 0)

        B_concentracion = data_auxiliar.loc[filtro_B0, 'concentracion']
        B0 = data_auxiliar.loc[filtro_B0, 'concentracion'].iloc[0]
        A0 = data_auxiliar.loc[filtro_A0, 'concentracion'].iloc[0]
        print('A0:', A0)
        print('B0:', B0)

        # Definimos la función de la ecuación diferencial
        def modelo_bimolecular(X, t, k, n, m):
            A = A0 * (1 - X)
            B = B0 - (coeficiente_b / coeficiente_a) * A0 * X
            dXdt = k * (A0 ** (n-1)) * (A ** n) * (B ** m)
            return dXdt

        # Función para resolver la ODE
        def resolver_ode(params, t, X0):
            k, n, m = params
            X_sol = odeint(modelo_bimolecular, X0, t, args=(k, n, m), atol=1e-8, rtol=1e-8)
            return X_sol.flatten()

        # Función de ajuste para curve_fit
        def funcion_ajuste(t, k, n, m):
            X0 = 0  # Conversión inicial
            X_ajustada = resolver_ode([k, n, m], t, X0)
            return X_ajustada

        # Valores iniciales para los parámetros k, n y m
        valores_iniciales = [estimacion_inicial_k, n, m]

        # Ajuste de los parámetros usando curve_fit
        parametros_optimos, covarianza = curve_fit(funcion_ajuste, t_data, conversiones_data, p0=valores_iniciales)

        # Los valores óptimos de k, n y m
        k_optimo, n_optimo, m_optimo = parametros_optimos

        # Generar la cadena de texto con la ecuación del modelo ajustado
        ecuacion_texto = f'$-\\frac{{dA}}{{dt}} = {k_optimo:.4e} A^{{{n_optimo:.4f}}} B^{{{m_optimo:.4f}}}$'
        ecuacion_texto_cadena = f"-dA/dt = {k_optimo:.4e} * A^{{{n_optimo:.4f}}} * B^{{{m_optimo:.4f}}}"

        # Imprimir los parámetros óptimos
        print('k_optimo:', k_optimo)
        print('n_optimo:', n_optimo)
        print('m_optimo:', m_optimo)

        # Usar los parámetros óptimos para calcular los valores ajustados
        X_ajustada = funcion_ajuste(t_data, *parametros_optimos)
        A_ajustada = A0 * (1 - X_ajustada)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(t_data, A_concentracion, label='Datos experimentales reactivo limitante', color='blue')
        ax.plot(t_data, A_ajustada, label='Ajuste', color='red')
        ax.text(0.02, 0.5, ecuacion_texto, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Concentración')
        ax.set_title('Ajuste del Modelo Bimolecular')
        ax.legend()
        ax.grid(True)

        # Verificar si la carpeta 'temp' existe, si no, crearla
        if not os.path.exists('temp'):
            os.makedirs('temp')

        # Ruta de la imagen
        ruta_imagen = 'temp/temp_bimol.png'

        # Guardar la imagen en la carpeta 'temp' con el nombre 'temp_bimol.png'
        plt.savefig(ruta_imagen, format='png')
        plt.close(fig)

        return k_optimo, A0, n_optimo, 'modelo_bimolecular', ecuacion_texto, ecuacion_texto_cadena, ruta_imagen
    

#ämetodo ocupado dashboard
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
            ax.set_title('Modelo de datos: reactivo limitante vs tiempo')
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


    @staticmethod
    def graficar_modelo_salida_opcional_ecuacion(data_cinetica, columna_tiempo, columna_concentracion_reactivo_limitante, k_ord_n_optimo, A_0_optimo, n_optimo, modelo_tipo, ecuacion_texto=None, data_producto=None, columna_concentracion_producto=None, grafico=None, ax=None, canvas=None):
        # Graficos de los datos
        if grafico == "MatplotlibWidget":
            print("Iniciando graficado con MatplotlibWidget")
            print(f"Datos cinéticos: {data_cinetica}")
            print(f"k_ord_n_optimo: {k_ord_n_optimo}, A_0_optimo: {A_0_optimo}, n_optimo: {n_optimo}")

            ax.clear()  # Limpiar el eje para una nueva gráfica
            ax.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
            
            if data_producto is not None and columna_concentracion_producto is not None:
                ax.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

            # Seleccionar el modelo correspondiente y calcular la función
            if modelo_tipo == 'modelo_primer_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_primer_orden
            elif modelo_tipo == 'modelo_segundo_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_segundo_orden
            elif modelo_tipo == 'modelo_n_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_n_orden
            elif modelo_tipo == 'modelo_cero_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_cero_orden
            else:
                raise ValueError("Tipo de modelo no reconocido.")

            # Grafica de la función correspondiente al tipo de modelo
            t_data_graf = data_cinetica[columna_tiempo]
            A_funcion = modelo_funcion(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo)
            print(f"Valores calculados para la función {modelo_tipo}:", A_funcion)
           
            ax.plot(t_data_graf, A_funcion, label=f'{modelo_tipo.replace("_", " ")}', color='green')
            # Agregar la ecuación al gráfico
            ax.text(0.02, 0.5, ecuacion_texto, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
            ax.set_xlabel('Tiempo')
            ax.set_ylabel('Concentración')
            ax.set_title(f'Modelo de datos: Reactivo limitante vs Tiempo ({modelo_tipo.replace("_", " ")})')
            ax.legend()                       
            canvas.draw()  # Actualizar el lienzo con el nuevo gráfico
        else:
            plt.plot(data_cinetica[columna_tiempo], data_cinetica[columna_concentracion_reactivo_limitante], linestyle=':', label='A', color='orange', linewidth=5)
            
            if data_producto is not None and columna_concentracion_producto is not None:
                plt.plot(data_producto[columna_tiempo], data_producto[columna_concentracion_producto], linestyle='--', label='R', color='cyan', linewidth=1)

            # Seleccionar el modelo correspondiente y calcular la función
            if modelo_tipo == 'modelo_primer_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_primer_orden
            elif modelo_tipo == 'modelo_segundo_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_segundo_orden
            elif modelo_tipo == 'modelo_n_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_n_orden
            elif modelo_tipo == 'modelo_cero_orden':
                modelo_funcion = MetodoIntegralModelos.modelo_cero_orden
            else:
                raise ValueError("Tipo de modelo no reconocido.")

            # Grafica de la función correspondiente al tipo de modelo
            t_data_graf = data_cinetica[columna_tiempo]
            A_funcion = modelo_funcion(t_data_graf, k_ord_n_optimo, A_0_optimo, n_optimo)

            plt.plot(t_data_graf, A_funcion, label=f'{modelo_tipo.replace("_", " ")}', color='green')
            # Agregar la ecuación al gráfico
            plt.text(0.02, 0.5, ecuacion_texto, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
            plt.xlabel('Tiempo')
            plt.ylabel('Concentración')
            plt.title(f'Modelo de datos: A vs Tiempo ({modelo_tipo.replace("_", " ")})')
            plt.legend()
            plt.show()