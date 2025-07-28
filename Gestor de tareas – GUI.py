import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from plyer import notification
import json
import os
from datetime import datetime

ARCHIVO_TAREAS = "tareas.json"

# ---------------- DATOS ----------------
tareas = []
tema_actual = "oscuro"

temas = {
    "oscuro": {
        "bg": "#2e2e2e",
        "fg": "white",
        "entry_bg": "#1e1e1e",
        "button_bg": "#4caf50",
        "alt_button_bg": "#424242",
        "highlight": "#66bb6a"
    },
    "claro": {
        "bg": "#f0f0f0",
        "fg": "black",
        "entry_bg": "#ffffff",
        "button_bg": "#1976d2",
        "alt_button_bg": "#dddddd",
        "highlight": "#2196f3"
    }
}

# ---------------- FUNCIONES ----------------
def notificar():
    pendientes = [t for t in tareas if t['estado'] == 'Pendiente']
    if pendientes:
        notification.notify(
            title="Tareas pendientes",
            message=f"Tienes {len(pendientes)} tarea(s) por realizar.",
            timeout=5
        )

def guardar_tareas():
    with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=4)

def cargar_tareas():
    if os.path.exists(ARCHIVO_TAREAS):
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            tareas.extend(datos)

def agregar_tarea():
    texto = entrada.get().strip()
    tiempo = tiempo_var.get()
    importancia = importancia_var.get()
    if texto:
        tareas.append({
            "texto": texto,
            "estado": "Pendiente",
            "tiempo": tiempo,
            "importancia": importancia
        })
        entrada.delete(0, tk.END)
        actualizar_tablero()
        guardar_tareas()
    else:
        messagebox.showwarning("Campo vacío", "Escribe una tarea.")

def marcar_completada(tree):
    item = tree.focus()
    if item:
        idx = int(tree.item(item)['tags'][0])
        tareas[idx]['estado'] = 'Realizada'
        actualizar_tablero()
        guardar_tareas()

def eliminar_tarea(tree):
    item = tree.focus()
    if item:
        idx = int(tree.item(item)['tags'][0])
        tareas.pop(idx)
        actualizar_tablero()
        guardar_tareas()

def actualizar_tablero():
    for i in tree_pendientes.get_children():
        tree_pendientes.delete(i)
    for i in tree_realizadas.get_children():
        tree_realizadas.delete(i)

    for idx, t in enumerate(tareas):
        data = (t['texto'], t['tiempo'], t['importancia'])
        if t['estado'] == 'Pendiente':
            tree_pendientes.insert("", "end", values=data, tags=(str(idx),))
        else:
            tree_realizadas.insert("", "end", values=data, tags=(str(idx),))

def actualizar_estado():
    pendientes = sum(1 for t in tareas if t['estado'] == 'Pendiente')
    realizadas = sum(1 for t in tareas if t['estado'] == 'Realizada')
    estado.config(text=f"Pendientes: {pendientes} | Realizadas: {realizadas}")
    root.after(1000, actualizar_estado)

def cambiar_tema():
    global tema_actual
    tema_actual = "claro" if tema_actual == "oscuro" else "oscuro"
    aplicar_tema()

def aplicar_tema():
    tema = temas[tema_actual]
    root.config(bg=tema['bg'])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry)):
            widget.config(bg=tema['bg'], fg=tema['fg'])
        elif isinstance(widget, tk.Button):
            widget.config(bg=tema['button_bg'], fg='white', activebackground=tema['highlight'])
    entrada.config(bg=tema['entry_bg'], fg=tema['fg'])
    tree_pendientes.tag_configure('even', background=tema['entry_bg'])
    tree_realizadas.tag_configure('even', background=tema['entry_bg'])

# ---------------- INTERFAZ ----------------
root = tk.Tk()
root.title("Kanban Gestor de Tareas")
root.geometry("1080x700")

# Entrada tarea
entrada = tk.Entry(root, font=("Arial", 14), width=40)
entrada.grid(row=0, column=0, padx=10, pady=10)

tiempo_var = tk.StringVar(value="Indefinido")
tk.OptionMenu(root, tiempo_var, "Indefinido", "5 min", "10 min", "30 min", "1 hora", "2 horas").grid(row=0, column=1)

importancia_var = tk.StringVar(value="Media")
tk.OptionMenu(root, importancia_var, "Alta", "Media", "Baja").grid(row=0, column=2)

btn_add = tk.Button(root, text="Agregar Tarea", command=agregar_tarea, font=("Arial", 12))
btn_add.grid(row=0, column=3, padx=10)

btn_tema = tk.Button(root, text="Cambiar Tema", command=cambiar_tema, font=("Arial", 12))
btn_tema.grid(row=0, column=4, padx=10)

# Tablero Kanban
tk.Label(root, text="Pendientes", font=("Arial", 14, "bold")).grid(row=1, column=0, columnspan=2)
tk.Label(root, text="Realizadas", font=("Arial", 14, "bold")).grid(row=1, column=2, columnspan=2)

cols = ("Tarea", "Tiempo", "Importancia")
tree_pendientes = ttk.Treeview(root, columns=cols, show='headings', height=20)
for c in cols:
    tree_pendientes.heading(c, text=c)
tree_pendientes.grid(row=2, column=0, columnspan=2, padx=10)

btn_done = tk.Button(root, text="Marcar como Realizada", command=lambda: marcar_completada(tree_pendientes))
btn_done.grid(row=3, column=0, pady=5)

btn_del = tk.Button(root, text="Eliminar", command=lambda: eliminar_tarea(tree_pendientes))
btn_del.grid(row=3, column=1, pady=5)

tree_realizadas = ttk.Treeview(root, columns=cols, show='headings', height=20)
for c in cols:
    tree_realizadas.heading(c, text=c)
tree_realizadas.grid(row=2, column=2, columnspan=2, padx=10)

btn_del2 = tk.Button(root, text="🗑 Eliminar", command=lambda: eliminar_tarea(tree_realizadas))
btn_del2.grid(row=3, column=2, pady=5)

# Estado
tk.Label(root, text="", font=("Arial", 12)).grid(row=4, column=0, columnspan=4, pady=5)
estado = tk.Label(root, text="", font=("Arial", 12))
estado.grid(row=5, column=0, columnspan=4, pady=10)

# Inicio
cargar_tareas()
aplicar_tema()
actualizar_tablero()
actualizar_estado()
notificar()
root.mainloop()
