#import sys
import os


def check_image_folder(image_folder):
    """Checks that the input folder contains the images subdirectory.
    Checks that the images are of an appropriate format, 
    (accepts only .jpg, .png, .tif)."""

    if not (os.path.exists(image_folder)):
        raise Exception("\n\nThe input folder should contain a subdirectory called images.\n") 

    if os.path.isfile(".DS_Store"):
        os.remove('.DS_Store')

    for file in os.listdir(image_folder):
        if not (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".tif")):
            raise Exception(f"\n\nThe image: '{file}' is of the wrong format.\nPlease change the format of the image or delete the file.\n")


def check_label_folder(image_folder, label_folder):
    """Checks that the optional subirectory 'labels'
    contains a .csv file associated with each image file
    in the subdirectory 'images'."""

    if os.path.exists(label_folder):
        for file in os.listdir(label_folder):
            if not file.endswith(".csv"):
                raise Exception("\n\nThe subdirectory labels should only contain .csv files. Please delete all other files.\n")
        
        image_count = len(os.listdir(image_folder))
        label_count = len(os.listdir(label_folder))
        if image_count != label_count:
            raise Exception("\n\nThe number of images and labels do not match.\n")


def main():
    user_input = input("Enter the path of your file: ")

    image_folder = user_input + "/images"
    label_folder = user_input + "/labels"

    check_image_folder(image_folder)
    check_label_folder(image_folder, label_folder)


main()