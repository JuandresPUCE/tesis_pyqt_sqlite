import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import odeint

# Datos de entrada
tiempos = np.array([1.18, 2.88, 5.6, 11.0])
conversiones = np.array([0.2, 0.4, 0.6, 0.8])

# Crear un DataFrame
df = pd.DataFrame({
    'tiempos': tiempos,
    'conversiones': conversiones
})

# Ordenar el DataFrame por la columna de tiempos
df = df.sort_values(by='tiempos')

# Extraer los datos ordenados
tiempos_ordenados = df['tiempos'].values
conversiones_ordenadas = df['conversiones'].values

# Definir el modelo cinético como una función de ODE
def modelo_ode(t, k, n, m, A0, B0, a, b):
    def dA_dt(A, t):
        B = B0 - (b / a) 
        A = A0 * (1 - A / A0)
        return -k * (A**n) * (B**m)
    
    # Inicialización: valor inicial de A
    A0_value = A0 * (1 - conversiones_ordenadas[0])  # Usar el primer valor de conversión
    A = odeint(dA_dt, A0_value, t)
    return A.flatten()

# Definir una función para ajustar el modelo a los datos
def ajustar_modelo(t, k, n, m, A0, B0, a, b):
    return modelo_ode(t, k, n, m, A0, B0, a, b)

# Parámetros fijos para la función de ajuste
A0 = 1
B0 = 2
a = 1
b = 1

# Ajustar el modelo
popt, pcov = curve_fit(lambda t, k, n, m: ajustar_modelo(t, k, n, m, A0, B0, a, b), 
                      tiempos_ordenados, conversiones_ordenadas, p0=[0.1, 1, 1])

# Extraer parámetros óptimos
k_optimo, n_optimo, m_optimo = popt
print(f'Valor óptimo de k: {k_optimo}')
print(f'Valor óptimo de n: {n_optimo}')
print(f'Valor óptimo de m: {m_optimo}')
