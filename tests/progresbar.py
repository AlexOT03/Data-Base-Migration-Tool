from tkinter import *
from tkinter.ttk import *
import time

def start():
    GB = 10
    download = 0

    while(download<GB):
        time.sleep(1)
        bar['value'] += 10
        download += 1
        window.update_idletasks()

window = Tk()
bar = Progressbar(window, orient=HORIZONTAL, length=300)
bar.pack(padx=20, pady=20)
button = Button(window, text="Download", command=start).pack()

window.mainloop()