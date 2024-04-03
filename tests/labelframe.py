import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()

# configure the root window
root.geometry('300x200')
root.resizable(False, False)
root.title('LabelFrame Demo')

# label frame
lf = ttk.LabelFrame(root, text='Alignment')
lf.grid(column=0, row=0, padx=20, pady=20)

alignment_var = tk.StringVar()
alignments = ('Left', 'Center', 'Right')

# create radio buttons and place them on the label frame

grid_column = 0
for alignment in alignments:
    # create a radio button
    radio = ttk.Radiobutton(lf, text=alignment, value=alignment, variable=alignment_var)
    radio.grid(column=grid_column, row=0, ipadx=10, ipady=10)
    # grid column
    grid_column += 1

root.mainloop()