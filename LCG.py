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
print("Números pseudoaleatorios generados por el LCG:")
for numero in generador:
    print(numero)
