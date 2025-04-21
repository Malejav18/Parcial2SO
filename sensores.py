import random
import threading
import time
from datetime import datetime, timedelta
import math

class SensorClimatico:
    def __init__(self):
        self.datos = []
        self.lock = threading.Lock()
        self.hora_actual = datetime.now()

        # Variables base
        self.temperatura_base = 20.0
        self.humedad_base = 60.0
        self.presion_base = 1013.0

    def calcular_dato(self):
        # Simula el paso del tiempo
        self.hora_actual += timedelta(seconds=1)
        hora = self.hora_actual.hour + self.hora_actual.minute / 60.0

        # Ciclo día-noche (temperatura sube de 6 a 14h y baja luego)
        ciclo_diario = math.sin((hora - 6) * math.pi / 12)
        temperatura = self.temperatura_base + ciclo_diario * 7 + random.uniform(-1.5, 1.5)

        # Humedad inversamente proporcional a temperatura + random suave
        humedad = self.humedad_base - ciclo_diario * 10 + random.uniform(-3, 3)

        # Presión atmosférica con oscilaciones lentas
        presion = self.presion_base + math.sin(hora / 6) * 3 + random.uniform(-0.5, 0.5)

        return {
            'fecha': self.hora_actual.strftime("%Y-%m-%d"),
            'hora': self.hora_actual.strftime("%H:%M:%S"),
            'temperatura': round(temperatura, 2),
            'humedad': round(humedad, 2),
            'presion': round(presion, 2)
        }

    def hilo_generador(self):
        while True:
            dato = self.calcular_dato()
            with self.lock:
                self.datos.append(dato)
                if len(self.datos) > 100:
                    self.datos = self.datos[-100:]
            time.sleep(1)

    def obtener_datos(self):
        with self.lock:
            return self.datos[-20:]
