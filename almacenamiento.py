import csv
import os
import time

class AlmacenadorCSV:
    def __init__(self, sensor, archivo='datos/datos_climaticos.csv'):
        self.sensor = sensor
        self.archivo = archivo
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        self.campos = ['fecha', 'hora', 'temperatura', 'humedad', 'presion']
        self.inicializar_archivo()

    def inicializar_archivo(self):
        with open(self.archivo, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.campos)
            writer.writeheader()

    def hilo_guardado(self):
        while True:
            time.sleep(5)
            datos = self.sensor.obtener_datos()[-5:]
            if datos:
                with open(self.archivo, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.campos)
                    for d in datos:
                        writer.writerow(d)
