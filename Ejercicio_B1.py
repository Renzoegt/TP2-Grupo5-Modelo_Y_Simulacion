# Ejercicio B.1: Generador de Variables Exponencial(λ = 0.8)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, expon

# Parámetros
lam = 0.8          
n_muestras = 500   

# Generamos 500 números utilizando el LCG de A.1
a = 10037
c = 1007
m = 2**32
semilla = 1109

def LCG(a, c, m, semilla, n):
    sem = semilla
    for _ in range(n):
        sem = (a * sem + c) % m
        yield sem

# Generar los 500 valores U(0,1) con el LCG
generador_b1 = LCG(a, c, m, semilla, n_muestras)
U = np.array([x / m for x in generador_b1])

# Transformada Inversa: X = -ln(U) / λ
X = -np.log(U) / lam

# Test K-S
# Para Exponencial(λ), la FDA es F(x) = 1 - e^(-λx)
# scipy usa la escala = 1/λ
estadistico_ks, p_valor_ks = kstest(X, 'expon', args=(0, 1/lam))
valor_critico_ks = 1.36 / np.sqrt(n_muestras)

print("=== VARIABLE EXPONENCIAL (λ = 0.8) ===")
print(f"\nTest Kolmogorov-Smirnov:")
print(f" Estadístico D calculado: {estadistico_ks:.6f}")
print(f" Valor crítico (5%): {valor_critico_ks:.6f}")
print(f" p-valor: {p_valor_ks:.6f}")
if estadistico_ks < valor_critico_ks:
    print("  Conclusión: NO se rechaza H0 -> las muestras siguen una Exp(0.8).")
else:
    print("  Conclusión: Se rechaza H0 -> las muestras NO siguen una Exp(0.8).")

# Tabla de estadísticos
media_muestral = np.mean(X)
varianza_muestral = np.var(X, ddof=1)
minimo_muestral = np.min(X)
maximo_muestral = np.max(X)

media_teorica = 1 / lam           
varianza_teorica = 1 / lam**2        

print(f"\nTabla de estadísticos (500 muestras):")
print(f"{'Estadístico':<20} {'Muestral':>12} {'Teórico':>12}")
print("-" * 45)
print(f"{'Media':<20} {media_muestral:>12.4f} {media_teorica:>12.4f}")
print(f"{'Varianza':<20} {varianza_muestral:>12.4f} {varianza_teorica:>12.4f}")
print(f"{'Mínimo':<20} {minimo_muestral:>12.4f} {'-':>12}")
print(f"{'Máximo':<20} {maximo_muestral:>12.4f} {'-':>12}")

# Histograma
x_curva = np.linspace(0, np.max(X) + 0.5, 300)
y_curva = lam * np.exp(-lam * x_curva)   

plt.figure(figsize=(9, 5))
plt.hist(X, bins=30, density=True, edgecolor='black', color='steelblue', alpha=0.7, label='Muestras LCG (densidad)')
plt.plot(x_curva, y_curva, color='red', linewidth=2, label=f'Curva teórica Exp(λ={lam})')
plt.title("B.1 – Histograma Exponencial(λ=0.8) con curva teórica")
plt.xlabel("Tiempo entre llegadas (min)")
plt.ylabel("Densidad")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()