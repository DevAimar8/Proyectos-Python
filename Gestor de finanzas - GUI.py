import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import datetime

ARCHIVO = "finanzas.json"
categorias = ["Comida", "Transporte", "Ocio", "Salud", "Otros"]

# ---------------- FUNCIONES DE ARCHIVO ----------------
def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(finanzas, f, indent=4)

# ---------------- OPERACIONES ----------------
def agregar_movimiento():
    tipo = tipo_var.get()
    cat = categoria_var.get()
    monto = monto_var.get()
    try:
        valor = float(monto)
        fecha = datetime.now().strftime("%Y-%m-%d")
        finanzas.append({"tipo": tipo, "categoria": cat, "monto": valor, "fecha": fecha})
        guardar_datos()
        actualizar_lista()
        monto_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido.")

def calcular_saldo():
    ingresos = sum(item['monto'] for item in finanzas if item['tipo'] == "Ingreso")
    egresos = sum(item['monto'] for item in finanzas if item['tipo'] == "Egreso")
    return ingresos - egresos

def actualizar_lista():
    lista.delete(*lista.get_children())
    for i, item in enumerate(finanzas):
        lista.insert("", "end", values=(item['fecha'], item['tipo'], item['categoria'], f"${item['monto']:.2f}"))
    saldo = calcular_saldo()
    saldo_label.config(text=f"Saldo total: ${saldo:.2f}")

def mostrar_grafico():
    egresos_por_categoria = {}
    for item in finanzas:
        if item['tipo'] == "Egreso":
            cat = item['categoria']
            egresos_por_categoria[cat] = egresos_por_categoria.get(cat, 0) + item['monto']

    if not egresos_por_categoria:
        messagebox.showinfo("Sin datos", "No hay egresos para graficar.")
        return

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(egresos_por_categoria.values(), labels=egresos_por_categoria.keys(), autopct='%1.1f%%')
    ax.set_title("Distribución de egresos")

    grafico_ventana = tk.Toplevel(root)
    grafico_ventana.title("Gráfico de Egresos")
    canvas = FigureCanvasTkAgg(fig, master=grafico_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ---------------- INTERFAZ ----------------
root = tk.Tk()
root.title("💰 Gestor de Finanzas Personales")
root.geometry("750x600")
root.configure(bg="#2e2e2e")

# Formulario
frame_form = tk.Frame(root, bg="#2e2e2e")
frame_form.pack(pady=10)

tipo_var = tk.StringVar(value="Ingreso")
categoria_var = tk.StringVar(value="Comida")
monto_var = tk.StringVar()

tk.Label(frame_form, text="Tipo:", bg="#2e2e2e", fg="white").grid(row=0, column=0)
tk.OptionMenu(frame_form, tipo_var, "Ingreso", "Egreso").grid(row=0, column=1)

tk.Label(frame_form, text="Categoría:", bg="#2e2e2e", fg="white").grid(row=0, column=2)
tk.OptionMenu(frame_form, categoria_var, *categorias).grid(row=0, column=3)

tk.Label(frame_form, text="Monto:", bg="#2e2e2e", fg="white").grid(row=0, column=4)
tk.Entry(frame_form, textvariable=monto_var).grid(row=0, column=5)

tk.Button(root, text="➕ Agregar Movimiento", bg="#4caf50", fg="white", command=agregar_movimiento).pack(pady=10)

# Tabla
cols = ("Fecha", "Tipo", "Categoría", "Monto")
lista = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    lista.heading(col, text=col)
    lista.column(col, width=150)
lista.pack(pady=10, fill="both", expand=True)

# Saldo y gráfico
saldo_label = tk.Label(root, text="Saldo total: $0.00", font=("Arial", 14), bg="#2e2e2e", fg="white")
saldo_label.pack(pady=10)

tk.Button(root, text="📊 Mostrar Gráfico de Egresos", command=mostrar_grafico, bg="#2196f3", fg="white").pack()

# Iniciar
finanzas = cargar_datos()
actualizar_lista()
root.mainloop()
