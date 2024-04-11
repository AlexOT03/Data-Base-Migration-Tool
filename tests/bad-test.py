import tkinter as tk
from tkinter import ttk
import time

# Suponiendo que aquí están tus funciones existentes

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title("Progress of Migration")

        self.title_label1 = tk.Label(self, text="Passing data to tables")
        self.title_label1.pack(padx=10, pady=10, anchor='w')
        self.bar1 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar1.pack(padx=10, pady=(0, 20))

        self.title_label2 = tk.Label(self, text="Creating foreignkeys")
        self.title_label2.pack(padx=10, pady=10, anchor='w')
        self.bar2 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar2.pack(padx=10, pady=(0, 20))


def migrate_db_with_progress(sqls_conn, mysql_conn, database, tables, progress_window):
    total_tasks = len(tables) + 1  # Sumamos 1 para la tarea de agregar claves foráneas
    progress_per_task = 100 / total_tasks
    progress = 0

    try:
        #migrate_db_to_mysql(sqls_conn, mysql_conn, database, tables)
        progress_window.bar1['value'] = progress + progress_per_task
        progress_window.update_idletasks()
        progress += progress_per_task

        #add_foreign_keys(sqls_conn, mysql_conn, database)
        progress_window.bar2['value'] = progress + progress_per_task
        progress_window.update_idletasks()
        progress += progress_per_task

    except Exception as e:
        print(f"Ocurrió un error: {e}")


def create_progress_window(root):
    progress_window = ProgressWindow(root)
    return progress_window


def start_migration(progress_window):
    # Aquí podrías tener tus conexiones y otros parámetros necesarios
    sqls_conn = None
    mysql_conn = None
    database = "tu_base_de_datos"
    tables = None  # Aquí deberías tener la lista de tablas que quieres migrar
    migrate_db_with_progress(sqls_conn, mysql_conn, database, tables, progress_window)


root = tk.Tk()

# Crear la ventana de progreso
progress_window = create_progress_window(root)

# Crear el botón para iniciar la migración
start_button = tk.Button(root, text='Iniciar Migración', command=lambda: start_migration(progress_window))
start_button.pack()

root.mainloop()