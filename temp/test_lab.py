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

# Inverso de Lt
df['1/Lt_298.75K'] = 1 / df['Lt_298.75K']
df['1/Lt_308.05K'] = 1 / df['Lt_308.05K']

# Función para ajuste lineal
def linear_func(t, k, c):
    return k * t + c

# Ajuste lineal para T = 298.75 K
popt_29875, _ = curve_fit(linear_func, df['Tiempo (s)'], df['1/Lt_298.75K'])
k_29875 = popt_29875[0]

# Ajuste lineal para T = 308.05 K
popt_30805, _ = curve_fit(linear_func, df['Tiempo (s)'], df['1/Lt_308.05K'])
k_30805 = popt_30805[0]

# Plot de resultados
plt.figure(figsize=(12, 6))

# Gráfico para T = 298.75 K
plt.subplot(1, 2, 1)
plt.scatter(df['Tiempo (s)'], df['1/Lt_298.75K'], label='Datos experimentales')
plt.plot(df['Tiempo (s)'], linear_func(df['Tiempo (s)'], *popt_29875), color='red', label=f'Ajuste lineal (k = {k_29875:.2e} s⁻¹)')
plt.title('Ajuste lineal para T = 298.75 K')
plt.xlabel('Tiempo (s)')
plt.ylabel('1/Lt')
plt.legend()

# Gráfico para T = 308.05 K
plt.subplot(1, 2, 2)
plt.scatter(df['Tiempo (s)'], df['1/Lt_308.05K'], label='Datos experimentales')
plt.plot(df['Tiempo (s)'], linear_func(df['Tiempo (s)'], *popt_30805), color='red', label=f'Ajuste lineal (k = {k_30805:.2e} s⁻¹)')
plt.title('Ajuste lineal para T = 308.05 K')
plt.xlabel('Tiempo (s)')
plt.ylabel('1/Lt')
plt.legend()

plt.tight_layout()
plt.show()

# Imprimir constantes de velocidad
print(f"Constante de velocidad para T = 298.75 K: k = {k_29875:.2e} s⁻¹")
print(f"Constante de velocidad para T = 308.05 K: k = {k_30805:.2e} s⁻¹")
