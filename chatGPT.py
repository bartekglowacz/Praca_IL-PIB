import matplotlib.pyplot as plt
import numpy as np

def quadratic_function(a, b, c, x):
    return a * x**2 + b * x + c

a = 1
b = -3
c = 2
x = np.linspace(-10, 10, 100)
y = quadratic_function(a, b, c, x)

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Wykres funkcji kwadratowej')
plt.grid(True)
plt.show()
