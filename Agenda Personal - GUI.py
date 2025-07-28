import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime
from plyer import notification

ARCHIVO = "agenda.json"

# ---------------- FUNCIONES ----------------
def cargar_eventos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_eventos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4)

def agregar_evento():
    titulo = titulo_var.get().strip()
    fecha = fecha_entry.get()
    hora = hora_var.get().strip()
    if titulo and hora:
        eventos.append({"titulo": titulo, "fecha": fecha, "hora": hora, "estado": "Pendiente"})
        guardar_eventos()
        actualizar_lista()
        titulo_var.set("")
        hora_var.set("")
    else:
        messagebox.showwarning("Faltan datos", "Completa título y hora.")

def actualizar_lista():
    lista.delete(0, tk.END)
    hoy = datetime.now().strftime("%Y-%m-%d")
    for i, e in enumerate(eventos):
        if e['fecha'] == hoy:
            estado = "✔" if e['estado'] == "Completado" else "✖"
            lista.insert(tk.END, f"[{estado}] {e['hora']} - {e['titulo']}")

def marcar_completado():
    idx = lista.curselection()
    if idx:
        hoy = datetime.now().strftime("%Y-%m-%d")
        visibles = [i for i, e in enumerate(eventos) if e['fecha'] == hoy]
        real_idx = visibles[idx[0]]
        eventos[real_idx]['estado'] = "Completado"
        guardar_eventos()
        actualizar_lista()

def notificar_eventos():
    hoy = datetime.now().strftime("%Y-%m-%d")
    ahora = datetime.now().strftime("%H:%M")
    for e in eventos:
        if e['fecha'] == hoy and e['hora'] == ahora and e['estado'] == "Pendiente":
            notification.notify(
                title="Recordatorio de evento",
                message=f"{e['titulo']} a las {e['hora']}",
                timeout=5
            )
    root.after(60000, notificar_eventos)  # revisa cada minuto

def cambiar_tema():
    global tema_actual
    tema_actual = "claro" if tema_actual == "oscuro" else "oscuro"
    aplicar_tema()

def aplicar_tema():
    tema = temas[tema_actual]
    root.config(bg=tema['bg'])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Listbox, tk.Entry)):
            widget.config(bg=tema['bg'], fg=tema['fg'])
    lista.config(bg=tema['entry_bg'], fg=tema['fg'])

# ---------------- INTERFAZ ----------------
root = tk.Tk()
root.title("🗓️ Agenda Diaria")
root.geometry("500x600")

tema_actual = "oscuro"
temas = {
    "oscuro": {"bg": "#2e2e2e", "fg": "white", "entry_bg": "#1e1e1e"},
    "claro": {"bg": "#ffffff", "fg": "black", "entry_bg": "#f5f5f5"}
}

# Campos
titulo_var = tk.StringVar()
hora_var = tk.StringVar()

fecha_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
fecha_entry.pack(pady=5)
tk.Entry(root, textvariable=titulo_var, font=("Arial", 12), width=30).pack(pady=5)
tk.Entry(root, textvariable=hora_var, font=("Arial", 12), width=15).pack(pady=5)
tk.Button(root, text="Agregar Evento", command=agregar_evento).pack(pady=5)
tk.Button(root, text="Marcar como Completado", command=marcar_completado).pack(pady=5)
tk.Button(root, text="🌗 Cambiar Tema", command=cambiar_tema).pack(pady=5)

# Lista eventos del día
tk.Label(root, text="Eventos de Hoy", font=("Arial", 14, "bold")).pack(pady=10)
lista = tk.Listbox(root, width=60, height=20, font=("Arial", 10))
lista.pack(pady=10)

# Cargar y ejecutar
eventos = cargar_eventos()
aplicar_tema()
actualizar_lista() 
notificar_eventos()
root.mainloop()
