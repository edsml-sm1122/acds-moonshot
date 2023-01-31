import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from gui import check_label_folder, check_image_folder, check_location_folder, remove_ds_store
import pandas as pd

root = tk.Tk()
root.title("Crater Detection")
root.geometry('500x500')


def import_folder():

    folder_path = tk.filedialog.askdirectory()
    print(folder_path)

    if folder_path:
        images_folder = os.path.join(folder_path, "images")
        labels_folder = os.path.join(folder_path, "labels")
        locations_folder = os.path.join(folder_path, "locations")

        image_check, files = check_image_folder(images_folder)
        if image_check != "images":
            tk.messagebox.showerror('Error', image_check)

        files['name'] = remove_ds_store(files['name'])
        files['path'] = remove_ds_store(files['path'])

        df = pd.DataFrame.from_dict(files)

        if os.path.exists(labels_folder):
            label_check, files = check_label_folder(images_folder, labels_folder)
            if label_check != "labels":
                tk.messagebox.showerror('Error', label_check)
            
            files = remove_ds_store(files)

            df["labels"] = files

        if os.path.exists(locations_folder):
            locations_folder, files = check_location_folder(locations_folder)
            if locations_folder != "locations":
                tk.messagebox.showerror('Error', locations_folder)
            
            files["latitudes"] = remove_ds_store(files["latitudes"])
            files["longitudes"] = remove_ds_store(files["longitudes"])

            df["latitudes"] = files['latitudes']
            df["longitudes"] = files['longitudes']

        df.to_csv('data.csv', index=False)
        return df


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
#file_list = ttk.Treeview(root, column=("images", "latitude", "longitude"), show='headings')

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
#file_list.pack()
get_output_btn.pack()


root.mainloop()