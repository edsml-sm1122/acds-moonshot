import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Crater Detection")

def import_folder():
    folder_path = filedialog.askdirectory()
    print(f"Selected folder: {folder_path}")

button = tk.Button(text="Import Folder", command=import_folder)
button.pack()

root.mainloop()

