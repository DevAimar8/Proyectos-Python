import tkinter as tk
import math

# Funciones matemáticas disponibles
funciones = {
    "√": lambda x: math.sqrt(x),
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": lambda x: math.log10(x),
    "ln": lambda x: math.log(x),
}

# Ventana principal
root = tk.Tk()
root.title("Calculadora Científica")
root.geometry("420x600")
root.configure(bg="#2e2e2e")

expresion = ""

def presionar(valor):
    global expresion
    expresion += str(valor)
    entrada_var.set(expresion)

def limpiar():
    global expresion
    expresion = ""
    entrada_var.set("")

def borrar():
    global expresion
    expresion = expresion[:-1]
    entrada_var.set(expresion)

def calcular():
    global expresion
    try:
        resultado = str(eval(expresion, {"__builtins__": None}, {**funciones, **math.__dict__}))
        entrada_var.set(resultado)
        expresion = resultado
    except Exception as e:
        entrada_var.set("Error")
        expresion = ""

# Pantalla de entrada
entrada_var = tk.StringVar()
entrada = tk.Entry(root, textvariable=entrada_var, font=("Arial", 22), bd=0, relief="flat", bg="#1e1e1e", fg="white", justify="right")
entrada.pack(pady=20, ipady=10, ipadx=8, fill="x", padx=15)

# Frame para botones
frame = tk.Frame(root, bg="#2e2e2e")
frame.pack()

# Diseño de botones
botones = [
    ["7", "8", "9", "/", "√"],
    ["4", "5", "6", "*", "log"],
    ["1", "2", "3", "-", "ln"],
    ["0", ".", "+", "(", ")"],
    ["sin", "cos", "tan", "pi", "e"],
    ["C", "←", "=", "**", "%"]
]

# Crear botones
for fila in botones:
    fila_frame = tk.Frame(frame, bg="#2e2e2e")
    fila_frame.pack(pady=4)
    for btn in fila:
        if btn == "=":
            cmd = calcular
        elif btn == "C":
            cmd = limpiar
        elif btn == "←":
            cmd = borrar
        elif btn == "pi":
            cmd = lambda v=math.pi: presionar(round(v, 10))
        elif btn == "e":
            cmd = lambda v=math.e: presionar(round(v, 10))
        elif btn in funciones:
            cmd = lambda f=btn: presionar(f + "(")
        else:
            cmd = lambda b=btn: presionar(b)

        tk.Button(fila_frame, text=btn, width=6, height=2, font=("Arial", 14), bg="#3c3f41", fg="white",
                  activebackground="#555", activeforeground="white", relief="flat", command=cmd).pack(side="left", padx=4)

root.mainloop()
