import tkinter as tk
from tkinter import messagebox
import string
import random

def generar_contraseña():
    longitud = longitud_var.get()
    incluir_mayus = mayus_var.get()
    incluir_minus = minus_var.get()
    incluir_num = num_var.get()
    incluir_simbolos = simbolos_var.get()

    caracteres = ""
    if incluir_mayus:
        caracteres += string.ascii_uppercase
    if incluir_minus:
        caracteres += string.ascii_lowercase
    if incluir_num:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        messagebox.showwarning("Advertencia", "Selecciona al menos un tipo de carácter.")
        return

    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    resultado_var.set(contraseña)

def copiar_al_portapapeles():
    password = resultado_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles.")

# Ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas Seguras")
root.geometry("420x450")
root.config(bg="#2e2e2e")
root.resizable(False, False)

# Variables
longitud_var = tk.IntVar(value=12)
mayus_var = tk.BooleanVar(value=True)
minus_var = tk.BooleanVar(value=True)
num_var = tk.BooleanVar(value=True)
simbolos_var = tk.BooleanVar(value=True)
resultado_var = tk.StringVar()

# Título
tk.Label(root, text="Generador de Contraseñas", font=("Arial", 18, "bold"), fg="white", bg="#2e2e2e").pack(pady=15)

# Longitud
frame_long = tk.Frame(root, bg="#2e2e2e")
frame_long.pack(pady=10)
tk.Label(frame_long, text="Longitud:", font=("Arial", 12), fg="white", bg="#2e2e2e").pack(side="left")
tk.Scale(frame_long, from_=4, to=40, variable=longitud_var, orient="horizontal", length=200, bg="#2e2e2e",
         fg="white", troughcolor="#444", highlightthickness=0).pack(side="left")

# Opciones de caracteres
frame_opts = tk.Frame(root, bg="#2e2e2e")
frame_opts.pack(pady=10)

tk.Checkbutton(frame_opts, text="Mayúsculas (A-Z)", variable=mayus_var, font=("Arial", 11), bg="#2e2e2e", fg="white",
               activebackground="#2e2e2e", activeforeground="white", selectcolor="#2e2e2e").pack(anchor="w")
tk.Checkbutton(frame_opts, text="Minúsculas (a-z)", variable=minus_var, font=("Arial", 11), bg="#2e2e2e", fg="white",
               activebackground="#2e2e2e", activeforeground="white", selectcolor="#2e2e2e").pack(anchor="w")
tk.Checkbutton(frame_opts, text="Números (0-9)", variable=num_var, font=("Arial", 11), bg="#2e2e2e", fg="white",
               activebackground="#2e2e2e", activeforeground="white", selectcolor="#2e2e2e").pack(anchor="w")
tk.Checkbutton(frame_opts, text="Símbolos (!@#...)", variable=simbolos_var, font=("Arial", 11), bg="#2e2e2e", fg="white",
               activebackground="#2e2e2e", activeforeground="white", selectcolor="#2e2e2e").pack(anchor="w")

# Botón generar
tk.Button(root, text="Generar Contraseña", font=("Arial", 12), bg="#4caf50", fg="white",
          activebackground="#45a049", width=25, height=2, command=generar_contraseña).pack(pady=15)

# Resultado
tk.Entry(root, textvariable=resultado_var, font=("Arial", 14), justify="center", bg="#1e1e1e", fg="white", bd=0,
         relief="sunken", width=32).pack(pady=10)

# Botón copiar
tk.Button(root, text="Copiar al Portapapeles", font=("Arial", 11), bg="#2196f3", fg="white",
          activebackground="#1976d2", width=25, command=copiar_al_portapapeles).pack(pady=10)

root.mainloop()
