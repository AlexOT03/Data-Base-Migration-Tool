import tkinter as tk
from tkinter import ttk

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Progress of Migration")

        title_label1 = tk.Label(self, text="Passing data to tables")
        title_label1.pack(padx=10, pady=10, anchor='w')

        self.bar1 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar1.pack(padx=0, pady=(0, 20))

        title_label2 = tk.Label(self, text="Creating foreignkeys")
        title_label2.pack(padx=10, pady=10, anchor='w')

        self.bar2 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar2.pack(padx=0, pady=(0, 20))