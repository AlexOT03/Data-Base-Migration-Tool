import tkinter as tk
from tkinter import ttk, messagebox
from multiprocessing import Process, cpu_count
import asyncio
from layout.base.Config_base import config_window
from apps.connections import sqls_conn, mysql_conn
from apps.databases import sqls_db, mysql_db
from layout.Migration_layout import MigrationConfirmationWindow

class MainLayout(tk.Tk):
    def __init__(self):
        super().__init__()
        config_window(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sqls_connect = None
        self.mysql_connect = None

        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill='both')

        self.title_label = tk.Label(self.master_frame, text="Welcome to DataWise Migrator Tool!", font=("Arial", 14))
        self.title_label.pack(padx=30, pady=15)
        self.subtitle_label = tk.Label(self.master_frame, text="Before starting, you must first connect to the database")
        self.subtitle_label.pack(padx=10, pady=5, anchor='nw')
        self.separator = ttk.Separator(self.master_frame, orient='horizontal')
        self.separator.pack(fill='x')

        # SQL Server connection form
        self.sqls_label = ttk.LabelFrame(self.master_frame, text="SQL Server")
        self.sqls_label.pack(padx=10, pady=(20, 10))

        self.driver_var = tk.StringVar(value="{SQL Server}")

        self.driver_menu_button = ttk.Menubutton(self.sqls_label, text="Select Driver")
        self.driver_menu_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='EW')
        self.driver_menu_button.menu = tk.Menu(self.driver_menu_button, tearoff=0)
        self.driver_menu_button["menu"] = self.driver_menu_button.menu

        for driver in ["{SQL Server}", "{ODBC Driver 17 for SQL Server}"]:
            self.driver_menu_button.menu.add_radiobutton(label=driver, variable=self.driver_var, value=driver)
        
        self.label_server = tk.Label(self.sqls_label, text="Server:")
        self.label_server.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_server = ttk.Entry(self.sqls_label)
        self.entry_server.grid(row=2, column=1, padx=10, pady=5)
        
        self.auth_var = tk.StringVar()
        self.checkbox_windows_auth = ttk.Checkbutton(self.sqls_label, text="Windows Auth?", variable=self.auth_var, onvalue="1", offvalue="0", command=self.win_auth)
        self.checkbox_windows_auth.grid(row=3, column=1, padx=10, pady=5)
        
        self.label_user = tk.Label(self.sqls_label, text="User:")
        self.label_user.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_user = ttk.Entry(self.sqls_label)
        self.entry_user.grid(row=4, column=1, padx=10, pady=5)
        
        self.label_password = tk.Label(self.sqls_label, text="Password:")
        self.label_password.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entry_password = ttk.Entry(self.sqls_label, show="*")
        self.entry_password.grid(row=5, column=1, padx=10, pady=5)

        # MySQL connection form
        self.mysql_label = ttk.LabelFrame(self.master_frame, text="MySQL")
        self.mysql_label.pack(padx=10, pady=(10, 20))

        self.label_host = tk.Label(self.mysql_label, text="Host:")
        self.label_host.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.entry_host = ttk.Entry(self.mysql_label)
        self.entry_host.grid(row=1, column=3, padx=10, pady=5)
        
        self.label_mysql_user = tk.Label(self.mysql_label, text="User:")
        self.label_mysql_user.grid(row=2, column=2, sticky="w", padx=10, pady=5)
        self.entry_mysql_user = ttk.Entry(self.mysql_label)
        self.entry_mysql_user.grid(row=2, column=3, padx=10, pady=5)
        
        self.label_mysql_password = tk.Label(self.mysql_label, text="Password:")
        self.label_mysql_password.grid(row=3, column=2, sticky="w", padx=10, pady=5)
        self.entry_mysql_password = ttk.Entry(self.mysql_label, show="*")
        self.entry_mysql_password.grid(row=3, column=3, padx=10, pady=5)

        self.separator = ttk.Separator(self.master_frame, orient='horizontal')
        self.separator.pack(anchor='s', fill='x')

        self.exit_btn = ttk.Button(self.master_frame, text="Connect", command=self.connect_servers)
        self.exit_btn.pack(anchor='se', side='right', padx=5, pady=5)  # Alinea a la derecha

        self.conn_btn = ttk.Button(self.master_frame, text="Exit", command=self.on_closing)
        self.conn_btn.pack(anchor='se', side='right', padx=5, pady=5)  # Alinea a la derecha


    def win_auth(self):
        if self.auth_var.get() == "1":
            self.entry_user.config(state="disabled")
            self.entry_password.config(state="disabled")
        else:
            self.entry_user.config(state="normal")
            self.entry_password.config(state="normal")


    def connect_servers(self):
        try:
            self.sqls_connect = sqls_conn.connect_sqls(self.driver_var.get(), 
                                                       self.entry_server.get(), 
                                                       self.auth_var.get(), 
                                                       self.entry_user.get(), 
                                                       self.entry_password.get())
            self.mysql_connect = mysql_conn.connect_mysql(self.entry_host.get(), 
                                                          self.entry_mysql_user.get(), 
                                                          self.entry_mysql_password.get())
        except Exception as e:
            messagebox.showerror("Error", f"Error {e}")

        if all([self.sqls_connect, self.mysql_connect]):
            self.show_databases_console()
        else:
            sqls_conn.close_sqls_conn(self.sqls_connect)
            mysql_conn.close_mysql_conn(self.mysql_connect)
            messagebox.showwarning("Warning", "You need all connections")
    

    def show_databases_console(self):
        self.master_frame.destroy()
        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill='both')

        self.title_label = tk.Label(self.master_frame, text="Welcome to DataWise Migrator Tool!", font=("Arial", 14))
        self.title_label.pack(pady=15)
        self.subtitle_label = tk.Label(self.master_frame, text="Select an option to get started")
        self.subtitle_label.pack(padx=10, pady=5, anchor='nw')
        self.separator = ttk.Separator(self.master_frame, orient='horizontal')
        self.separator.pack(fill='x')

        self.notebook = ttk.Notebook(self.master_frame)
        self.notebook.pack(padx=10, pady=10, expand=True)
        self.separator = ttk.Separator(self.master_frame, orient='horizontal')
        self.separator.pack(fill='x')

        self.btn_close = ttk.Button(self.master_frame, text="Exit", command=self.on_closing)
        self.btn_close.pack(padx=10, pady=10, anchor='s', side='right')

        self.frame1 = ttk.Frame(self.notebook)
        self.frame1.pack(fill='both', expand=True)
        self.notebook.add(self.frame1, text='General Options')

        self.frame2 = ttk.Frame(self.notebook)
        self.frame2.pack(fill='both', expand=True)
        self.notebook.add(self.frame2, text='Migrate DB')

        self.dbs_frame = tk.Frame(self.frame1)
        self.dbs_frame.pack()

        self.sqls_label = ttk.LabelFrame(self.dbs_frame, text="SQL Server")
        self.sqls_label.grid(row=2, column=0, padx=(10, 0), pady=10)
        self.tree_sql = ttk.Treeview(self.sqls_label, height=5)
        self.tree_sql.heading("#0", text="Databases", anchor=tk.W)
        self.tree_sql.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.mysql_label = ttk.LabelFrame(self.dbs_frame, text="MySQL")
        self.mysql_label.grid(row=2, column=1, padx=10, pady=10)
        self.tree_mysql = ttk.Treeview(self.mysql_label,  height=5)
        self.tree_mysql.heading("#0", text="Databases", anchor=tk.W)
        self.tree_mysql.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.select_sql_dbs(self.sqls_connect)
        self.select_mysql_dbs(self.mysql_connect)

        self.dbs_var = tk.StringVar(value="SQL Server")
        self.dbs = ["SQL Server", "MySQL"]
        self.server_dbs = tk.OptionMenu(self.frame1, self.dbs_var, *self.dbs)
        self.server_dbs.pack(padx=10, pady=10)

        self.run_btn = ttk.Button(self.frame1, text="Run", command=self.run_query)
        self.run_btn.pack(padx=10, pady=10)

        self.int_console = tk.Text(self.frame1, height=3)
        self.int_console.pack(padx=10, pady=10, fill='both', expand=True)

        self.colums = tk.Variable()
        self.out_table = ttk.Treeview(self.frame1, height=4, show='headings')
        self.out_table.pack(padx=10, pady=10, fill='both', expand=True)

        self.notebook2 = ttk.Notebook(self.frame2)
        self.notebook2.pack(padx=10, pady=10, fill='both', expand=True)

        self.subframe1 = ttk.Frame(self.notebook2)
        self.subframe1.pack(fill='both', expand=True)
        self.notebook2.add(self.subframe1, text='SQL Server to MySQl')

        self.subframe2 = ttk.Frame(self.notebook2)
        self.subframe2.pack(fill='both', expand=True)
        self.notebook2.add(self.subframe2, text='MySQL to SQL Server')

        # sql server migration part -------------------------------------------------------------------------------
        self.label1 = tk.Label(self.subframe1, text="Select the database you want to migrate to MySQL")
        self.label1.pack(padx=10, pady=(20, 0))

        self.dbsSqls = sqls_conn.get_sqls_dbs(self.sqls_connect)
        self.dbs1_var = tk.StringVar(value=self.dbsSqls[0])
        self.dbs = self.dbsSqls
        self.db_sqls = tk.OptionMenu(self.subframe1, self.dbs1_var, *self.dbs)
        self.db_sqls.pack(padx=10, pady=10)

        self.label1 = tk.Label(self.subframe1, text="Select the destination database")
        self.label1.pack(padx=10, pady=(30, 0))

        self.label1 = tk.Label(self.subframe1, text="If it does not exist, write the name and it will be created automatically (it must be the same)")
        self.label1.pack(padx=10, pady=10)

        self.dbsMysql = mysql_conn.get_mysql_dbs(self.mysql_connect)
        self.selected1_db = tk.StringVar(value=self.dbsMysql[0])
        self.database_spinner = ttk.Combobox(self.subframe1, values=self.dbsMysql, textvariable=self.selected1_db)
        self.database_spinner.pack(padx=10, pady=10)

        self.button_next_sql = ttk.Button(self.subframe1, text="Next", command=self.next_sqls_step)
        self.button_next_sql.pack(pady=10)

        # mysql migration part -------------------------------------------------------------------------------
        self.label1 = tk.Label(self.subframe2, text="Select the database you want to migrate to SQL Server")
        self.label1.pack(padx=10, pady=(20, 0))

        self.dbsMysql2 = mysql_conn.get_mysql_dbs(self.mysql_connect)
        self.dbs2_var = tk.StringVar(value=self.dbsMysql2[0])
        self.dbs2 = self.dbsMysql2
        self.db_mysql = tk.OptionMenu(self.subframe2, self.dbs2_var, *self.dbs2)
        self.db_mysql.pack(padx=10, pady=10)

        self.label1 = tk.Label(self.subframe2, text="Select the destination database")
        self.label1.pack(padx=10, pady=(30, 0))

        self.label1 = tk.Label(self.subframe2, text="If it does not exist, write the name and it will be created automatically (it must be the same)")
        self.label1.pack(padx=10, pady=10)

        self.dbsSqls2 = sqls_conn.get_sqls_dbs(self.sqls_connect)
        self.selected2_db = tk.StringVar(value=self.dbsSqls2[0])
        self.database_spinner = ttk.Combobox(self.subframe2, values=self.dbsSqls2, textvariable=self.selected2_db)
        self.database_spinner.pack(padx=10, pady=10)

        self.button_next_sql = ttk.Button(self.subframe2, text="Next", command=self.next_mysql_step)
        self.button_next_sql.pack(pady=10)
    

    def next_sqls_step(self):
        exp_database = self.dbs1_var.get()
        inp_database = self.selected1_db.get()

        if exp_database == inp_database:
            db_mysql_status = mysql_conn.check_mysql_db_exist(self.mysql_connect, inp_database)
            if not db_mysql_status:
                mysql_conn.create_mysql_db(self.mysql_connect, inp_database)
                db_status = f"The database {inp_database} does not exist on MySQL, we proceeded with its creation to continue with the operation"
            else:
                db_status = f"The database {inp_database} exists on MySQL, the operation will proceed"
            print("YES")
            tables = sqls_db.get_sql_server_tables(self.sqls_connect, exp_database)
            MigrationConfirmationWindow(self, inp_database, tables, self.sqls_connect, self.mysql_connect, db_status, "SQLS")
        else:
            messagebox.showwarning("warning", "The database name isnt same!")
    

    def next_mysql_step(self):
        exp_database = self.dbs2_var.get()
        inp_database = self.selected2_db.get()

        if exp_database == inp_database:
            db_sqls_status = sqls_conn.check_sqls_db_exist(self.sqls_connect, inp_database)
            if not db_sqls_status:
                sqls_conn.create_sqls_db(self.sqls_connect, inp_database)
                db_status = f"The database {inp_database} does not exist on SQL Server, we proceeded with its creation to continue with the operation"
            else:
                db_status = f"The database {inp_database} exists on SQL server, the operation will proceed"
            print("YES")
            tables = mysql_db.get_mysql_tables(self.mysql_connect, exp_database)
            MigrationConfirmationWindow(self, inp_database, tables, self.sqls_connect, self.mysql_connect, db_status, "MySQL")
        else:
            messagebox.showwarning("warning", "The database name isnt same!")
        

    def clear_table(self):
        for child in self.out_table.get_children():
            self.out_table.delete(child)

    def setup_columns(self, num_columns, table_name):
        if num_columns and table_name:
            first_values = [t[0] for t in table_name]
            self.out_table['columns'] = list(range(num_columns))
            for col in range(num_columns):
                self.out_table.heading(col, text=f"{first_values[col]}")
                self.out_table.column(col, stretch=True)
        self.out_table.heading("#0", text="")
    
    def get_table_name_mysql(self, query, connection):
        databases = mysql_conn.get_mysql_dbs(connection)
        db_name = None

        for db_name in databases:
            if db_name in query:
                break
        else:
            return "No se encontró el nombre de la base de datos en la consulta."

        tables = mysql_db.get_mysql_tables(connection, db_name)
        table_name = None

        for table_name in tables:
            if table_name in query:
                break
        else:
            return "No se encontró el nombre de la tabla en la consulta."
        
        name, _, _ = mysql_db.get_mysql_table_structure(connection, table_name)

        return name


    def get_table_name_sqls(self, query, connection) -> str:
        databases = sqls_conn.get_sqls_dbs(connection)
        db_name = None
        
        for db_name in databases:
            if db_name in query:
                break
        else:
            return "No se encontró el nombre de la base de datos en la consulta."
    
        tables = sqls_db.get_sql_server_tables(connection, db_name)
        table_name = None
        
        for table_name in tables:
            if table_name in query:
                break
        else:
            return "No se encontró el nombre de la tabla en la consulta."

        name, _, _ = sqls_db.get_sql_server_table_structure(connection, table_name)
        return name


    def run_query(self):
        query = self.int_console.get("1.0", tk.END)
        db_type = self.dbs_var.get()

        if db_type == "SQL Server":
            name_table = self.get_table_name_sqls(query, self.sqls_connect)
            out_text = sqls_conn.sqls_query(self.sqls_connect, query)
        elif db_type == "MySQL":
            name_table = self.get_table_name_mysql(query, self.mysql_connect)
            out_text = mysql_conn.mysql_query(self.mysql_connect, query)
        else:
            messagebox.showerror("Error", "No database type selected")
            return

        self.clear_table()

        if out_text:
            num_columns = len(out_text[0])
            self.setup_columns(num_columns, name_table)

            for row in out_text:
                self.out_table.insert("", "end", values=row)

    
    def select_sql_dbs(self, connect):
        self.update_sql_dbs()
        
        self.frame1.after(100000, self.select_sql_dbs, connect)

    def select_mysql_dbs(self, connect):
        self.update_mysql_dbs()
        
        self.frame1.after(100000, self.select_mysql_dbs, connect)

    def update_sql_dbs(self):
        self.tree_sql.delete(*self.tree_sql.get_children())  # Limpiar árbol de SQL
        dbs = sqls_conn.get_sqls_dbs(self.sqls_connect)
        for db in dbs:
            db_id = self.tree_sql.insert("", tk.END, text=db, open=False)
            tables = sqls_db.get_sql_server_tables(self.sqls_connect, db)
            for table in tables:
                self.tree_sql.insert(db_id, tk.END, text=f'dbo.{table}')

    def update_mysql_dbs(self):
        self.tree_mysql.delete(*self.tree_mysql.get_children())  # Limpiar árbol de MySQL
        dbs = mysql_conn.get_mysql_dbs(self.mysql_connect)
        for db in dbs:
            db_id = self.tree_mysql.insert("", tk.END, text=db, open=False)
            tables = mysql_db.get_mysql_tables(self.mysql_connect, db)
            for table in tables:
                self.tree_mysql.insert(db_id, tk.END, text=table)
    
    def on_closing(self):
        close = messagebox.askyesno("Close App?", "Are you sure to close the app?")

        if close:
            if self.sqls_connect is not None and self.mysql_connect is not None:
                sqls_conn.close_sqls_conn(self.sqls_connect)
                mysql_conn.close_mysql_conn(self.mysql_connect)
            elif self.sqls_connect is not None:
                sqls_conn.close_sqls_conn(self.sqls_connect)
            elif self.mysql_connect is not None:
                mysql_conn.close_mysql_conn(self.mysql_connect)
            else:
                ...
            self.destroy()

