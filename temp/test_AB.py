import scipy.integrate as integrate
import scipy.optimize as optimize
import numpy as np

# Definimos la función integrando
def integrand(X, k, A0, B0, b, a, n, m):
    A = A0 * (1 - X)
    B = B0 - (b / a) * A0 * X
    return 1 / (k * (A**n) * (B**m))

# Función para realizar la integración numérica
def compute_time(X, k, A0, B0, b, a, n, m):
    result, _ = integrate.quad(integrand, 0, X, args=(k, A0, B0, b, a, n, m))
    return result

# Función de ajuste
def fit_func(X, k, n, m):
    A0 = 1.0  # Valor constante
    B0 = 1.0  # Valor constante
    b = 1.0   # Valor constante
    a = 1.0   # Valor constante
    return np.array([compute_time(x, k, A0, B0, b, a, n, m) for x in X])

# Datos experimentales (ejemplo)
X_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
t_data = np.array([0.5, 1.2, 1.9, 2.6, 3.3])

# Parámetros iniciales
initial_guess = [1.0, 1.0, 1.0]  # [k, n, m]

# Ajuste de parámetros
params, params_covariance = optimize.curve_fit(fit_func, X_data, t_data, p0=initial_guess)

# Parámetros ajustados
k_fit, n_fit, m_fit = params
print(f"Ajuste de parámetros: k={k_fit}, n={n_fit}, m={m_fit}")
