import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria")
        self.root.geometry("600x600")
        self.root.configure(bg="#2e2e2e")

        self.cartas = list("AABBCCDDEEFFGGHH")
        random.shuffle(self.cartas)

        self.botones = []
        self.primera = None
        self.segunda = None
        self.bloqueado = False
        self.pares_encontrados = 0

        self.tablero = tk.Frame(self.root, bg="#2e2e2e")
        self.tablero.pack(pady=20)
        self.crear_tablero()

        self.estado = tk.Label(self.root, text="Encuentra todos los pares", bg="#2e2e2e", fg="white", font=("Arial", 14))
        self.estado.pack(pady=10)

    def crear_tablero(self):
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                btn = tk.Button(self.tablero, text="", width=8, height=4, font=("Arial", 18, "bold"),
                                command=lambda idx=idx: self.revelar(idx), bg="#455a64", fg="white")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.botones.append(btn)

    def revelar(self, idx):
        if self.bloqueado or self.botones[idx]['text'] != "":
            return

        self.botones[idx]['text'] = self.cartas[idx]
        self.botones[idx].config(bg="#66bb6a")

        if not self.primera:
            self.primera = idx
        elif not self.segunda and idx != self.primera:
            self.segunda = idx
            self.bloqueado = True
            self.root.after(800, self.verificar_pareja)

    def verificar_pareja(self):
        i, j = self.primera, self.segunda
        if self.cartas[i] == self.cartas[j]:
            self.botones[i].config(bg="#388e3c")
            self.botones[j].config(bg="#388e3c")
            self.pares_encontrados += 1
            if self.pares_encontrados == 8:
                self.estado.config(text="¡Ganaste! Has encontrado todos los pares")
        else:
            self.botones[i].config(text="", bg="#455a64")
            self.botones[j].config(text="", bg="#455a64")

        self.primera = None
        self.segunda = None
        self.bloqueado = False

if __name__ == "__main__":
    root = tk.Tk()
    juego = MemoryGame(root)
    root.mainloop()
