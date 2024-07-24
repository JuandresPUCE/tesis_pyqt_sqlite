import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Datos
tiempos = np.array([0, 60, 120, 180, 240, 300, 420, 540, 660, 780, 900, 1020, 1140])
conductividades = np.array([31.7, 12.35, 12.21, 11.25, 10.53, 10.11, 9.75, 9.34, 9.31, 9.15, 9.04, 8.96, 8.84])

conductividades_2 = np.array([47.2, 13.75, 12.21, 11.62, 10.95, 10.8, 10.55, 10.05, 9.92, 9.71, 9.68, 9.84, 9.8])

# Parámetros iniciales
L0 = conductividades_2[0]  # Conductividad inicial
Lc = conductividades_2[-1]  # Conductividad final
C = 0.5  # Concentración inicial fija

# Función para la ecuación
def modelo(t, k):
    return Lc + (L0 - Lc) / (k * C * t)

# Ajustar la curva
popt, pcov = curve_fit(modelo, tiempos[1:], conductividades_2[1:], p0=[0.1])

# Parámetro ajustado
k = popt[0]

# Predicción con el modelo ajustado
tiempos_ajustados = np.linspace(0, max(tiempos), 100)
conductividades_2_ajustadas = modelo(tiempos_ajustados, k)

# Graficar resultados
plt.figure()
plt.scatter(tiempos, conductividades_2, color='red', label='Datos')
plt.plot(tiempos_ajustados, conductividades_2_ajustadas, color='blue', label='Modelo Ajustado')
plt.xlabel('Tiempo')
plt.ylabel('Conductividad')
plt.title('Modelo de Conductividad vs. Tiempo')
plt.legend()
plt.show()

print(f"Constante cinética k: {k}")
