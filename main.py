# main.py
import tkinter as tk
from tkinter import filedialog
from controller import Controller
from model import Model
from view import View

def main():
    root = tk.Tk()
    root.title("Audio Analysis App")

    model = Model("")
    view = View(root)
    controller = Controller(model, view)

    view.set_controller(controller)

    view.grid(row=0, column=0, padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
