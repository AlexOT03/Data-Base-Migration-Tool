import tkinter as tk
from tkinter import ttk, messagebox
from util.Tooltip_util import Tooltip
from apps.databases import sqls_db, mysql_db

class MigrationConfirmationWindow(tk.Toplevel):
    def __init__(self, parent, database, tables, sqls_connect, mysql_connect, db_status, type):
        super().__init__(parent)
        self.parent = parent
        self.title("Confirmacion")
        self.iconbitmap("img/dark_icon.ico")
        self.resizable(False, False)
        
        self.title = tk.Label(self, text="Database migration confirmation", font=("Arial", 14))
        self.title.pack(padx=20, pady=10)

        self.label_confirmation = tk.Label(self, text="Please confirm the tables you want to migrate")
        self.label_confirmation.pack(padx=10, pady=10)

        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.pack(fill='x')

        self.label_comprovation = tk.Label(self, text=db_status)
        self.label_comprovation.pack(padx=30, pady=10)

        self.label_info = ttk.Label(self, text='ℹ️(hover me)')
        self.label_info.pack(padx=10, pady=10)

        self.tooltip = Tooltip(self.label_info, "Selecting the tables manually \n will prevent foreign keys \n from being migrated")
        
        self.label_frame = ttk.LabelFrame(self, text=f"Tables of database {database}:")
        self.label_frame.pack(padx=10, pady=10, fill='both')
        
        self.selected_tables = []
        self.table_var = tk.StringVar(value=tables)  # Lista de tablas disponibles
        self.tables_listbox = tk.Listbox(self.label_frame, listvariable=self.table_var, selectmode=tk.MULTIPLE)
        self.tables_listbox.pack(pady=5)
        
        self.select_all_var = tk.BooleanVar()
        self.select_all_checkbox = ttk.Checkbutton(self.label_frame, text="Seleccionar todas:", variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_checkbox.pack(pady=5)
        
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.pack(fill='x')

        self.button_confirm = ttk.Button(self, text="Confirm", command=self.confirm_migration)
        self.button_confirm.pack(side='right', padx=5, pady=5)
        
        self.button_cancel = ttk.Button(self, text="Cancel", command=self.destroy)
        self.button_cancel.pack(side='right', padx=5, pady=5)
        
        self.database = database
        self.sqls_connect = sqls_connect
        self.mysql_connect = mysql_connect
        self.type = type
    
    def toggle_select_all(self):
        if self.select_all_var.get():
            self.tables_listbox.select_set(0, tk.END)
        else:
            self.tables_listbox.selection_clear(0, tk.END)

    def confirm_migration(self):
        selected_tables_indices = self.tables_listbox.curselection()
        for index in selected_tables_indices:
            self.selected_tables.append(self.tables_listbox.get(index))
        
        print(self.selected_tables)
        if self.type == "SQLS":
            try:
                sqls_db.migrate_to_mysql_process(self.sqls_connect, self.mysql_connect, self.database, self.selected_tables)
                messagebox.showinfo("Completado", f"La migraccion de la base de datos {self.database} a MySQL fue exitosa.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrio un error durante la migracion de {self.database} a MySQL \n Code: {e}")
            
        elif self.type == "MySQL":
            try:
                mysql_db.migrate_to_sql_server_process(self.sqls_connect, self.mysql_connect, self.database, self.selected_tables)
                messagebox.showinfo("Completado", f"La migraccion de la base de datos {self.database} a SQL Server fue exitosa.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrio un error durante la migracion de {self.database} a SQL Server \n Code: {e}")
        
        self.destroy()