import tkinter as tk
from tkinter import ttk
import time

def create_progress_bar(root, length=100):
    progress_bar = ttk.Progressbar(root, length=length)
    progress_bar.pack()
    return progress_bar

def start_progress_bar(progress_bar, delay=0.01):
    progress = 0
    while progress < 100:
        progress += 1
        progress_bar['value'] = progress
        root.update_idletasks()
        time.sleep(delay)

root = tk.Tk()

# Crear la primera barra de progreso para la operación A
progress_bar_A = create_progress_bar(root, length=200)
start_button_A = tk.Button(root, text='Start A', command=lambda: start_progress_bar(progress_bar_A))
start_button_A.pack()

# Crear la segunda barra de progreso para la operación B
progress_bar_B = create_progress_bar(root, length=200)
start_button_B = tk.Button(root, text='Start B', command=lambda: start_progress_bar(progress_bar_B))
start_button_B.pack()

root.mainloop()
