import matplotlib.pyplot as plt

# Crear datos de ejemplo
x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

# Crear el gráfico
plt.plot(x, y)

# Añadir una ecuación en la posición x=1, y=20
plt.text(1, 20, r'$y=ax^2 + bx + c$', fontsize=15)

# Mostrar el gráfico
plt.show()