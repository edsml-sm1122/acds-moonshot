import os
import csv

def count_files(directory, exclude='.DS_Store'):
    """Counts files in directory, but excludes the .DS_Store files."""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != exclude:
                count += 1
    return count

def check_image_folder(image_folder):
    """Checks that the input folder contains the images subdirectory.
    Checks that the images are of an appropriate format, 
    (accepts only .jpg, .png, .tif)."""

    if not (os.path.exists(image_folder)):
        return "\n\nThe input folder should contain a subdirectory called images.\n"
    
    if os.path.isfile(".DS_Store"):
        os.remove('.DS_Store')

    for file in os.listdir(image_folder):
        if not (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".tif") or file.endswith(".DS_Store")):
            return f"\n\nThe image: '{file}' is of the wrong format.\nPlease change the format of the image or delete the file.\n"
    
    return "images"


def check_label_folder(image_folder, label_folder):
    """Checks that the optional subirectory 'labels'
    contains a .csv file associated with each image file
    in the subdirectory 'images'."""

    for file in os.listdir(label_folder):
        if not (file.endswith(".csv") or file.endswith(".DS_Store")):
            return "\n\nThe subdirectory labels should only contain .csv files. Please delete all other files.\n"

    img_count = count_files(image_folder)
    label_count = count_files(label_folder)

    if img_count != label_count:
        return "\n\nThe number of images and labels do not match.\n"
    
    return "labels"


def check_location_folder(location_folder):

    if os.path.exists(location_folder):
        # Get all the csv files in the folder
        csv_files = [f for f in os.listdir(location_folder) if f.endswith('.csv')]
        # Create a list to store the values
        values = []
        # Iterate through each csv file
        for csv_file in csv_files:
            # Open the csv file and read its content
            with open(os.path.join(location_folder, csv_file), 'r') as f:
                reader = csv.reader(f)
                # Convert the reader object to a list
                csv_values = list(reader)
                # Check if the csv file has only two values
                if len(csv_values) == 1 and len(csv_values[0]) == 2:
                    # Add the values to the list
                    values.append(csv_values[0])
                else:
                    return 'The csv file {} has more than two values'.format(csv_file)
                    # Show an error message if the csv file has more than two values
                    #tk.messagebox.showerror('Error', 'The csv file {} has more than two values'.format(csv_file))

        return "locations", values

def main():
    user_input = input("Enter the path of your file: ")

    image_folder = user_input + "/images"
    label_folder = user_input + "/labels"

    check_image_folder(image_folder)
    check_label_folder(image_folder, label_folder)


