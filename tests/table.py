import tkinter as tk
from tkinter import ttk
import datetime

# Datos de la variable result
result = [
    (1, 1, datetime.datetime(2011, 1, 17, 0, 0)),
    (2, 1, datetime.datetime(2012, 6, 27, 0, 0)),
    # ... (otros datos)
    (11, 2, datetime.datetime(2011, 9, 3, 0, 0))
]

# Crear una ventana
root = tk.Tk()
root.title("Tabla de Datos")

# Crear una tabla
table = ttk.Treeview(root, columns=("ID", "Valor 1", "Fecha"))
table.heading("#1", text="ID")
table.heading("#2", text="Valor 1")
table.heading("#3", text="Fecha")

# Insertar datos en la tabla
for row in result:
    table.insert("", "end", values=row)

# Ajustar el ancho de las columnas
for col in ("ID", "Valor 1", "Fecha"):
    table.column(col)

# Mostrar la tabla
table.pack()

# Ejecutar la aplicación
root.mainloop()
