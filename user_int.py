import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from gui import check_label_folder, check_image_folder, check_location_folder, remove_ds_store
import pandas as pd

class App(tk.Tk):

    def __init__(self, master):

        self.master = master

        self.import_btn = ttk.Button(text="Import Folder", command=self.import_folder)

        # Selection between Mars & Moon
        self.planet_selected = tk.StringVar()
        self.planet_selected.set("Mars")
        self.mars_rb = tk.Radiobutton(self.master, text="Mars", variable=self.planet_selected, value="Mars")
        self.moon_rb = tk.Radiobutton(self.master, text="Moon", variable=self.planet_selected, value="Moon")

        # Image size entry box
        self.image_size_label = tk.Label(self.master, text="Image size (m/px):")
        self.default_image_size = 100
        self.image_size_entry = tk.Entry(self.master)
        self.image_size_entry.insert(0, self.default_image_size)

        # IoU
        self.IoU_label = tk.Label(self.master, text="IoU thresholds:")
        self.default_IoU = 0.5
        self.IoU_entry = tk.Entry(self.master)
        self.IoU_entry.insert(0, self.default_IoU)

        # output settings selection box
        self.output_label = tk.Label(self.master, text="Output settings:")
        self.output_options = ['Original', 
                        'CDM bounding boxes', 
                        'CDM and true bounding boxes', 
                        'Crater size-frequency distribution', 
                        'Confusion matrix']
        self.output_var = tk.StringVar(self.master)
        self.output_var.set(self.output_options[0])
        self.output_dropdown = tk.OptionMenu(self.master, self.output_var, *self.output_options)

        self.get_output_btn = tk.Button(self.master, text="Submit", command=self.get_all_settings)

        self.import_btn.pack()
        self.mars_rb.pack()
        self.moon_rb.pack()
        self.image_size_label.pack()
        self.image_size_entry.pack()
        self.IoU_label.pack()
        self.IoU_entry.pack()
        self.output_label.pack()
        self.output_dropdown.pack()
        self.get_output_btn.pack()


    def import_folder(self):

        folder_path = tk.filedialog.askdirectory()

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
            file_list = tk.Listbox(self.master)
            file_list.pack()
            for name in df['name']:
                file_list.insert(tk.END, name)
            return df

    def get_all_settings(self):
        settings = {
            'Planet': self.planet_selected.get(),
            'IoU': self.IoU_entry.get(),
            'ImageSize': self.image_size_entry.get(),
            'output': self.output_var.get(), 
        }
        print(settings)
        return settings

def main(): 
    root = tk.Tk()
    root.title("Crater Detection Model (CDM)")
    root.geometry('500x500')
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()