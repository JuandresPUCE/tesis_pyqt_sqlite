import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Datos
#T = np.array([20, 50, 100]) + 273.15  # Convertir a Kelvin
#k = np.array([1.2, 1.7, 2.7])

#k=np.array([1.96,37.8])
k=np.array([1.978,37.8])
T=np.array([200,300]) + 273.15

# Tomar el logaritmo natural de k
ln_k = np.log(k)

# Definir la función de Arrhenius
def arrhenius(T, lnK0, EA_R):
    return lnK0 - EA_R * (1 / T)

# Ajustar los datos usando curve_fit
popt, pcov = curve_fit(arrhenius, T, ln_k)
lnK0, EA_R = popt

print(f"ln(K0): {lnK0}")
print(f"EA/R: {EA_R}")

# Para visualizar el ajuste
T_fit = np.linspace(min(T), max(T), 100)
ln_k_fit = arrhenius(T_fit, *popt)

plt.scatter(1/T, ln_k, label='Datos')
plt.plot(1/T_fit, ln_k_fit, label='Ajuste', color='red')
plt.xlabel('1/T (1/K)')
plt.ylabel('ln(k)')
plt.legend()
plt.show()
