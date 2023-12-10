import tkinter as tk
from view import View
from controller import Controller
from model import Model

def main():
    root = tk.Tk()
    root.title("Audio Analysis App")

    # Create instances of Model, View, and Controller
    model = Model("")
    view = View(root)
    controller = Controller(model, view)

    # Set controller for communication between View and Controller
    view.set_controller(controller)

    # Place View in the tkinter app
    view.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()
