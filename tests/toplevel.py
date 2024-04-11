import tkinter as tk
from tkinter import ttk

class ProgressWindow(tk.Top):
    def __init__(self) -> None:
        super().__init__()
        self.title("Progres of Migration")

        self.title = tk.Label(self, text="Passing data to tables").pack(padx=10, pady=10, anchor='w')
        self.bar1 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar1.pack(padx=0, pady=(0, 20))

        self.title = tk.Label(self, text="Creating foreignkeys").pack(padx=10, pady=10, anchor='w')
        self.bar2 = ttk.Progressbar(self, orient='horizontal', length=500)
        self.bar2.pack(padx=0, pady=(0, 20))

app = ProgressWindow()
app.mainloop()