"""This module is used for the user interface (GUI)"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from gui_helper import check_label_folder, check_image_folder, check_location_folder, remove_ds_store
from visualisation import boundBox, comparedBox
from statistic import tripleStatic
import pandas as pd
import shutil
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
        self.option_list = [0, 1, 0, 0, 0]
        
        self.get_output_btn = tk.Button(self.master, text="Submit", command=self.submit_functions)

        self.import_btn.pack()
        self.mars_rb.pack()
        self.moon_rb.pack()
        self.image_size_label.pack()
        self.image_size_entry.pack()
        self.IoU_label.pack()
        self.IoU_entry.pack()
        self.output_label.pack()
        
        self.label_added = False
        self.location_added = False
        
        
        self.update_option_list = []
        for i in range(5):
            self.temp_option = tk.IntVar()
            
            if i == 1:
                self.chk = tk.Checkbutton(self.master, text=self.checkbox_labels[i], variable=self.temp_option, state="disabled")
            else:  
                self.chk = tk.Checkbutton(self.master, text=self.checkbox_labels[i], variable=self.temp_option)
            
            
            self.temp_option.set(self.option_list[i])
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
                locations_folder, files = check_location_folder(images_folder, locations_folder)
                if locations_folder != "locations":
                    tk.messagebox.showerror('Error', locations_folder)
                else:
                    location_label = tk.Label(self.master, text="Locations have been provided.")
                
                    files["latitudes"] = remove_ds_store(files["latitudes"])
                    files["longitudes"] = remove_ds_store(files["longitudes"])

                    import_df["latitudes"] = files['latitudes']
                    import_df["longitudes"] = files['longitudes']
                    
                    self.location_added = True
            else:
                location_label = tk.Label(self.master, text="Locations have not been provided.")

            
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
                    files = remove_ds_store(files)
                    import_df["labels"] = files
                    self.label_added = True
            else:
                label_label = tk.Label(self.master, text="The images are not labelled!")
            
            label_label.pack(side='top')
            location_label.pack(side='top')

            import_df.to_csv('import_data.csv', index=False)
            
            print(self.label_added)
            print(self.location_added)
            return import_df
            
        


    def extract_df_columns(self, path):
        image_dirs = []
        image_ids = []
        label_dirs = []
        
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            if self.label_added:
                index = headers.index('labels')
                for row in reader:
                    image_dirs.append(row[1])
                    image_ids.append(row[0].split(".")[0])
                    label_dirs.append(row[index])
            else:
                for row in reader:
                    image_dirs.append(row[1])
                    image_ids.append(row[0].split(".")[0])
        
        return image_dirs, image_ids, label_dirs


    def no_box(self, settings, image_dirs):

        if settings['Options'][0]:
            try:
                os.mkdir(settings['Output'] + '/' + 'Original images')
            except FileExistsError:
                    tk.messagebox.showerror("Error", "Original images folder already exists")
    
            for image_dir in image_dirs:
                # get the filename from the directory path
                filename = os.path.basename(image_dir)
                
                # construct the output path
                output_path = os.path.join(settings['Output'] + '/' + 'Original images' + '/', filename)
                
                # copy the image to the output folder
                shutil.copy(image_dir, output_path)
                
    def one_box(self, settings, image_dirs, image_ids):
        if settings['Options'][1]:
            try:
                os.mkdir(settings['Output'] + '/' + 'CDM bounding boxes')
            except FileExistsError:
                tk.messagebox.showerror("Error", "CDM bounding boxes folder already exists")
                
            for i in range(len(image_ids)):
                filename = os.path.basename(image_dirs[i])
                output_path = os.path.join(settings['Output'] + '/' + 'CDM bounding boxes' + '/', filename)
                boundBox(image_dirs[i], 
                         settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv',
                         output_path)
                
                
    def two_boxes(self, settings, image_dirs, image_ids, label_dirs):
        if settings['Options'][2]:
            if label_dirs:
                try:
                    os.mkdir(settings['Output'] + '/' + 'True labels and CDM bounding boxes')
                except FileExistsError:
                    tk.messagebox.showerror("Error", "True labels and CDM bounding boxes folder already exists")
                    
                for i in range(len(image_ids)):
                    filename = os.path.basename(image_dirs[i])
                    output_path = os.path.join(settings['Output'] + '/' + 'True labels and CDM bounding boxes' + '/', filename)
                    comparedBox(image_dirs[i], 
                             settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv',
                             label_dirs[i],
                             output_path)
                    
    def performance_stats(self, settings, image_ids, label_dirs, IoU):
        if settings['Options'][4]:
            if label_dirs:
                TP, FP, FN = 0,0,0
                try:
                    os.mkdir(settings['Output'] + '/' + 'statistics')
                except FileExistsError:
                    tk.messagebox.showerror("Error", "statistics folder already exists")
                for i in range(len(image_ids)):
                    nTP, nFP, nFN = tripleStatic( 
                             settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv',
                             label_dirs[i],
                             threshold = float(IoU))
                    TP += nTP
                    FP += nFP
                    FN += nFN
                output_path = os.path.join(settings['Output'] + '/' + 'statistics' + '/', 'performance matrix.csv')
                triOut = [[TP, FP, FN]]
                triName=['TP','FP','FN']
                triCsv=pd.DataFrame(columns=triName,data=triOut)
                triCsv.to_csv(output_path, index=False)
                

                    
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
        
        # passing the parameters to the model, creating a detection folder into the user selected output directory
        #os.mkdir(settings['Output'] + '/' + 'detections')
        
        image_dirs, image_ids, label_dirs = self.extract_df_columns('import_data.csv')
        
        self.no_box(settings, image_dirs)
        self.one_box(settings, image_dirs, image_ids)
        self.two_boxes(settings, image_dirs, image_ids, label_dirs)
        
        self.performance_stats(settings, image_ids, label_dirs, settings['IoU'])

        # when the user want the bounding box for the detections only   
        
        
        tk.messagebox.showinfo("Success",  "Successfully exported!")    


def main(): 
    root = tk.Tk()
    root.title("Crater Detection Model (CDM)")
    #root.geometry('500x500')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()