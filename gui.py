import os
import csv
import pandas as pd

def count_files(directory, exclude='.DS_Store'):
    """Counts files in directory, but excludes the .DS_Store files."""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != exclude:
                count += 1
    return count


def remove_ds_store(file_list):
    return [item for item in file_list if '.DS_Store' not in item]


def check_image_folder(image_folder):
    """Checks that the input folder contains the images subdirectory.
    Checks that the images are of an appropriate format, 
    (accepts only .jpg, .png, .tif)."""

    files = {'name':[], 'path':[]}

    if not (os.path.exists(image_folder)):
        return "\n\nThe input folder should contain a subdirectory called images.\n", files

    for file in os.listdir(image_folder):
        if not (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".tif") or file.endswith(".DS_Store")):
            return f"\n\nThe image: '{file}' is of the wrong format.\nPlease change the format of the image or delete the file.\n", files
        else:
            files['name'].append(file)
            files['path'].append(image_folder + '/' +  file)

    return "images", files


def check_label_folder(image_folder, label_folder):
    """Checks that the optional subirectory 'labels'
    contains a .csv file associated with each image file
    in the subdirectory 'images'."""

    files = []

    for file in os.listdir(label_folder):
        if not (file.endswith(".csv") or file.endswith(".DS_Store")):
            return "\n\nThe subdirectory labels should only contain .csv files. Please delete all other files.\n", files
        else:
            files.append(label_folder + '/' + file)

    img_count = count_files(image_folder)
    label_count = count_files(label_folder)

    if img_count != label_count:
        return "\n\nThe number of images and labels do not match.\n", files
    
    images_files = set(os.path.splitext(f)[0] for f in os.listdir(image_folder))
    labels_files = set(os.path.splitext(f)[0] for f in os.listdir(label_folder))

    if images_files != labels_files:
        return "File names in the images & labels subdirectories do not match.", files
    
    return "labels", files


def check_location_folder(location_folder):

    if os.path.exists(location_folder):
        csv_files = [f for f in os.listdir(location_folder) if f.endswith('.csv')]

        files = {'latitudes':[], 'longitudes':[]}

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

def main():
    user_input = input("Enter the path of your file: ")

    image_folder = user_input + "/images"
    label_folder = user_input + "/labels"

    check_image_folder(image_folder)
    check_label_folder(image_folder, label_folder)

