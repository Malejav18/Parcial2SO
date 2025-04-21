from multiprocessing.dummy import Pool as ThreadPool
from threading import Semaphore, Lock
import time
import random
from datetime import datetime

def log_event(nombre, estado):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {nombre}: {estado}")

def usar_bus(nombre):
    while time.time() - inicio_simulacion < DURACION_SIMULACION:
        log_event(nombre, f"🔄 Quiere acceder al bus...")
        tiempo_inicio_espera = time.time()

        bus_semaforo.acquire()
        tiempo_espera = round(time.time() - tiempo_inicio_espera, 2)
        tiempo_uso = round(random.uniform(1.0, 2.0), 2)

        with consola_lock:
            log_event(nombre, f"✅ Acceso tras {tiempo_espera}s.")
            log_event(nombre, f"📡 Enviando datos durante {tiempo_uso}s...")

        time.sleep(tiempo_uso)

        with consola_lock:
            log_event(nombre, f"⬅️ Liberó el bus tras {tiempo_uso}s.")

        bus_semaforo.release()

        pausa = round(random.uniform(0.5, 1.5), 2)
        log_event(nombre, f"💤 Esperando {pausa}s antes de volver a intentar...\n")
        time.sleep(pausa)

# Configuración global
bus_semaforo = Semaphore(1)
consola_lock = Lock()
nombres = [f"Dispositivo {chr(65+i)}" for i in range(4)]  # A, B, C, D
DURACION_SIMULACION = 50

# Iniciar simulación
print(f"\n🔁 Iniciando simulación durante {DURACION_SIMULACION} segundos...\n")
inicio_simulacion = time.time()

# Lanzar los hilos
with ThreadPool(len(nombres)) as pool:
    pool.map(usar_bus, nombres)

print("\n⏹️ Simulación finalizada.")
