
from os import listdir

import csv

import random

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw



def atomBound(imgpath, bbpath, csv_exist=True):
  # output rected img to a folder
  rawimg = Image.open(imgpath)
  rawimg = rawimg.convert("RGB")
  postimg = ImageDraw.ImageDraw(rawimg)
  w,h = rawimg.size
  
  if csv_exist == True:
    with open(bbpath) as bboxloc:
      reader = csv.reader(bboxloc)
      for i, rows in enumerate(reader):
          postimg.rectangle(((float(rows[0])*w - float(rows[2])*w/2, float(rows[1])*h - 
                                        float(rows[3])*h/2), (float(rows[0])*w + float(rows[2])*w/2, float(rows[1])*h + float(rows[3])*h/2)), fill=None, outline='red', width=1)
    
  return rawimg, postimg


def boundBox(imgpath, bbpath, outpath, csv_exist):
  rawimg, postimg = atomBound(imgpath, bbpath, csv_exist)
  rawimg.save(outpath)
  #display(rawimg)


def comparedBox(imgpath, bbpath, tbpath, outpath, csv_exist):
  # output rected img to a folder
  rawimg, postimg = atomBound(imgpath, bbpath, csv_exist)
  w,h = rawimg.size 
  
  print('tbpath================================================================')
  print(tbpath)
  with open(tbpath) as tboxloc:
    reader = csv.reader(tboxloc)
    for i, rows in enumerate(reader):
        postimg.rectangle(((float(rows[0])*w - float(rows[2])*w/2, float(rows[1])*h - 
                                       float(rows[3])*h/2), (float(rows[0])*w + float(rows[2])*w/2, float(rows[1])*h + float(rows[3])*h/2)), fill=None, outline='blue', width=1)
  rawimg.save(outpath)
  #display(rawimg)



# boundBox('/Users/dl1122/Downloads/evaluation_dataset/moon/images/Lunar_test_B.jpg',  #input path
#           '/Users/dl1122/Desktop/final moon/detections/Lunar_test_B.csv',
#          '/Users/dl1122/Desktop/final moon/images/bounding boxes/Lunar_test_B.jpg',
#          csv_exist = True)  

'''
comparedBox('/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/images/test_1.png', #input path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/detections/test_1.csv', #detected label path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/labels/test_1.csv', #true label path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/Xenophanes/acds-moonshot-xenophanes/data/test output with true.jpg')  
'''



def to_coords(imgpath, lat, lon, bbpath, R, image_scale):
    '''
    Converts coordinates from the format [0,1] to latitude and longitude for a given 
    location at the centre of the image.
    
    Parameters
    -------------
    x: x coordinate for crater location in [0,1]
    y: y coordinate for crater location in [0,1]
    w: width of the rectangle fitting around the crater in [0,1]
    h: height of the rectangle fitting around the crater in [0,1]
    lat_centre: latitude of the location at the centre of the image
    lon_centre: longitude of the location at the centre of the image
    lat_range: height of the image in degrees latitude
    lon_range: width of the image in degrees longitude
    
    Returns
    --------------
    Coordinates x, y of the crater location in longitude and latitude 
    Width w and height h of the rectangle fitting around the crater in degrees latitude and longitude

    This function is called in ...
    
    '''

      
    crtP = []
    rawimg = Image.open(imgpath)
    imgW,imgH = rawimg.size

    with open(bbpath) as bboxloc:
      reader = csv.reader(bboxloc)
      for i, rows in enumerate(reader):
        crtP.append(rows[:4])
        crtP[i] += ([float(rows[0])*imgW*image_scale/(1000 * R) + lon, lat - float(rows[1])*imgH*image_scale/(1000 * R) , (max(float(rows[2])*imgW, float(rows[3])*imgH)*(image_scale / 1000))])

    with open(bbpath, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(crtP)
      
      
      
import shlex
import os


imgs_path = '/Users/dl1122/Downloads/Archive/data/images'

bbspath = '/Users/dl1122/Downloads/Archive/test\ export\ folder/detections'
bbspath = shlex.split(bbspath)[0]


loc_path = '/Users/dl1122/Downloads/Archive/data/locations'




def add_loc_all_detected_csv(bbspath,imgs_path,loc_path,image_scale = 100, planet = 'mars'):
  
  if planet == 'mars':
    R = 3389.5
  else:
    R = 1737.4
  
  # get a list of files in the directory
  detected_files = os.listdir(bbspath)
  # iterate through each file
  for each_csv in detected_files:
      # get the full path of the file
      file_path = os.path.join(bbspath, each_csv)
      # check if the path is a file
      if os.path.isfile(file_path) and each_csv.endswith(".csv"):
        image_title = os.path.splitext(each_csv)[0]
        
        #location file path
        loc_file_path = os.path.join(loc_path, image_title +'.csv')

        #image file path
        for file in os.listdir(imgs_path):
          if file.startswith(image_title) and (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".tif")):
              img_file_path = os.path.join(imgs_path, file)                             

        with open(loc_file_path, 'r') as file:
          reader = csv.reader(file)
          for row in reader:
              latitude = float(row[0])
              longitude = float(row[1])
        to_coords(img_file_path, latitude, longitude, file_path,100,R)
        
        
#add_loc_all_detected_csv(bbspath, imgs_path, loc_path)
              
        
        




