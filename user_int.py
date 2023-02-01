import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from gui import check_label_folder, check_image_folder, check_location_folder, remove_ds_store
import pandas as pd
import csv

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
        self.checkbox_labels = ['Original', 
                        'CDM bounding boxes', 
                        'CDM and true bounding boxes', 
                        'Crater size-frequency distribution', 
                        'Performance matrix']
        self.option_list = [0, 0, 0, 0, 0]
        


        self.get_output_btn = tk.Button(self.master, text="Submit", command=self.submit_functions)

        self.import_btn.pack()
        self.mars_rb.pack()
        self.moon_rb.pack()
        self.image_size_label.pack()
        self.image_size_entry.pack()
        self.IoU_label.pack()
        self.IoU_entry.pack()
        self.output_label.pack()
        
        self.update_option_list = []
        for i in range(5):
            self.temp_option = tk.IntVar()
            self.chk = tk.Checkbutton(self.master, text=self.checkbox_labels[i], variable=self.temp_option)
            self.chk.pack()
            self.update_option_list.append(self.temp_option)
        
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
            import_df = pd.DataFrame.from_dict(files)
            
            if os.path.exists(locations_folder):
                locations_folder, files = check_location_folder(locations_folder)
                if locations_folder != "locations":
                    tk.messagebox.showerror('Error', locations_folder)
                
                files["latitudes"] = remove_ds_store(files["latitudes"])
                files["longitudes"] = remove_ds_store(files["longitudes"])

                import_df["latitudes"] = files['latitudes']
                import_df["longitudes"] = files['longitudes']

            
            file_list = tk.Listbox(self.master)
            file_list.pack()
            for name in import_df['name']:
                file_list.insert(tk.END, name)

            if os.path.exists(labels_folder):
                label_check, files = check_label_folder(images_folder, labels_folder)
                if label_check != "labels":
                    tk.messagebox.showerror('Error', label_check)
                else:
                    label_label = tk.Label(self.master, text="The images are labelled!")
                    #label_status = tk.Canvas(self.master, height=14, width=14, bg='#10cc52')
                
                files = remove_ds_store(files)
                import_df["labels"] = files
            else:
                label_label = tk.Label(self.master, text="The images are not labelled!")
                #label_status = tk.Canvas(self.master, height=14, width=14, bg='red')
                #label_status.config(bg='red')
            
            label_label.pack(side='top')
            #label_status.pack(side='top')

            import_df.to_csv('import_data.csv', index=False)
            
            return import_df


    def submit_functions(self):
        
        dir_path = filedialog.askdirectory(initialdir=".", title="Create Output Directory", parent=self.master)

        for i in range(5):
            if self.update_option_list[i].get() == 1:
                self.option_list[i] = 1
            else:
                self.option_list[i] = 0
        settings = {
            'Planet': self.planet_selected.get(),
            'IoU': self.IoU_entry.get(),
            'ImageSize': self.image_size_entry.get(),
            'Options': self.option_list,
            'Output': dir_path,
        }
        
        
        with open('settings.csv', 'w', newline='') as csvfile:
            # Creating a writer object
            writer = csv.DictWriter(csvfile, fieldnames=settings.keys())

            # Writing headers (keys of the dictionary)
            writer.writeheader()

            # Writing data row
            writer.writerow(settings)
            
        # setting_df = pd.DataFrame.from_dict(settings)
        # setting_df.to_csv('settings.csv', index=False)
        
        # print(settings)
        
        #print("Directory saved as:", dir_path)   

        # os.mkdir(dir_path + '/' + 'detections')
        # os.mkdir(dir_path + '/' + 'images')
        # os.mkdir(dir_path + '/' + 'statistics') 
        
        #self.settings = self.get_all_settings()      


def main(): 
    root = tk.Tk()
    root.title("Crater Detection Model (CDM)")
    #root.geometry('500x500')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()