# interfaz.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class InterfazGrafica:
    def __init__(self, sensor):
        self.sensor = sensor
        self.paused = False

        self.root = tk.Tk()
        self.root.title("🌤️ Estación Meteorológica Profesional")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f0f2f5")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11), background="#f0f2f5")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # --- Frame superior: controles y resumen ---
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.label_estado = ttk.Label(top_frame, text="Esperando datos...")
        self.label_estado.pack(side="left", padx=10)

        self.btn_pausa = ttk.Button(top_frame, text="⏸ Pausar", command=self.toggle_pausa)
        self.btn_pausa.pack(side="right", padx=5)

        self.btn_guardar = ttk.Button(top_frame, text="💾 Guardar ahora", command=self.guardar_manual)
        self.btn_guardar.pack(side="right", padx=5)

        self.btn_limpiar = ttk.Button(top_frame, text="🧹 Limpiar tabla", command=self.limpiar_tabla)
        self.btn_limpiar.pack(side="right", padx=5)

        # --- Gráfica ---
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="x", padx=10, pady=10)

        # --- Tabla de datos ---
        tabla_frame = ttk.Frame(self.root)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(tabla_frame, columns=("hora", "temp", "hum", "pres"), show="headings", height=10)
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("temp", text="Temperatura (°C)")
        self.tabla.heading("hum", text="Humedad (%)")
        self.tabla.heading("pres", text="Presión (hPa)")

        self.tabla.column("hora", width=100, anchor="center")
        self.tabla.column("temp", width=120, anchor="center")
        self.tabla.column("hum", width=120, anchor="center")
        self.tabla.column("pres", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # --- Resumen estadístico ---
        resumen_frame = ttk.Frame(self.root)
        resumen_frame.pack(fill="x", padx=10, pady=5)

        self.label_resumen = ttk.Label(resumen_frame, text="Resumen estadístico:")
        self.label_resumen.pack(anchor="w", padx=10)

        self.label_stats = ttk.Label(resumen_frame, text="...")
        self.label_stats.pack(anchor="w", padx=20)

    def toggle_pausa(self):
        self.paused = not self.paused
        self.btn_pausa.config(text="▶ Reanudar" if self.paused else "⏸ Pausar")

    def guardar_manual(self):
        datos = self.sensor.obtener_datos()
        if datos:
            try:
                with open("datos/datos_climaticos_manual.csv", "w", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['fecha', 'hora', 'temperatura', 'humedad', 'presion'])
                    writer.writeheader()
                    for d in datos:
                        writer.writerow(d)
                messagebox.showinfo("Guardado", "Datos guardados correctamente en 'datos_climaticos_manual.csv'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")
        else:
            messagebox.showwarning("Sin datos", "No hay datos para guardar.")

    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def actualizar(self):
        if self.paused:
            self.root.after(1000, self.actualizar)
            return

        datos = self.sensor.obtener_datos()
        if not datos:
            self.root.after(1000, self.actualizar)
            return

        # === Gráfica ===
        tiempos = [d["hora"] for d in datos]
        temperaturas = [d["temperatura"] for d in datos]
        humedades = [d["humedad"] for d in datos]
        presiones = [d["presion"] for d in datos]

        self.ax.clear()
        self.ax.plot(tiempos, temperaturas, label="🌡️ Temp (°C)", color="#ff5e57", linewidth=2)
        self.ax.plot(tiempos, humedades, label="💧 Humedad (%)", color="#3498db", linewidth=2)
        self.ax.plot(tiempos, presiones, label="📈 Presión (hPa)", color="#2ecc71", linewidth=2)
        self.ax.set_title("Datos Climáticos en Tiempo Real")
        self.ax.set_xticklabels(tiempos, rotation=45, ha='right')
        self.ax.legend(loc="upper left")
        self.ax.grid(True)
        self.canvas.draw()

        # === Último dato ===
        ult = datos[-1]
        texto_estado = f"Última lectura: {ult['hora']} | Temp: {ult['temperatura']}°C | Humedad: {ult['humedad']}% | Presión: {ult['presion']} hPa"
        self.label_estado.config(text=texto_estado)

        # === Tabla de datos ===
        self.limpiar_tabla()
        for d in datos:
            self.tabla.insert("", "end", values=(d["hora"], d["temperatura"], d["humedad"], d["presion"]))

        # === Estadísticas ===
        temp_max = max(temperaturas)
        temp_min = min(temperaturas)
        hum_avg = round(sum(humedades) / len(humedades), 2)
        pres_ult = presiones[-1]

        self.label_stats.config(text=f"🌡️ Máx: {temp_max}°C | Mín: {temp_min}°C | 💧 Humedad Media: {hum_avg}% | 📈 Última Presión: {pres_ult} hPa")

        self.root.after(1000, self.actualizar)

    def iniciar(self):
        self.actualizar()
        self.root.mainloop()
