import math
import matplotlib.pyplot as plt

def LCG(a, c, m, semilla):
    sem = semilla
    while True:
        sem = (a * sem + c) % m
        yield sem / m

a = 10037
c = 1007
m = 2**32
semilla = 1109

# Parámetros de la simulación
DURACION_TURNO = 480 # 8 horas en minutos
PROB_RETRIAL = 0.3 # 30% de las llamadas que "fallan" vuelven a intentar
ESCALA_RETRIAL = 15 # Las re-llamadas ocurren en promedio 15 min después

# Tasa de llegada variable (NHPP)
# Simula un pico de llamadas al mediodía (minuto 240)
def get_lambda_actual(t):
    # Base de 0.4, subiendo a 1.2 en el pico, y bajando al final
    # Función de intesidad (Campana de Gauss): λ(t) = λ_base + amplitud * exp(-((t - pico)^2) / varianza)
    lambda_base = 0.4
    pico = 240
    amplitud = 0.8
    return lambda_base + amplitud * math.exp(-((t - pico)**2) / 20000)

def simular_call_center_mejorado(dias=1):
    generador = LCG(a, c, m, semilla)
    
    resultados_totales = []

    for dia in range(dias):
        tiempo_actual = 0
        llamadas_exitosas = 0
        llamadas_reintentadas = 0
        lista_retrials = [] # Almacena el tiempo en que ocurrirá la re-llamada
        
        tiempos_llegada = [] # Para el gráfico final

        while tiempo_actual < DURACION_TURNO:
            # Determinamos la tasa λ actual según el tiempo
            lambda_t = get_lambda_actual(tiempo_actual)
            
            # Generar próximo tiempo de inter-arribo (Transformada Inversa)
            u = next(generador)
            interarribo = -math.log(max(u, 1e-10)) / lambda_t
            tiempo_actual += interarribo
            
            if tiempo_actual > DURACION_TURNO:
                break
                
            # Procesamos la llegada
            llamadas_exitosas += 1
            tiempos_llegada.append(tiempo_actual)
            
            # Mejora 2: Mecanismo de Retrials (Simulamos una falla por sistema lleno/ocupado)
            if next(generador) < 0.2: # 20% de probabilidad de saturación
                if next(generador) < PROB_RETRIAL:
                    # Tiempo de espera para volver a llamar (Exponencial)
                    espera = -math.log(max(next(generador), 1e-10)) * ESCALA_RETRIAL
                    tiempo_retrial = tiempo_actual + espera
                    if tiempo_retrial < DURACION_TURNO:
                        lista_retrials.append(tiempo_retrial)

        # Sumamos los re-intentos que efectivamente ocurrieron dentro del turno
        llamadas_reintentadas = len(lista_retrials)
        tiempos_llegada.extend(lista_retrials)
        
        resultados_totales.append({
            'total': llamadas_exitosas + llamadas_reintentadas,
            'originales': llamadas_exitosas,
            'reintentos': llamadas_reintentadas,
            'tiempos': sorted(tiempos_llegada)
        })

    return resultados_totales

resultados = simular_call_center_mejorado(dias=1)[0]

print(f"--- RESULTADOS DE LA SIMULACIÓN MEJORADA ---")
print(f"Llamadas originales (NHPP): {resultados['originales']}")
print(f"Llamadas por re-intento (Retrials): {resultados['reintentos']}")
print(f"Total de carga en el sistema: {resultados['total']}")

# Gráfico de densidad de llamadas para observar el NHPP
plt.figure(figsize=(10, 5))
plt.hist(resultados['tiempos'], bins=24, color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Distribución de Llegadas con Tasa Variable y Re-intentos")
plt.xlabel("Minuto del Turno (0 a 480)")
plt.ylabel("Cantidad de Llamadas")
plt.axvline(240, color='red', linestyle='--', label='Pico de Demanda (NHPP)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()