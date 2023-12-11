import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text="Selected File: " + file_path)
        # Here you can perform further operations with the selected file path

# Create a Tkinter window
root = tk.Tk()
root.title("File Input GUI")

# Create a label for displaying the selected file path
label = tk.Label(root, text="Select a file", wraplength=300)
label.pack(padx=10, pady=20)

# Create a button to open a file dialog
button = tk.Button(root, text="Open File", command=open_file)
button.pack(padx=10, pady=10)

# Run the main Tkinter loop
root.mainloop()
