from tkinter import *
from glob import glob

pdf_files = glob("**/*.pdf", recursive=True)

window = Tk()
window.title("YoFinder")
window.geometry("350x200")

lbl = Label(window, text=pdf_files, font=("Arial Bold", 20))
lbl.grid(row=0, column=0)

window.mainloop()