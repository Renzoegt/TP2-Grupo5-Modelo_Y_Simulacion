import math
import matplotlib.pyplot as plt

def LCG_u01(a, c, m, semilla, n):
    sem = semilla
    for i in range(n):
        sem = (a * sem + c) % m
        yield sem / m # Normalizamos de manera automática

a = 10037
c = 1007
m = 2**32
semilla = 1109

def correr_simulacion_completa(lambd_objetivo, dias=100):
    generador = LCG_u01(a, c, m, semilla, 100000)
    
    resultados_dias = []
    duracion_turno = 480 # 8 horas
    
    for _ in range(dias):
        tiempo_transcurrido = 0
        conteo_llamadas = 0
        
        while tiempo_transcurrido < duracion_turno:
            try:
                u = next(generador)
                # Método de la Transformada Inversa
                interarribo = -math.log(max(u, 1e-10)) / lambd_objetivo
                tiempo_transcurrido += interarribo
                
                if tiempo_transcurrido <= duracion_turno:
                    conteo_llamadas += 1
            except StopIteration:
                break # Por si se agotan los números del generador
                
        resultados_dias.append(conteo_llamadas)
    return resultados_dias

# --- EJECUCIÓN DE ESCENARIOS ---

lambda_base = 0.8
escenarios = {
    "Base (λ=0.8)": correr_simulacion_completa(lambda_base),
    "Campaña +10% (λ=0.88)": correr_simulacion_completa(lambda_base * 1.1), # +10%
    "Reducción -10% (λ=0.72)": correr_simulacion_completa(lambda_base * 0.9) # -10%
}

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Análisis de Sensibilidad: Simulación Call Center (100 días)', fontsize=16, fontweight='bold')

colors = ['#3498db', '#e74c3c', '#2ecc71']
titulos = list(escenarios.keys())

# Histogramas
for i, (nombre, datos) in enumerate(escenarios.items()):
    ax = axes.flatten()[i]
    ax.hist(datos, bins=15, color=colors[i], edgecolor='black', alpha=0.7)
    ax.set_title(f'Histograma: {nombre}')
    ax.set_xlabel('Llamadas por Turno')
    ax.set_ylabel('Frecuencia (Días)')
    media = sum(datos)/len(datos)
    ax.axvline(media, color='black', linestyle='--', label=f'Media: {media:.1f}')
    ax.legend()

# Gráfico de líneas comparativo
ax_line = axes[1, 1]
for i, (nombre, datos) in enumerate(escenarios.items()):
    ax_line.plot(datos, label=nombre, color=colors[i], linewidth=1.5, alpha=0.8)

ax_line.set_title('Comparativa de Evolución Diaria')
ax_line.set_xlabel('Día de Simulación')
ax_line.set_ylabel('Cantidad de Llamadas')
ax_line.grid(True, linestyle=':', alpha=0.6)
ax_line.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- TABLA DE RESULTADOS (C.1/C.2) ---
print(f"{'Escenario':<25} | {'Media':<10} | {'Máx':<8} | {'Mín':<8} | {'Desv. Est':<10}")
print("-" * 70)
for nombre, datos in escenarios.items():
    media = sum(datos)/len(datos)
    maximo = max(datos)
    minimo = min(datos)
    # Cálculo de desviación estándar manual
    varianza = sum((x - media)**2 for x in datos) / len(datos)
    desv = math.sqrt(varianza)
    print(f"{nombre:<25} | {media:<10.2f} | {maximo:<8} | {minimo:<8} | {desv:<10.2f}")