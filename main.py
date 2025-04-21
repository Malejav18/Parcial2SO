# main.py
import threading
from sensores import SensorClimatico
from almacenamiento import AlmacenadorCSV
from interfaz import InterfazGrafica

def main():
    sensor = SensorClimatico()
    almacenador = AlmacenadorCSV(sensor)
    interfaz = InterfazGrafica(sensor)

    t1 = threading.Thread(target=sensor.hilo_generador, daemon=True)
    t2 = threading.Thread(target=almacenador.hilo_guardado, daemon=True)

    t1.start()
    t2.start()
    interfaz.iniciar()


main()
