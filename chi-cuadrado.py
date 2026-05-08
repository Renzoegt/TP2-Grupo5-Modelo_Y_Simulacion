import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

def LCG(a, c, m, semilla, n):
    sem = semilla
    for _ in range(n):
        sem = (a * sem + c) % m
        yield sem

# Parámetros del LCG
a = 10037
c = 1007
m = 2**32
semilla = 1109
n = 1000

# Generar números pseudoaleatorios U(0,1)
generador = LCG(a, c, m, semilla, n)
numeros = np.array([x / m for x in generador])

# Prueba de Chi-Cuadrado
k = 10
gl = k - 1
frecuencias_obs, _ = np.histogram(numeros, k, range=(0, 1))
frecuencia_esperada = n / k

chi_calculado = np.sum((frecuencias_obs - frecuencia_esperada)**2 / frecuencia_esperada)

# Valor crítico al 5%
alpha = 0.05 # Probabilidad de cometer error Tipo I
chi_critico = chi2.ppf(1 - alpha, gl)

print("=== TEST CHI-CUADRADO ===")
print(f"Frecuencias observadas: {frecuencias_obs}")
print(f"Chi-cuadrado calculado: {chi_calculado:.4f}")
print(f"Grados de libertad: {gl}")
print(f"Valor crítico (5%): {chi_critico:.4f}")

if chi_calculado < chi_critico:
    print("Conclusión: NO se rechaza H0 -> los números parecen uniformes.")
else:
    print("Conclusión: Se rechaza H0 -> los números NO parecen uniformes.")

plt.hist(numeros, k, edgecolor='black')
plt.title("Histograma de números pseudoaleatorios")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.show()