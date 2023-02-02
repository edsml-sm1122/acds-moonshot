
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


'''
boundBox('/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/images/test_1.png',  #input path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/detections/test_1.csv', #detected label path
         '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/Xenophanes/acds-moonshot-xenophanes/data/test output.jpg')  
comparedBox('/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/images/test_1.png', #input path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/detections/test_1.csv', #detected label path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/data/labels/test_1.csv', #true label path
            '/Users/dl1122/Library/Mobile Documents/com~apple~CloudDocs/Imperical College/Xenophanes/acds-moonshot-xenophanes/data/test output with true.jpg')  
'''

