"""This module contains helper functions used for the user interface (in the user_int module)."""

import os
import csv


def remove_ds_store(file_list):
    """
        Removes strings that contain the substring '.DS_Store'.

        This function is used in the import_images(), import_locations(), and import_labels() methods 
        (see user_int.py).
        It is also used in the check_file_names(folder_1, folder_2) function below.

        Parameters
        ----------
        file_list : list of strings.

        Returns
        -------
        list: file_list but without the strings which contain the substring '.DS_Store'.

        """
    return [item for item in file_list if '.DS_Store' not in item]


def check_image_folder(image_folder):
    """
        Checks that the 'images' subdirectory exists.
        Checks that the images in the subdirectory are of an appropriate format (accepts only .jpg, .png, .tif).
        If no errors are found, appends the name and path of the images to a dictionary, and returns the dictionary.

        This function is used in the import_images() method (see user_int.py).

        Parameters
        ----------
        image_folder: path to the 'images' folder.

        Returns
        -------
        - A string: if the string "images" is returned, no errors were found; otherwise, the string describes the error.
        - files: dictionary which contains the name and path of the images in the image_folder.
        (Note: the dictionary is empty if an error is found.)

        """

    files = {'name':[], 'path':[]}

    if not (os.path.exists(image_folder)):
        return "The input folder should contain a subdirectory called images.", files

    for file in os.listdir(image_folder):
        if not (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".tif") or file.endswith(".DS_Store")):
            return f"The image: '{file}' is of the wrong format.\nPlease change the format of the image or delete the file.", files
        else:
            files['name'].append(file)
            files['path'].append(image_folder + '/' +  file)

    return "images", files


def count_files(directory, exclude='.DS_Store'):
    """
        Counts files in a directory, but does not count the exclude file (default: .DS_Store files).

        This function is used in check_label_folder(image_folder, label_folder) and in check_location_folder(image_folder, location_folder), below.

        Parameters
        ----------
        directory: the directory which contains the files to be counted.
        exclude: the file name to exclude from the count.

        Returns
        -------
        count: the number of files in the directory.

        """
    
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != exclude:
                count += 1
    return count


def ends_with_csv(folder):
    """
        Checks that a directory only contains .csv files (it overlooks .DS_Store files).

        This function is used in check_label_folder(image_folder, label_folder) and check_location_folder(image_folder, location_folder), below.

        Parameters
        ----------
        folder: path to the directory.

        Returns
        -------
        - Boolean: True if the folder only contains .csv (or .DS_Store files)

        """

    for file in os.listdir(folder):
        if not (file.endswith(".csv") or file.endswith(".DS_Store")):
            return False
        else:
            return True


def check_file_names(folder_1, folder_2):
    """
        Checks that two directores have matching file names (excludes the file extensions).

        This function is used in check_label_folder(image_folder, label_folder) and check_location_folder(image_folder, location_folder), below.

        Parameters
        ----------
        folder_1: path to the first directory.
        folder_2: path to the second directory.

        Returns
        -------
        - Boolean: True if the directories contains files with matching names. 

        """

    files_1 = remove_ds_store(list(os.path.splitext(f)[0] for f in os.listdir(folder_1)))
    files_2 = remove_ds_store(list(os.path.splitext(f)[0] for f in os.listdir(folder_2)))

    if set(files_1) != set(files_2):
        return False
    else:
        return True


def check_label_folder(image_folder, label_folder):
    """
        Checks that the label_folder only contains csv files.
        Checks that the label_folder contains a .csv file associated with each file in the image_folder.
        Checks that the names of the csv files match the names of the images in the image_folder.
        If no errors are found, appends the path of the csv files from the label_folder to a list and returns the list.

        This function is used in the import_labels() method (see user_int.py).

        Parameters
        ----------
        image_folder: path to the 'images' folder.
        label_folder: path to the 'labels' folder.

        Returns
        -------
        - A string: if the string "labels" is returned, no errors were found; otherwise, the string describes the error.
        - files: list which contains the paths to the csv files in the labels_folder.
        (Note: the list is empty if an error is found.)

        """

    files = []

    if not ends_with_csv(label_folder):
        return "The subdirectory labels should only contain .csv files. Please delete all other files.", files

    img_count = count_files(image_folder)
    label_count = count_files(label_folder)

    if img_count != label_count:
        return "The number of images and labels do not match.", files
    
    if not check_file_names(image_folder, label_folder):
        return "File names in the images & labels subdirectories do not match.", files

    for file in os.listdir(label_folder):
        files.append(label_folder + '/' + file)
    
    return "labels", files


def check_location_folder(image_folder, location_folder):
    """ 
        Checks that the location_folder only contains csv files.
        Checks that the location_folder contains a .csv file associated with each file in the image_folder.
        Checks that the names of the csv files match the names of the images in the image_folder.
        Checks that the csv files only contain two values (the latitude and longitude associated with the images in the image_folder).
        
        If no errors are found, appends the latitude and longitude infromation from the csv files to a dictionary, and returns the dictionary.

        This function is used in the import_locations() method (see user_int.py).

        Parameters
        ----------
        image_folder: path to the 'images' folder.
        location_folder: path to the 'locations' folder.

        Returns
        -------
        - A string: if the string "locations" is returned, no errors were found; otherwise, the string describes the error.
        - files: dictionary which contains the latitude and longitude information from the csv files.
        (Note: the list is empty if an error is found.)
        

        """
    
    files = {'latitudes':[], 'longitudes':[]}

    if not ends_with_csv(location_folder):
        return "The subdirectory locations should only contain .csv files. Please delete all other files.", files

    img_count = count_files(image_folder)
    location_count = count_files(location_folder)

    if img_count != location_count:
        return "The number of images and locations do not match.", files

    if not check_file_names(image_folder, location_folder):
        return "File names in the images & locations subdirectories do not match.", files

    csv_files = [f for f in os.listdir(location_folder) if f.endswith('.csv')]
    for csv_file in csv_files:
        with open(os.path.join(location_folder, csv_file), 'r') as f:
            reader = csv.reader(f)
            csv_values = list(reader)
            if len(csv_values) == 1 and len(csv_values[0]) == 2:
                files['latitudes'].append(csv_values[0][0])
                files['longitudes'].append(csv_values[0][1])
            else:
                return 'The csv file {} has more than two values'.format(csv_file), files

    return "locations", files
