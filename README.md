# Moonshot: Automatic Impact Crater Detection on the Moon

## Project Description:

A software tool for automatically detecting impact craters in images of planetary surfaces (Mars and Moon)
and deriving from this a crater-size frequency distribution that can
be used for dating.

## User Manual:

#### 1) To run the software tool, type the following command in the terminal:

>> python3 user_int.py

A GUI window will appear on the screen. 

#### 2) Click on the 'Import Folder' button and select an input folder location.
The input folder should contain a subdirectory `images/` that contains a single image, or multiple images.
The accepted image formats are: .png, .jpg, .tif.

Optional subdirectories in the input folder:
- `labels/` containing a `.csv` file associated with each image file
  that provides a list of all the ground truth bounding boxes for
  craters in the image (i.e. 0.4266826923076923,0.16346153846153846,0.06971153846153846,0.0673076923076923. The `.csv` files should not contain any headers.
- `locations/` containing a `.csv` file associated with each image file
  that provides location of the image centre in latitude and longitude.
  (i.e. 45.792650,26.826999). The `.csv` files should not contain any headers.

Once the input folder location has been selected, the image names will be listed on the GUI window (see example below). 

<img src=image_1.png width="300"/>

#### 3) Optional:
- Input box 1: Add information about image resolution in metres per pixel (m/px). The default is 100 m/px.
- Input box 2: Add information about IoU threshold. The default is 0.5.

#### 4) Tick the desired output settings. 
Depending on the ticked boxes, the software will output:
- `original_images`: the original image files.
- `bounding_boxes`: a .png file for each input image that shows the bounding boxes of the craters detected by the CDM. 
Note: this option is always ticked and disabled because, by default, the software always outputs a list of all the bounding boxes for craters detected in each image.
- `bounding_boxes (with ground truth)`: a .png file for each input image that shows the bounding boxes of the craters detected by the CDM in one colour and the ground truth bounding boxes in a different color. 
Note: this option can only be selected when ground-truth labels have been provided.
- `size-frequency dist`: a plot for each input image comparing the ground truth bounding boxes and the model detection bounding boxes. 
Note: this option can only be selected when the Moon planet has been selected.
- `performance matrix`: a .csv file for each input image that summarises the True Positive, False Positive and False Negative detections in the image. 
Note: this option can only be selected when ground-truth labels have been provided.

#### 5) Press submit to run the software. 
You will be prompted to create an output Directory (with a user-specified name). The program might take long to run. Be patient. 
A pop-up message will appear when the software tool has finished running.

The output directory will contain up to three subdirectories (depending on the selected output settings):
- A subdirectory `detections/` containing a `.csv` file for each input image that contains a list of all the bounding boxes for craters in
the image as detected by the tool. 
- A subdirectory `images/`, which may contain three different subdirectories:
1) `original images/`
2) `bounding boxes/`
3) `bounding boxes (with ground truth)/`
- A subdirectory `statistics/`, which may contain two different subdirectories:
1) `size-frequency dist`
2) `performance matrix`

Example output directories:
<img src=image_2.png width="300"/>

## Tests:

...

## Team:

...
