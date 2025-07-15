import tkinter as tk
from tkinter import messagebox

# Función para convertir temperatura
def convertir():
    try:
        temp = float(entry.get())
        modo = conversion.get()

        if modo == "Celsius → Fahrenheit":
            resultado = (temp * 9/5) + 32
            resultado_var.set(f"{resultado:.2f} °F")
        elif modo == "Fahrenheit → Celsius":
            resultado = (temp - 32) * 5/9
            resultado_var.set(f"{resultado:.2f} °C")
        else:
            resultado_var.set("❌ Selecciona un modo válido.")
    except ValueError:
        resultado_var.set("⚠️ Ingresa un número válido.")

# Interfaz principal
root = tk.Tk()
root.title("Conversor de Temperatura")
root.geometry("400x350")
root.configure(bg="#2e2e2e")
root.resizable(False, False)

# Título
tk.Label(root, text="🌡️ Conversor de Temperatura", font=("Arial", 18, "bold"), bg="#2e2e2e", fg="white").pack(pady=20)

# Entrada
entry = tk.Entry(root, font=("Arial", 16), justify="center", width=10, bd=0, bg="#1e1e1e", fg="white")
entry.pack(pady=10)

# Modo de conversión
conversion = tk.StringVar()
conversion.set("Celsius → Fahrenheit")
opciones = ["Celsius → Fahrenheit", "Fahrenheit → Celsius"]
tk.OptionMenu(root, conversion, *opciones).pack(pady=10)

# Botón de conversión
tk.Button(root, text="Convertir", font=("Arial", 12), bg="#4caf50", fg="white",
          activebackground="#45a049", width=20, height=2, command=convertir).pack(pady=10)

# Resultado
resultado_var = tk.StringVar(value="Resultado aparecerá aquí")
tk.Label(root, textvariable=resultado_var, font=("Arial", 14), wraplength=350,
         bg="#2e2e2e", fg="#f5f5f5").pack(pady=20)

root.mainloop()
