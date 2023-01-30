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
        
def get_image_size():
    image_size = image_size_entry.get()
    print("Image size is:", image_size)
    
def get_IoU():
    IoU = IoU_entry.get()
    print("IoU threshold is:", IoU)

def get_all_settings():
    settings = dict({
        
    })
    

# Import button
import_btn = tk.Button(text="Import Folder", command=import_folder)

# Selection between Mars & Moon
planet_selected = tk.StringVar()
planet_selected.set("Mars")
mars_rb = tk.Radiobutton(root, text="Mars", variable=planet_selected, value="Mars", command=select_planet)
moon_rb = tk.Radiobutton(root, text="Moon", variable=planet_selected, value="Moon", command=select_planet)

# Image size entry box
image_size_label = tk.Label(root, text="Image size (m/px):")
default_image_size = 100
image_size_entry = tk.Entry(root)
image_size_entry.insert(0, default_image_size)

# IoU
IoU_label = tk.Label(root, text="IoU thresholds:")
default_IoU = 10
IoU_entry = tk.Entry(root)
IoU_entry.insert(0, default_IoU)

# output settings selection box
output_label = tk.Label(root, text="Output settings:")
output_options = ['Original', 
                  'CDM bounding boxes', 
                  'CDM and true bounding boxes', 
                  'Crater size-frequency distribution', 
                  'Confusion matrix']
output_var = tk.StringVar(root)
output_var.set(output_options[0])
output_dropdown = tk.OptionMenu(root, output_var, *output_options)






# Run button
get_output_btn = tk.Button(root, text="Submit", command=get_image_size)

import_btn.pack()
mars_rb.pack()
moon_rb.pack()
image_size_label.pack()
image_size_entry.pack()
IoU_label.pack()
IoU_entry.pack()
output_label.pack()
output_dropdown.pack()
get_output_btn.pack()


root.mainloop()
