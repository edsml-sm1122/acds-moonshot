"""This module is used for the user interface (GUI)"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import ast

import os
import shlex, subprocess
from distutils.dir_util import copy_tree

from gui_helper import check_label_folder, check_image_folder, check_location_folder, remove_ds_store
from visualisation import boundBox, comparedBox, to_coords, add_loc_all_detected_csv
from data_manager import DataManager
from model_utils import MyModel, bigimgpix2cellpix, crop, convert_function, output_combined_csv
from statistic import tripleStatic, plot_frequency_distribution
import pandas as pd
import shutil
import csv

class App(tk.Tk):
    """ 
    GUI for the Crater Detection Model (CDM).

    Attributes:
    ----------

        - master: Tkinter root window.

        - import_df: Pandas DataFrame used to store information about names and paths of User input data.
        - label_added: Boolean (True/False), True if 'labels/' subdirectory exists in the User-specified input folder. 
        - location_added: Boolean (True/False), True if 'locations/' subdirectory exists in the User-specified input folder.
        - import_btn: Tkinter import button.

        - planet_selected: Tkinter StringVar object which specifies the selected planet (default: 'Mars').
        - mars_rb: Tkinter Radiobutton which allows the user to select the Mars planet.
        - moon_rb: Tkinter Radiobutton which allows the user to select the Moon planet.

        - image_size_label: Tkinter Label which tells the user to add information about image size in the input box.
        - image_size_entry: Tkinter input box which allows the user to add information about image size.
        - default_image_size: default image size (set to 100 m/px).

        - IoU_label: Tkinter Label which tells the user to add information about IoU threshold in the input box.
        - default_IoU: default IoU threshold (set to 0.5).
        - IoU_entry: Tkinter input box which allows the user to add information about IoU threshold.

        - output_label: Tkinter Label which tells the user to add information about the output.
        - checkbox_labels: list containing checkbox labels (for the User's selection of output). 
        - selected_checkboxes: list of Booleans associated with the output checkbox selection (by default, the second, third and fifth box is ticked).
        - var0: Tkinter IntVar variable associated with checkbutton check0.
        - var1: Tkinter IntVar variable associated with checkbutton check1.
        - var2: Tkinter IntVar variable associated with checkbutton check2.
        - var3: Tkinter IntVar variable associated with checkbutton check3.
        - var4: Tkinter IntVar variable associated with checkbutton check4.
        - check0: Tkinter Checkbutton associated with checkbox_labels[0].
        - check1: Tkinter Checkbutton associated with checkbox_labels[1].
        - check2: Tkinter Checkbutton associated with checkbox_labels[2].
        - check3: Tkinter Checkbutton associated with checkbox_labels[3].
        - check4: Tkinter Checkbutton associated with checkbox_labels[4].
        
        - get_output_btn: Tkinter submit button.
    """

    def __init__(self, master):
        """ 
        Creates the GUI.
        
        Parameters
        ----------
        master: Tkinter root window.

        """

        self.master = master
        self.import_df = pd.DataFrame()
        self.label_added = False
        self.location_added = False
        
        self.images_folder = False
        self.labels_folder = False
        self.locations_folder = False
        self.output_folder = False


        # Import button
        self.import_btn = ttk.Button(text="Import Folder", command=self.import_folder)
        
        # Mars & Moon selection
        self.planet_selected = tk.StringVar()
        self.planet_selected.set("mars")
        self.mars_rb = tk.Radiobutton(self.master, text="Mars", variable=self.planet_selected, value="mars")
        self.moon_rb = tk.Radiobutton(self.master, text="Moon", variable=self.planet_selected, value="moon")

        # Image size entry box
        self.image_size_label = tk.Label(self.master, text="Image Size (m/px):")
        self.default_image_size = 100
        self.image_size_entry = tk.Entry(self.master)
        self.image_size_entry.insert(0, self.default_image_size)

        # IoU entry box
        self.IoU_label = tk.Label(self.master, text="IoU Threshold:")
        self.default_IoU = 0.5
        self.IoU_entry = tk.Entry(self.master)
        self.IoU_entry.insert(0, self.default_IoU)

        # Output settings (selection box)
        self.output_label = tk.Label(self.master, text="Output Settings:")
        self.checkbox_labels = ['original images', 
                                'bounding boxes', 
                                'bounding boxes (with ground truth)', 
                                'size-frequency dist', 
                                'performance matrix']
        self.selected_checkboxes = [0,1,0,0,0]

        # the second box is disabled because it should be chosen by default.
        # if labels are not added, the second and fourth boxes are disabled.
        self.var0 = tk.IntVar()
        self.check0 = tk.Checkbutton(self.master, text=self.checkbox_labels[0], variable=self.var0, state="normal", command=lambda: self.update_checkbutton(self.var0, self.checkbox_labels[0], 0)) 
        
        self.var1 = tk.BooleanVar()
        self.var1.set(True)
        self.check1 = tk.Checkbutton(self.master, text=self.checkbox_labels[1], variable=self.var1, state="disabled", command=lambda: self.update_checkbutton(self.var1, self.checkbox_labels[1], 1)) 
        
        self.var2 = tk.IntVar()
        self.check2 = tk.Checkbutton(self.master, text=self.checkbox_labels[2], variable=self.var2, state="disabled", command=lambda: self.update_checkbutton(self.var2, self.checkbox_labels[2], 2)) 
       
        self.var3 = tk.IntVar()
        self.check3 = tk.Checkbutton(self.master, text=self.checkbox_labels[3], variable=self.var3, state="normal", command=lambda: self.update_checkbutton(self.var3, self.checkbox_labels[3], 3))

        self.var4 = tk.IntVar()
        self.check4 = tk.Checkbutton(self.master, text=self.checkbox_labels[4], variable=self.var4, state="disabled", command=lambda: self.update_checkbutton(self.var4, self.checkbox_labels[4], 4))

        # Submit button
        self.get_output_btn = tk.Button(self.master, text="Submit", command=self.submit_functions)

        # Tkinter packs
        self.import_btn.pack()
        self.mars_rb.pack()
        self.moon_rb.pack()
        self.image_size_label.pack()
        self.image_size_entry.pack()
        self.IoU_label.pack()
        self.IoU_entry.pack()
        self.output_label.pack()
        self.check0.pack()
        self.check1.pack()
        self.check2.pack()
        self.check3.pack()
        self.check4.pack()
        self.get_output_btn.pack()


    def update_checkbutton(self, var, name, index):
        """
        This function is used to update the selected_checkboxes attribute.
        (selected_checkboxes contains a Boolean list which indicates which checkbox the user has ticked).

        Parameters
        ----------
        var: Tkinter IntVar variable associated with a checkbox button (either 1 or 0).
        name: str, checkbox name (i.e. 'original images', 'bounding boxes', etc).
        index: int, represents the index of the checkbox (i.e. index 0 corresponds to the checkbox 'original images').

        Returns
        -------
        None
        
        """
        if index == 1:
            self.selected_checkboxes[index] = 1
        else:
            if var.get() == 1:
                self.selected_checkboxes[index] = var.get()
                print(f"'{name}' checkbox was ticked.")
            else:
                self.selected_checkboxes[index] = var.get()
                print(f"'{name}' checkbox was unticked.")

    def import_folder(self):
        '''
        This function is called when the "Import Folder" button in the pop-up window is clicked.

        It accepts a User-specified input folder location. The input folder should contain a subdirectory 'images/' that contains a single image or multiple images. This is checked in the import_images() method.
        The names of the image files are displayed in the window.

        If the input folder contains a subdirectory called 'locations/', the import_locations() method is called.
        If the input folder contains a subdirectory called 'labels/', the import_labels() method is called.

        The import_folder() method displays strings to indicate whether or not locations and labels have been provided by the User.
        
        Parameters
        ----------
        None

        Returns
        -------
        None

        '''

        folder_path = tk.filedialog.askdirectory()

        if folder_path:
            self.images_folder = os.path.join(folder_path, "images")
            self.labels_folder = os.path.join(folder_path, "labels")
            self.locations_folder = os.path.join(folder_path, "locations")

            self.import_images(self.images_folder)
            
            if os.path.exists(self.locations_folder):
                self.location_added = True
                location_label = self.import_locations(self.images_folder, self.locations_folder)
            else:
                location_label = tk.Label(self.master, text="Locations have not been provided.")

            file_list = tk.Listbox(self.master) # will list the location files in a box
            file_list.pack()
            for name in self.import_df['name']:
                file_list.insert(tk.END, name)

            if os.path.exists(self.labels_folder):
                self.check2.config(state='normal')
                self.check4.config(state='normal')
                label_label = self.import_labels(self.images_folder, self.labels_folder)
            else:
                label_label = tk.Label(self.master, text="The images are not labelled!")
            
            label_label.pack(side='top')
            location_label.pack(side='top')

            self.import_df['folder_path'] = folder_path


    def import_images(self, images_folder):
        '''
        This method is called in the import_folder() method.

        The method performs checks on the 'images/' folder by calling the check_image_folder() function from the gui_helper Module.
        A dictionary ('files') is created, containing names and paths to the images.
        Any '.DS_Store' files and paths are removed from the dictionary by calling the remove_ds_store() function from the gui_helper Module.

        The self.import_df Pandas DataFrame is then updated to become a DataFrame containing the names and paths of the input images.
        
        Parameters
        ----------
        images_folder: the path to the subdirectory 'images/' (located in the User-specified input directory).

        Returns
        -------
        None

        '''
        
        image_check, files = check_image_folder(images_folder)
        if image_check != "images":
            tk.messagebox.showerror('Error', image_check)

        files['name'] = remove_ds_store(files['name'])
        files['path'] = remove_ds_store(files['path'])
        self.import_df = pd.DataFrame.from_dict(files)


    def import_locations(self, images_folder, locations_folder):
        '''
        This method is called in the import_folder() method.

        The method performs checks on the 'locations/' folder by calling the check_location_folder() function from the gui_helper Module.
        A dictionary ('files') is created, containing latitude and longitude information from the csv files in the location folder.
        Any '.DS_Store' files are removed from the dictionary by calling the remove_ds_store() function from the gui_helper Module.

        Two columns are added to the self.import_df Pandas DataFrame: 'latitudes' and 'longitudes'.
        
        Parameters
        ----------
        images_folder: the path to the subdirectory 'images/' (located in the User-specified input directory).
        locations_folder: the path to the subdirectory 'locations/' (located in the User-specified input directory).

        Returns
        -------
        None

        '''

        locations_folder, files = check_location_folder(images_folder, locations_folder)
        if locations_folder != "locations":
            tk.messagebox.showerror('Error', locations_folder)
        else:
            location_label = tk.Label(self.master, text="Locations have been provided.")
        
        files["latitudes"] = remove_ds_store(files["latitudes"])
        files["longitudes"] = remove_ds_store(files["longitudes"])

        self.import_df["latitudes"] = files['latitudes']
        self.import_df["longitudes"] = files['longitudes']

        return location_label


    def import_labels(self, images_folder, labels_folder):
        '''
        This method is called in the import_folder() method.

        The method performs checks on the 'labels/' folder by calling the check_label_folder() function from the gui_helper Module.
        A list ('files') is created, containing the paths to the csv files in the labels_folder.
        Any '.DS_Store' paths are removed from the dictionary by calling the remove_ds_store() function from the gui_helper Module.

        One column is added to the self.import_df Pandas DataFrame: 'labels'.
        
        Parameters
        ----------
        images_folder: the path to the subdirectory 'images/' (located in the User-specified input directory).
        labels_folder: the path to the subdirectory 'labels/' (located in the User-specified input directory).

        Returns
        -------
        None

        '''

        label_check, files = check_label_folder(images_folder, labels_folder)
        if label_check != "labels":
            tk.messagebox.showerror('Error', label_check)
        else:
            label_label = tk.Label(self.master, text="The images are labelled!")
            files = remove_ds_store(files)
            self.import_df["labels"] = files
            self.label_added = True

        return label_label


    def original_images(self, settings, image_dirs):
        """
        This method is called in the submit_functions() method, below.
        It creates an 'original images/' subdirectory in the 'images/' subdirectory.
        It then fills 'original images/' subdirectory  by copying the user's input images 
        and pasting them into the 'original images/' subdirectory. 
        
        More information can be found in the Docstring of the submit_functions() method.

        Parameters
        ----------
        settings: list which contains information about the boxes that were ticked by the user;
        if 'original images' box is ticked (meaning that the element with index 0 is equal to 1), the original_images() method should run.

        image_dirs: path to the 'images' directory (which contains the original input images).

        Returns
        -------
        None

        """

        if settings['Options'][0]:
            try:
                os.mkdir(settings['Output'] + '/images/' + 'original images')
            except FileExistsError:
                    tk.messagebox.showerror("Error", "'original images' folder already exists")

            output_path = os.path.join(settings['Output'] + '/images/' + 'original images')
            image_dirs = shlex.split(image_dirs)[0]
            print('this is image_dirs incopy tree')
            print(image_dirs)
            #image_dirs = image_dirs.replace('\ ', ' ')
            copy_tree(str(image_dirs), str(output_path))    


    def bounding_boxes(self, settings, image_dirs, image_ids):
        """
        This method is called in the submit_functions() method, below.
        It is a default function of the 'Submit button' (when no output boxes are ticked).
        
        It creates a 'bounding boxes/' subdirectory in the 'images/' subdirectory.
        It then fills 'bounding boxes/' subdirectory with a .png file for each input image, that shows the bounding boxes of the craters detected by the CDM. This is done by calling the boundBox() function in the visualisation Module.
        
        More information can be found in the Docstring of the submit_functions() method,
        and in the Docstring of the boundBox() function (from the visualisation Module).

        Parameters
        ----------
        settings: list which contains information about the boxes that were ticked by the user,
        if 'bounding boxes' box is ticked (meaning that the element with index 1 is equal to 1), the bounding_boxes() method should run.

        image_dirs: list which contains the path to the original input images in the 'images' directory.

        image_ids: list which contains the names of the the original input images in the 'images' directory.

        Returns
        -------
        None

        """
        if settings['Options'][1]:
            try:
                os.mkdir(settings['Output'] + '/images/' + 'bounding boxes')
            except FileExistsError:
                tk.messagebox.showerror("Error", "'bounding boxes' folder already exists")
                
            for i in range(len(image_ids)):
                filename = os.path.basename(image_dirs[i])
                output_path = os.path.join(settings['Output'] + '/images/' + 'bounding boxes' + '/', filename)
                
                csv_path = settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv'
                
                csv_exist = False
                if os.path.isfile(csv_path):
                    csv_exist = True

                    
                boundBox(image_dirs[i], 
                        csv_path,
                        output_path,
                        csv_exist)




    def gd_truth_bounding_boxes(self, settings, image_dirs, image_ids, label_dirs, label_folder_path):
        """
        This method is called in the submit_functions() method, below.
        
        It creates a 'bounding boxes (with ground truth)/' subdirectory in the 'images/' subdirectory.
        It then fills 'bounding boxes (with ground truth)/' subdirectory with a .png file for each input image that shows the bounding boxes of the craters detected by the CDM in one colour and the ground truth bounding boxes in a different color. 
        This is done by calling the comparedBox() function in the visualisation Module.
        
        More information can be found in the Docstring of the submit_functions() method,
        and in the Docstring of the comparedBox() function (from the visualisation Module).

        Parameters
        ----------
        settings: list which contains information about the boxes that were ticked by the user,
        if the 'bounding boxes (with ground truth)' box is ticked (meaning that the element with index 2 is equal to 1), the gd_truth_bounding_boxes() method should run.

        image_dirs: list which contains the path to the original input images in the 'images' directory.

        image_ids: list which contains the names of the original input images in the 'images' directory.

        label_dirs: list which contains the path of the csv files in the 'labels' directory.

        Returns
        -------
        None

        """
        if settings['Options'][2]:
            if label_dirs:
                try:
                    os.mkdir(settings['Output'] + '/images/' + 'bounding boxes (with ground truth)')
                except FileExistsError:
                    tk.messagebox.showerror("Error", "'bounding boxes (with ground truth)' folder already exists")
                    
                    
                    
                
                
                for i in range(len(image_ids)):
                    filename = os.path.basename(image_dirs[i])
                    output_path = os.path.join(settings['Output'] + '/images/' + 'bounding boxes (with ground truth)' + '/', filename)
                    csv_path = settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv'
                    input_csv = os.path.join(label_folder_path, image_ids[i] + '.csv')
                    input_csv = shlex.split(input_csv)[0]
                    print('this is input_csv ===============')
                    print(input_csv)
                    csv_exist = False
                    print('this is csv_path ===============')
                    print(csv_path)
                    
                    
                    print('previous success ===============')
                    print(label_dirs[i])

                    print('this is image_dirs ===============')
                    print(image_dirs[i])
                    
                    
                    
                    if os.path.isfile(csv_path):
                        csv_exist = True
                        
                    comparedBox(image_dirs[i], 
                             csv_path,
                             input_csv,
                             output_path,
                             csv_exist)

    
    
        #self.plot_sf_distribution(settings, image_dirs, image_ids)
    # def plot_frequency_distribution(imgpath, bbpath, R, image_scale, outpath, tbpath = 'None'):   

                
    def plot_sf_distribution(self, settings, image_dirs, image_ids, labels_added):
        #when the option is ticked
        if settings['Options'][3]:
            if settings['Planet'] == 'moon':
                try:
                    os.mkdir(settings['Output'] + '/size frequency distribution/')
                except FileExistsError:
                    tk.messagebox.showerror("Error", "'size frequency distribution' folder already exists")
                
                for i in range(len(image_ids)):
                    filename = os.path.basename(image_dirs[i])
                    print('this is file name sssssssssssssssssssssssssssssssssssssssssssss')
                    print(filename)
                    output_path = os.path.join(settings['Output'] + '/size frequency distribution/' , filename)
                    
                    print('this is outputpath name sssssssssssssssssssssssssssssssssssssssssssss')
                    print(output_path)
                    csv_path = settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv'

                    
                    if labels_added:
                        plot_frequency_distribution(image_dirs[i], 
                                                    csv_path, 
                                                    3474.8, 
                                                    float(settings['Image_size']), 
                                                    output_path, 
                                                    self.labels_folder)
                    
                    else:
                        plot_frequency_distribution(image_dirs[i], 
                                                    csv_path, 
                                                    3474.8, 
                                                    float(settings['Image_size']), 
                                                    output_path, 
                                                    tbpath = 'None')


                
                
                
        
            
    

    def performance_matrix(self, settings, image_ids, label_dirs, IoU, label_folder_path):
        """
        This method is called in the submit_functions() method, below.
        
        It creates a 'statistics' subdirectory in the output directory (which has a User-specified name).
        It then fills the 'statistics' subdirectory with a .csv file for each input image.
        Each csv file summarises the True Positive, False Positive and False Negative detections in the image.
        
        More information can be found in the Docstring of the submit_functions() method.

        Parameters
        ----------
        settings: list which contains information about the boxes that were ticked by the user,
        if the ''performance matrix' box is ticked, the performance_matrix() method should run.

        image_dirs: list which contains the path to the original input images in the 'images' directory.

        image_ids: list which contains the names of the original input images in the 'images' directory.

        label_dirs: list which contains the path of the csv files in the 'labels' directory.

        IoU: float, IoU threshold value (chosen by the User).

        Returns
        -------
        None

        """
        if settings['Options'][4]:
            if label_dirs:
                TP, FP, FN = 0,0,0
                try:
                    os.mkdir(settings['Output'] + '/' + 'statistics')
                except FileExistsError:
                    tk.messagebox.showerror("Error", "statistics folder already exists")
                for i in range(len(image_ids)):
                    
                    input_csv = os.path.join(label_folder_path, image_ids[i] + '.csv')
                    input_csv = shlex.split(input_csv)[0]
                    #input_csv = input_csv.replace('\ ', ' ')
                    csv_path = settings['Output'] + '/' + 'detections' + '/' + image_ids[i] + '.csv'
                
                    csv_exist = False
                    if os.path.isfile(csv_path):
                        csv_exist = True
                    print(csv_path, label_dirs[i])
                    nTP, nFP, nFN = tripleStatic( 
                             csv_path,
                             input_csv,
                             float(IoU), 
                             csv_exist)
                    TP += nTP
                    FP += nFP
                    FN += nFN
                output_path = os.path.join(settings['Output'] + '/' + 'statistics' + '/', 'performance matrix.csv')
                triOut = [[TP, FP, FN]]
                triName=['TP','FP','FN']
                triCsv=pd.DataFrame(columns=triName,data=triOut)
                triCsv.to_csv(output_path, index=False)
                

    def submit_functions(self):
        """
        This method is called when the user clicks on the 'Submit' button.
        
        First, the user is prompted to create an Output Directory (with a user-specified name).
        
        Depending on the Output settings selected by the user (i.e. bounding boxes, etc), different subdirectories 
        are created in the output directory:

        - 'detections/': contains a .csv file for each input image; each csv fils holds a list of all the bounding boxes for the craters in the image, as detected by the CDM.

        - 'images/': this subdirectory can contain three different subdirectories:
            1) 'original images/': the original image files.

            2) 'bounding boxes/': a .png file for each input image that shows the bounding boxes of the craters detected by the CDM.

            3) 'bounding boxes (with ground truth)/': a .png file for each input image that shows the bounding boxes of the craters detected by the CDM in one colour and the ground truth bounding boxes in a different color.

        - 'statistics/': contains a .csv file for each input image that summarises the True Positive, False Positive and False Negative detections in the image.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        
        dir_path = filedialog.askdirectory(initialdir=".", title="Create Output Directory", parent=self.master)
        
        
        
        images_path = self.import_df['folder_path'][0] + '/images/'
        images_path = images_path.replace(' ', '\ ')
        label_folder_path = 0
        if self.label_added:
            label_folder_path = self.import_df['folder_path'][0] + '/labels/'
            label_folder_path = label_folder_path.replace(' ', '\ ')
        
        settings = {
            'Planet': self.planet_selected.get(),
            'IoU': self.IoU_entry.get(),
            'Image_size': self.image_size_entry.get(),
            'Options': self.selected_checkboxes,
            'Output': dir_path,
            'Input_path': images_path,
            'Input_label_path': label_folder_path
        }
        
        
        print('this is what i want')
        print(settings['Input_path'])
        print(settings['Output'])
        
        
        
        '''
        ################################################################    
        ################################################################
        ################################################################
        ################################################################
        ################################################################
        '''
        # Calling the models, with the input images directory
        
        # when its mars images
        
        model = MyModel(model_dir='model')
        
        
        if settings['Planet'] == 'mars': 

            model.get_predicted_labels_for_images(settings['Input_path'], 
                                                settings['Planet'], 
                                                settings['Output'])
        
        # when the input is moon images
        else:
            destination = os.path.join(settings['Output'], 'detections')
            if os.path.exists(destination):
                os.rmdir(destination)
            os.mkdir(destination)
            
            settings['Input_path'] = shlex.split(settings['Input_path'])[0]
            #settings['Input_path'] = settings['Input_path'].replace('\ ', ' ')
            crop(settings['Input_path'], float(settings['Image_size']))
            
            for subdir, dirs, files in os.walk('cropped'):
                for dir in dirs:
                    sub_path = os.path.join(subdir, dir)
                    for sub_subdir, sub_dirs, sub_files in os.walk(sub_path):
                        for sub_dir in sub_dirs:
                            sub_sub_path = os.path.join(sub_subdir, sub_dir)
                            model.get_predicted_labels_for_images(sub_sub_path, settings['Planet'], output=False)
                       
                       
            final_csv_output_path = os.path.join(settings['Output'], 'detections')
            for subfolder in os.listdir('cropped'):
                subfolder_path = os.path.join('cropped', subfolder)
                if os.path.isdir(subfolder_path):
                    print('################################################################')
                    print(subfolder_path)
                    print(final_csv_output_path)
                    print('################################################################')
                    
                    output_combined_csv(subfolder_path, final_csv_output_path)
                    



        # where there are location information for each input image
        if self.location_added: 
            add_loc_all_detected_csv(os.path.join(settings['Output'], 'detections'), 
                                     self.images_folder, 
                                     self.locations_folder,
                                     float(settings['Image_size']),
                                     settings['Planet'])
            print('heall yeah################################################################')
            
        
        '''
        ################################################################    
        ################################################################
        ################################################################
        ################################################################
        ################################################################
        '''
        
        # getting path information (for the images and labels) located in the self.import_df attribute
        image_dirs = self.import_df['path'].values.tolist()
        image_ids = (self.import_df['name'].map(lambda x: x.split(".")[0])).values.tolist()
        label_dirs = 0
        if self.label_added:
            label_dirs = self.import_df['labels'].values.tolist()
            
            
        try:
            os.mkdir(settings['Output'] + '/' + 'images')
        except FileExistsError:
            tk.messagebox.showerror("Error", "images folder already exists")

        # filling subdirectories
        self.original_images(settings, images_path)
        self.bounding_boxes(settings, image_dirs, image_ids)
        self.gd_truth_bounding_boxes(settings, image_dirs, image_ids, label_dirs, label_folder_path)
        self.plot_sf_distribution(settings, image_dirs, image_ids, self.label_added)
        self.performance_matrix(settings, image_ids, label_dirs, settings['IoU'], label_folder_path)

        tk.messagebox.showinfo("Success",  "Successfully exported!")    


def main(): 
    root = tk.Tk()
    root.title("Crater Detection Model (CDM)")
    #root.geometry('500x500')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
