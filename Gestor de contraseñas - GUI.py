import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ARCHIVO = "contrasenas.json"

# ---------------- Seguridad ----------------
def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

def agregar():
    sitio = sitio_var.get().strip()
    usuario = usuario_var.get().strip()
    contrasena = contrasena_var.get().strip()
    if sitio and usuario and contrasena:
        datos.append({"sitio": sitio, "usuario": usuario, "contrasena": contrasena})
        guardar_datos()
        actualizar_tabla()
        limpiar_campos()
    else:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos.")

def limpiar_campos():
    sitio_var.set("")
    usuario_var.set("")
    contrasena_var.set("")

def eliminar():
    seleccionado = tree.selection()
    if seleccionado:
        idx = int(tree.item(seleccionado)['tags'][0])
        datos.pop(idx)
        guardar_datos()
        actualizar_tabla()

def copiar_contrasena():
    seleccionado = tree.selection()
    if seleccionado:
        idx = int(tree.item(seleccionado)['tags'][0])
        root.clipboard_clear()
        root.clipboard_append(datos[idx]['contrasena'])
        messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles.")

def buscar(event=None):
    filtro = entrada_busqueda.get().lower()
    tree.delete(*tree.get_children())
    for idx, item in enumerate(datos):
        if filtro in item['sitio'].lower():
            tree.insert("", "end", values=(item['sitio'], item['usuario'], "******"), tags=(str(idx),))

def actualizar_tabla():
    tree.delete(*tree.get_children())
    for idx, item in enumerate(datos):
        tree.insert("", "end", values=(item['sitio'], item['usuario'], "******"), tags=(str(idx),))

# ---------------- Interfaz ----------------
root = tk.Tk()
root.title("Gestor de Contraseñas Avanzado")
root.geometry("600x500")
root.configure(bg="#2e2e2e")

# Entrada de datos
sitio_var = tk.StringVar()
usuario_var = tk.StringVar()
contrasena_var = tk.StringVar()

tk.Label(root, text="Sitio", bg="#2e2e2e", fg="white").pack()
tk.Entry(root, textvariable=sitio_var, font=("Arial", 12)).pack(pady=2)

tk.Label(root, text="Usuario", bg="#2e2e2e", fg="white").pack()
tk.Entry(root, textvariable=usuario_var, font=("Arial", 12)).pack(pady=2)

tk.Label(root, text="Contraseña", bg="#2e2e2e", fg="white").pack()
tk.Entry(root, textvariable=contrasena_var, font=("Arial", 12), show="*").pack(pady=2)

tk.Button(root, text="Agregar", command=agregar, bg="#4caf50", fg="white").pack(pady=5)

# Búsqueda
entrada_busqueda = tk.Entry(root, font=("Arial", 12))
entrada_busqueda.pack(pady=5)
entrada_busqueda.bind("<KeyRelease>", buscar)

# Tabla de contraseñas
tree = ttk.Treeview(root, columns=("Sitio", "Usuario", "Contraseña"), show='headings')
tree.heading("Sitio", text="Sitio")
tree.heading("Usuario", text="Usuario")
tree.heading("Contraseña", text="Contraseña")
tree.pack(pady=10, fill="both", expand=True)

# Botones de acción
frame = tk.Frame(root, bg="#2e2e2e")
frame.pack(pady=5)
tk.Button(frame, text="🗑 Eliminar", command=eliminar, bg="#f44336", fg="white").pack(side="left", padx=5)
tk.Button(frame, text="📋 Copiar Contraseña", command=copiar_contrasena, bg="#2196f3", fg="white").pack(side="left", padx=5)

# Inicialización
datos = cargar_datos()
actualizar_tabla()
root.mainloop()
