import pandas as pd
import numpy as np

# Datos
data = {
    'Tiempo': [0, 60, 120, 180, 240, 300, 420, 540, 660, 780, 900, 1020, 1140],
    'Conductividad': [31.7, 12.35, 12.21, 11.25, 10.53, 10.11, 9.75, 9.34, 9.31, 9.15, 9.04, 8.96, 8.84]
}

df = pd.DataFrame(data)

# Parámetros
λ0 = df['Conductividad'][0]  # Valor en t=0
λ_infinito = df['Conductividad'].iloc[-1]  # Valor en el último tiempo

# Calcular k
def calcular_k(tiempo, λt, λ0, λ_infinito):
    return (2.303 / tiempo) * np.log((λ0 - λ_infinito) / (λt - λ_infinito))

# Aplicar la fórmula
df['k'] = df.apply(lambda row: calcular_k(row['Tiempo'], row['Conductividad'], λ0, λ_infinito) if row['Tiempo'] != 0 else np.nan, axis=1)

print(df)
