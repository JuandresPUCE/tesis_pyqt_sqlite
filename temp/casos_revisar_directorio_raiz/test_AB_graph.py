import scipy.integrate as integrate
import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt

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
initial_guess = [3.0, 1.0, 2.0]  # [k, n, m]

# Ajuste de parámetros
params, params_covariance = optimize.curve_fit(fit_func, X_data, t_data, p0=initial_guess)

# Parámetros ajustados
k_fit, n_fit, m_fit = params
print(f"Ajuste de parámetros: k={k_fit}, n={n_fit}, m={m_fit}")

# Resolver A = f(t) usando los parámetros ajustados
def dAdt(t, A, k, B0, b, a, n, m):
    B = B0 - (b / a) * A0 * (1 - A / A0)
    return -k * (A**n) * (B**m)

A0 = 1.0  # Valor constante
B0 = 1.0  # Valor constante
b = 1.0   # Valor constante
a = 1.0   # Valor constante

# Resolver la ODE
t_span = (0, max(t_data))
A_initial = A0
sol = integrate.solve_ivp(dAdt, t_span, [A_initial], args=(k_fit, B0, b, a, n_fit, m_fit), t_eval=np.linspace(0, max(t_data), 100))

# Imprimir y graficar los resultados
t_values = sol.t
A_values = sol.y[0]

plt.figure()
plt.plot(t_values, A_values, label='A(t)')
plt.scatter(t_data, A0 * (1 - X_data), color='red', label='Datos experimentales')
plt.xlabel('Tiempo')
plt.ylabel('Concentración de A')
plt.legend()
plt.title('Concentración de A en función del tiempo')
plt.show()

# Imprimir ecuación diferencial
print(f"dA/dt = {k_fit:.4f} * A^{n_fit:.4f} * (B0 - (b / a) * A0 * (1 - A / A0))^{m_fit:.4f}")

# Imprimir ecuación A = f(t)
for t, A in zip(t_values, A_values):
    print(f"t = {t:.2f}, A = {A:.4f}")

# Imprimir ecuación A' = f(A)
A_prime_values = dAdt(t_values, A_values, k_fit, B0, b, a, n_fit, m_fit)
for A, A_prime in zip(A_values, A_prime_values):
    print(f"A = {A:.4f}, dA/dt = {A_prime:.4f}")
