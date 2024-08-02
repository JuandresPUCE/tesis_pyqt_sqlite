import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Datos experimentales
tiempos = np.array([1.18, 2.88, 5.6, 11.0])
conversiones = np.array([0.2, 0.4, 0.6, 0.8])

# Valores conocidos
A0 = 1.0  # Valor conocido de A0
B0 = 2.0  # Valor conocido de B0
n = 1.0   # Valor conocido de n
a = 1.0   # Valor conocido de a
b = 1.0   # Valor conocido de b

# Definimos la función de la ecuación diferencial
def modelo_bimolecular(X, t, k, m):
    A = A0 * (1 - X)
    B = B0 - (b / a) * A0 * X
    dXdt = k * (A0 ** (n - 1)) * (A ** n) * (B ** m)
    return dXdt

# Función para resolver la ODE
def resolver_ode(params, t, X0):
    k, m = params
    X_sol = odeint(modelo_bimolecular, X0, t, args=(k, m))
    return X_sol.flatten()

# Función de ajuste para curve_fit
def funcion_ajuste(t, k, m):
    X0 = 0  # Conversión inicial
    X_ajustada = resolver_ode([k, m], t, X0)
    return X_ajustada

# Valores iniciales para los parámetros k y m
valor_inicial_k = 1.0  # Valor inicial para k
valor_inicial_m = 1.0  # Valor inicial para m
valores_iniciales = [valor_inicial_k, valor_inicial_m]

# Ajuste de los parámetros usando curve_fit
parametros_optimos, covarianza = curve_fit(funcion_ajuste, tiempos, conversiones, p0=valores_iniciales)

# Imprimir los parámetros óptimos
print("Parámetros óptimos:")
print("k =", parametros_optimos[0])
print("m =", parametros_optimos[1])

# Graficar los datos experimentales y el ajuste
plt.scatter(tiempos, conversiones, label='Datos experimentales')
plt.plot(tiempos, funcion_ajuste(tiempos, *parametros_optimos), label='Ajuste', color='red')
plt.xlabel('Tiempo')
plt.ylabel('Conversión')
plt.legend()
plt.show()
