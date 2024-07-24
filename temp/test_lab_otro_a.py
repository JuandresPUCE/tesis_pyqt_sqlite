import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Datos experimentales
data = {
    "Tiempo (s)": [60, 120, 180, 240, 300, 420, 540, 660, 780, 900, 1020, 1140],
    "Lt_298.75K": [12.35, 12.21, 11.25, 10.53, 10.11, 9.75, 9.34, 9.31, 9.15, 9.04, 8.96, 8.84],
    "Lt_308.05K": [13.75, 12.21, 11.62, 10.95, 10.80, 10.55, 10.05, 9.92, 9.71, 9.68, 9.84, 9.80]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Conductividades iniciales
conductividad_inicial_29875 = 31.7
conductividad_inicial_30805 = 47.2

# Concentración inicial (0.5N)
concentracion_inicial = 0.5

# Relación lineal (asumida) entre conductividad y concentración
a_29875 = concentracion_inicial / conductividad_inicial_29875
a_30805 = concentracion_inicial / conductividad_inicial_30805

# Función para convertir conductividad a concentración
def conductividad_a_concentracion(conductividad, a):
    return a * conductividad

# Convertir conductividad a concentración
df['Concentracion_298.75K'] = conductividad_a_concentracion(df['Lt_298.75K'], a_29875)
df['Concentracion_308.05K'] = conductividad_a_concentracion(df['Lt_308.05K'], a_30805)

# Inverso de concentración
df['1/Concentracion_298.75K'] = 1 / df['Concentracion_298.75K']
df['1/Concentracion_308.05K'] = 1 / df['Concentracion_308.05K']

# Función para ajuste lineal
def linear_func(t, k, c):
    return k * t + c

# Ajuste lineal para T = 298.75 K
popt_29875, _ = curve_fit(linear_func, df['Tiempo (s)'], df['1/Concentracion_298.75K'])
k_29875 = popt_29875[0]

# Ajuste lineal para T = 308.05 K
popt_30805, _ = curve_fit(linear_func, df['Tiempo (s)'], df['1/Concentracion_308.05K'])
k_30805 = popt_30805[0]

# Datos para el gráfico de Arrhenius
T = np.array([298.75, 308.05])  # en K
k = np.array([k_29875, k_30805])  # constantes de velocidad

# Convertir k a ln(k)
ln_k = np.log(k)

# Convertir T a 1/T
inv_T = 1 / T

# Ajuste lineal para Arrhenius
def arrhenius_func(inv_T, A, Ea):
    R = 8.314  # Constante de gas en J/(mol*K)
    return A - (Ea / R) * inv_T

popt_arrhenius, _ = curve_fit(arrhenius_func, inv_T, ln_k)
A = popt_arrhenius[0]
Ea = popt_arrhenius[1]

# Plot de resultados
plt.figure(figsize=(12, 6))

# Gráfico para T = 298.75 K y 308.05 K
plt.subplot(1, 2, 1)
plt.scatter(df['Tiempo (s)'], df['1/Concentracion_298.75K'], label='Datos experimentales (298.75 K)')
plt.plot(df['Tiempo (s)'], linear_func(df['Tiempo (s)'], *popt_29875), color='red', label=f'Ajuste lineal (k = {k_29875:.2e} L/(mol*s))')
plt.scatter(df['Tiempo (s)'], df['1/Concentracion_308.05K'], label='Datos experimentales (308.05 K)')
plt.plot(df['Tiempo (s)'], linear_func(df['Tiempo (s)'], *popt_30805), color='blue', label=f'Ajuste lineal (k = {k_30805:.2e} L/(mol*s))')
plt.title('Ajuste lineal de concentración')
plt.xlabel('Tiempo (s)')
plt.ylabel('1/Concentración (1/N)')
plt.legend()

# Gráfico de Arrhenius
plt.subplot(1, 2, 2)
plt.scatter(inv_T, ln_k, label='Datos experimentales')
plt.plot(inv_T, arrhenius_func(inv_T, *popt_arrhenius), color='green', label=f'Ajuste Arrhenius\nA = {A:.2e}, Ea = {Ea:.2e} J/mol')
plt.title('Gráfico de Arrhenius')
plt.xlabel('1/T (1/K)')
plt.ylabel('ln(k)')
plt.legend()

plt.tight_layout()
plt.show()

# Imprimir constantes de velocidad y parámetros de Arrhenius
print(f"Constante de velocidad para T = 298.75 K: k = {k_29875} L/(mol*s)")
print(f"Constante de velocidad para T = 308.05 K: k = {k_30805} L/(mol*s)")
print(f"Pre-exponencial A: {A:.2e}")
print(f"Energía de activación Ea: {Ea} J/mol")
