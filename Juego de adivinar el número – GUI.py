import tkinter as tk
import random

# Inicialización del número secreto
numero_secreto = random.randint(1, 100)
intentos = 0

# Función para verificar número
def verificar():
    global intentos
    try:
        intento = int(entry.get())
        intentos += 1
        if intento < numero_secreto:
            mensaje.set("📉 Muy bajo. Intenta de nuevo.")
        elif intento > numero_secreto:
            mensaje.set("📈 Muy alto. Intenta de nuevo.")
        else:
            mensaje.set(f"🎉 ¡Correcto! Lo adivinaste en {intentos} intentos.")
            entry.config(state="disabled")
            boton_verificar.config(state="disabled")
            boton_reiniciar.pack(pady=10)
    except ValueError:
        mensaje.set("❌ Por favor, ingresa un número válido.")

# Función para reiniciar el juego
def reiniciar():
    global numero_secreto, intentos
    numero_secreto = random.randint(1, 100)
    intentos = 0
    mensaje.set("Adivina un número del 1 al 100")
    entry.config(state="normal")
    boton_verificar.config(state="normal")
    entry.delete(0, tk.END)
    boton_reiniciar.pack_forget()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Juego: Adivina el Número")
root.geometry("400x350")
root.configure(bg="#2e2e2e")
root.resizable(False, False)

# Título
tk.Label(root, text="🎯 Adivina el Número", font=("Arial", 20, "bold"), bg="#2e2e2e", fg="white").pack(pady=20)

# Entrada
entry = tk.Entry(root, font=("Arial", 16), justify="center", width=10, bd=0, bg="#1e1e1e", fg="white")
entry.pack(pady=10)

# Botón verificar
boton_verificar = tk.Button(root, text="Verificar", font=("Arial", 12), bg="#4caf50", fg="white",
                            activebackground="#45a049", width=20, height=2, command=verificar)
boton_verificar.pack(pady=10)

# Mensaje dinámico
mensaje = tk.StringVar(value="🔢 Adivina un número del 1 al 100")
tk.Label(root, textvariable=mensaje, font=("Arial", 13), wraplength=350, bg="#2e2e2e", fg="white").pack(pady=10)

# Botón reiniciar (oculto al inicio)
boton_reiniciar = tk.Button(root, text="🔄 Reiniciar juego", font=("Arial", 11), bg="#2196f3", fg="white",
                            activebackground="#1976d2", command=reiniciar)

root.mainloop() 
