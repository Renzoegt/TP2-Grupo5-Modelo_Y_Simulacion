# TP2 - Grupo 5
# Ejercicio A.1: Generador Congruencial Lineal (LCG)

#Creamos el LCG (Generador Congruencial Lineal)
def LCG(a, c, m, semilla, n):
    sem = semilla
    for i in range(n):
        sem = (a * sem + c) % m
        yield sem

# Parámetros del LCG
a = 10037
c = 1007
m = 2**32
semilla = 1109
n = 10

# Generamos los números pseudoaleatorios (ô¿ô *)
generador = LCG(a, c, m, semilla, n)
print("=== GENERADOR LCG ===")
print("Números pseudoaleatorios generados por el LCG:")
for numero in generador:
    print(numero)
print()


# Ejercicio A.2: Test Chi-Cuadrado

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, kstest

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
print()

plt.hist(numeros, k, edgecolor='black')
plt.title("Histograma de números pseudoaleatorios")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.show()


# Ejercicio A.3: Test Kolmogorov-Smirnov (K-S)

def ejercicio_a3(numeros):
    n = len(numeros)
    estadistico_ks, p_valor = kstest(numeros, 'uniform')
    valor_critico_ks = 1.36 / np.sqrt(n)
    print("=== TEST KOLMOGOROV-SMIRNOV ===")
    print(f"Estadístico D calculado: {estadistico_ks:.6f}")
    print(f"Valor crítico (5%): {valor_critico_ks:.6f}")
    print(f"p-valor: {p_valor:.6f}")
    if estadistico_ks < valor_critico_ks:
        print("Conclusión: NO se rechaza H0 -> los números parecen uniformes.")
    else:
        print("Conclusión: Se rechaza H0 -> los números NO parecen uniformes.")
    print()
    numeros_ord = np.sort(numeros)
    fda_empirica = np.arange(1, n + 1) / n
    fda_teorica = numeros_ord
    plt.figure(figsize=(8, 5))
    plt.step(numeros_ord, fda_empirica, label='FDA Empírica (LCG)', color='steelblue', linewidth=1.2)
    plt.plot(numeros_ord, fda_teorica, label='FDA Teórica U(0,1)', color='orange', linewidth=1.5, linestyle='--')
    plt.title("Test K-S: FDA Empírica vs. FDA Teórica")
    plt.xlabel("Valor")
    plt.ylabel("Probabilidad acumulada")
    plt.legend()
    plt.grid(True)
    plt.show()

ejercicio_a3(numeros)


# Ejercicio A.4: Comparación LCG vs numpy.random.uniform()

# Generamos 1000 números con numpy
numeros_numpy = np.random.uniform(0, 1, n)

# Prueba Chi-Cuadrado para numpy
frecuencias_obs_numpy, _ = np.histogram(numeros_numpy, k, range=(0, 1))
chi_calculado_numpy = np.sum((frecuencias_obs_numpy - frecuencia_esperada)**2 / frecuencia_esperada)

# Prueba K-S para numpy
estadistico_ks_numpy, p_valor_numpy = kstest(numeros_numpy, 'uniform')
valor_critico_ks = 1.36 / np.sqrt(n)

# Prueba K-S para LCG (para la tabla comparativa)
estadistico_ks_lcg, p_valor_lcg = kstest(numeros, 'uniform')

print("=== COMPARACIÓN LCG vs NUMPY ===")
print(f"\n{'Estadístico':<30} {'LCG':>12} {'NumPy':>12}")
print("-" * 55)
print(f"{'Chi² calculado':<30} {chi_calculado:>12.4f} {chi_calculado_numpy:>12.4f}")
print(f"{'Chi² crítico (5%)':<30} {chi_critico:>12.4f} {chi_critico:>12.4f}")
print(f"{'KS estadístico D':<30} {estadistico_ks_lcg:>12.6f} {estadistico_ks_numpy:>12.6f}")
print(f"{'KS valor crítico (5%)':<30} {valor_critico_ks:>12.6f} {valor_critico_ks:>12.6f}")
print(f"{'KS p-valor':<30} {p_valor_lcg:>12.6f} {p_valor_numpy:>12.6f}")
print("-" * 55)

# Conclusiones Chi²
if chi_calculado < chi_critico:
    print("Chi² LCG   -> No se rechaza H0 -> los números parecen uniformes.")
else:
    print("Chi² LCG   -> Se rechaza H0 -> los números no parecen uniformes.")
if chi_calculado_numpy < chi_critico:
    print("Chi² NumPy -> No se rechaza H0 -> los números parecen uniformes.")
else:
    print("Chi² NumPy -> Se rechaza H0 -> los números no parecen uniformes.")

# Conclusiones K-S
if estadistico_ks_lcg < valor_critico_ks:
    print("K-S LCG    -> No se rechaza H0 -> los números parecen uniformes.")
else:
    print("K-S LCG    -> Se rechaza H0 -> los números no parecen uniformes.")
if estadistico_ks_numpy < valor_critico_ks:
    print("K-S NumPy  -> No se rechaza H0 -> los números parecen uniformes.")
else:
    print("K-S NumPy  -> Se rechaza H0 -> los números no parecen uniformes.")
print()

# Histogramas comparativos LCG vs NumPy
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(numeros, k, edgecolor='black', color='steelblue')
axes[0].set_title("Histograma LCG")
axes[0].set_xlabel("Intervalos")
axes[0].set_ylabel("Frecuencia")
axes[0].grid(True)
axes[1].hist(numeros_numpy, k, edgecolor='black', color='orange')
axes[1].set_title("Histograma numpy.random.uniform()")
axes[1].set_xlabel("Intervalos")
axes[1].set_ylabel("Frecuencia")
axes[1].grid(True)
plt.suptitle("Comparación de distribuciones: LCG vs NumPy")
plt.tight_layout()
plt.show()

# FDA comparativa K-S LCG vs NumPy
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
for ax, nums, label, color in zip(
    axes2,
    [numeros, numeros_numpy],
    ['LCG', 'NumPy'],
    ['steelblue', 'orange']
):
    nums_ord = np.sort(nums)
    fda_emp = np.arange(1, n + 1) / n
    ax.step(nums_ord, fda_emp, label=f'FDA Empírica ({label})', color=color, linewidth=1.2)
    ax.plot(nums_ord, nums_ord, label='FDA Teórica U(0,1)', color='red', linewidth=1.5, linestyle='--')
    ax.set_title(f"Test K-S: FDA Empírica vs. FDA Teórica ({label})")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Probabilidad acumulada")
    ax.legend()
    ax.grid(True)
plt.tight_layout()
plt.show()


# Ejercicio B.1: Generador de Variables Exponencial(λ = 0.8)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest

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
