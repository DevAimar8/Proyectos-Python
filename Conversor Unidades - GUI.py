from tkinter import ttk, messagebox, filedialog
import csv

# ---------------- CONVERSIONES ----------------
conversiones = {
    "Longitud": {"m": 1, "cm": 100, "km": 0.001, "in": 39.3701, "ft": 3.28084},
    "Peso": {"kg": 1, "g": 1000, "lb": 2.20462, "oz": 35.274},
    "Temperatura": "especial",
    "Velocidad": {"m/s": 1, "km/h": 3.6, "mph": 2.23694},
    "Tiempo": {"s": 1, "min": 1/60, "h": 1/3600, "d": 1/86400}
}

historial = []
tema_actual = "oscuro"
temas = {
    "oscuro": {"bg": "#2e2e2e", "fg": "white"},
    "claro": {"bg": "#ffffff", "fg": "black"}
}

# ---------------- FUNCIONES ----------------
def convertir(tipo, valor, unidad_origen, unidad_destino):
    try:
        val = float(value_vars[tipo].get())
        if tipo == "Temperatura":
            resultado = convertir_temperatura(val, unidad_origen, unidad_destino)
        else:
            base = val / conversiones[tipo][unidad_origen]
            resultado = base * conversiones[tipo][unidad_destino]
        resultado_str = f"{resultado:.4f} {unidad_destino}"
        result_vars[tipo].set(resultado_str)
        historial.append((tipo, val, unidad_origen, resultado_str))
    except ValueError:
        messagebox.showerror("Error", "Introduce un valor numérico válido.")

def convertir_temperatura(valor, origen, destino):
    if origen == destino:
        return valor
    if origen == "C":
        temp_k = valor + 273.15
    elif origen == "F":
        temp_k = (valor - 32) * 5/9 + 273.15
    else:
        temp_k = valor

    if destino == "C":
        return temp_k - 273.15
    elif destino == "F":
        return (temp_k - 273.15) * 9/5 + 32
    else:
        return temp_k

def copiar_resultado(tipo):
    resultado = result_vars[tipo].get()
    if resultado:
        root.clipboard_clear()
        root.clipboard_append(resultado)
        messagebox.showinfo("Copiado", f"Resultado copiado: {resultado}")

def mostrar_historial():
    ventana = tk.Toplevel(root)
    ventana.title("Historial de Conversiones")
    ventana.geometry("400x300")
    ventana.configure(bg=temas[tema_actual]['bg'])
    lb = tk.Listbox(ventana, bg=temas[tema_actual]['bg'], fg=temas[tema_actual]['fg'])
    lb.pack(fill="both", expand=True)
    for item in historial:
        lb.insert(tk.END, f"{item[0]}: {item[1]} {item[2]} → {item[3]}")

def exportar_historial():
    if not historial:
        messagebox.showinfo("Vacío", "No hay historial para exportar.")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Texto", "*.txt")])
    if archivo:
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tipo", "Valor", "Desde", "Resultado"])
            for item in historial:
                writer.writerow(item)
        messagebox.showinfo("Exportado", f"Historial guardado en {archivo}")

def cambiar_tema():
    global tema_actual
    tema_actual = "claro" if tema_actual == "oscuro" else "oscuro"
    aplicar_tema()

def aplicar_tema():
    tema = temas[tema_actual]
    root.configure(bg=tema['bg'])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, tk.Label)):
            widget.configure(bg=tema['bg'], fg=tema['fg'])
    for frame in notebook.winfo_children():
        frame.configure(bg=tema['bg'])
        for w in frame.winfo_children():
            if isinstance(w, (tk.Label, tk.Entry, tk.Button, tk.Listbox)):
                w.configure(bg=tema['bg'], fg=tema['fg'])

# ---------------- INTERFAZ ----------------
root = tk.Tk()
root.title("🌐 Conversor Universal de Unidades")
root.geometry("520x600")

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", padding=6, font=("Arial", 10))
style.configure("TNotebook", background="#f5f5f5")

# Botones globales
tk.Button(root, text="🌗 Tema Claro/Oscuro", command=cambiar_tema).pack(pady=5)
tk.Button(root, text="🕘 Ver Historial", command=mostrar_historial).pack(pady=5)
tk.Button(root, text="📄 Exportar Historial", command=exportar_historial).pack(pady=5)

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

value_vars = {}
result_vars = {}

for tipo in conversiones:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tipo)

    value_vars[tipo] = tk.StringVar()
    result_vars[tipo] = tk.StringVar()

    unidades = ["C", "F", "K"] if tipo == "Temperatura" else list(conversiones[tipo].keys())

    tk.Label(frame, text="Cantidad a convertir:").pack(pady=5)
    tk.Entry(frame, textvariable=value_vars[tipo]).pack(pady=5)

    origen_var = tk.StringVar(value=unidades[0])
    destino_var = tk.StringVar(value=unidades[1])

    tk.Label(frame, text="Desde:").pack()
    ttk.OptionMenu(frame, origen_var, unidades[0], *unidades).pack(pady=2)
    tk.Label(frame, text="Hacia:").pack()
    ttk.OptionMenu(frame, destino_var, unidades[1], *unidades).pack(pady=2)

    tk.Button(frame, text="Convertir", command=lambda t=tipo, o=origen_var, d=destino_var: convertir(t, value_vars[t].get(), o.get(), d.get())).pack(pady=5)
    tk.Label(frame, textvariable=result_vars[tipo], font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(frame, text="📋 Copiar resultado", command=lambda t=tipo: copiar_resultado(t)).pack()

aplicar_tema()
root.mainloop()
