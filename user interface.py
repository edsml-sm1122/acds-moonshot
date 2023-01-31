import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from gui import check_label_folder, check_image_folder

root = tk.Tk()
root.title("Crater Detection")


#file_list = pd.Series(data = [], index=['a', 'b', 'c'])

def import_folder():

    folder_path = tk.filedialog.askdirectory()
    file_list.delete(0, tk.END) # clear the list

    if folder_path:
        images_folder = os.path.join(folder_path, "images")
        labels_folder = os.path.join(folder_path, "labels")
        check_image_folder(images_folder)
        #check_label_folder(images_folder, labels_folder)
        #check_location_folder(...)
        
        for file_name in os.listdir(images_folder):
            file_list.insert(tk.END, file_name)

        
def get_all_settings():
    settings = {
        'Planet': planet_selected.get(),
        'IoU': IoU_entry.get(),
        'ImageSize': image_size_entry.get(),
        'output': output_var.get(), 
    }
    print(settings)
    return settings
    

# Import button
import_btn = ttk.Button(text="Import Folder", command=import_folder)

# Selection between Mars & Moon
planet_selected = tk.StringVar()
planet_selected.set("Mars")
mars_rb = tk.Radiobutton(root, text="Mars", variable=planet_selected, value="Mars")
moon_rb = tk.Radiobutton(root, text="Moon", variable=planet_selected, value="Moon")

# Image size entry box
image_size_label = tk.Label(root, text="Image size (m/px):")
default_image_size = 100
image_size_entry = tk.Entry(root)
image_size_entry.insert(0, default_image_size)

# IoU
IoU_label = tk.Label(root, text="IoU thresholds:")
default_IoU = 0.5
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


# display the file list
file_list = ttk.Treeview(root, column=("image", "label", "latitude", "longitude"), show='headings')

# Run button
get_output_btn = tk.Button(root, text="Submit", command=get_all_settings)

import_btn.pack()
mars_rb.pack()
moon_rb.pack()
image_size_label.pack()
image_size_entry.pack()
IoU_label.pack()
IoU_entry.pack()
output_label.pack()
output_dropdown.pack()
file_list.pack()
get_output_btn.pack()


root.mainloop()
vi