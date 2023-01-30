import tkinter as tk
from tkinter import filedialog
from tkinter import ttk



root = tk.Tk()
root.title("Crater Detection")


def import_folder():
    folder_path = filedialog.askdirectory()
    print(f"Selected folder: {folder_path}")

def select_planet():
    if planet_selected.get() == "Mars":
        print("Mars selected")
    else:
        print("Moon selected")
        
def on_select(event):
    print(f"Selected option: {output_options_combo.get()}")

planet_selected = tk.StringVar()
planet_selected.set("Mars")

output_options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
output_options_combo = ttk.Combobox(root, values=output_options)
output_options_combo.current(0)
output_options_combo.bind("&#8203;`oaicite:{"index":1,"invalid_reason":"Malformed citation <<ComboboxSelected>>"}`&#8203;", on_select)


# location pack
import_btn = tk.Button(text="Import Folder", command=import_folder)
mars_rb = tk.Radiobutton(root, text="Mars", variable=planet_selected, value="Mars", command=select_planet)
moon_rb = tk.Radiobutton(root, text="Moon", variable=planet_selected, value="Moon", command=select_planet)
output_options_combo.pack()

import_btn.pack()
mars_rb.pack()
moon_rb.pack()

root.mainloop()
