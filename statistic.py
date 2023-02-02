import os
from os import listdir
import shutil
import csv

import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw

def iouCal(x1, y1, x2, y2, w1, h1, w2, h2):
    """
    Function to calculate the Intersection over Union index (IoU) 
    for every crater bounding box in your model detection set 
    against every crater in our ground truth crater bounding box list
    
    Parameters
    ----------
    x1, y1, w1, h1 : detected crater position from prediction list
    x2, y2, w2, h2 : bounding box position in the ground truth list 
    
    Returns
    -------
    IoU = Area of Overlap/Area of Union    
    """
    # part of tripleStatic
    if abs(x1-x2) >= ((w1+w2)/2) or abs(y1-y2) >= ((h1+h2)/2):
        return 0
    else: 
        return (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))) / (w1*h1 + w2*h2 - (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))))


def tripleStatic(bbpath, tbpath, threshold=0.5):
    """
    Function to calculate crater recall index, crater precision index,
    and crater F1 score. 
    
    Parameters
    ----------
    bbpath : path for csv file of bounding box position
    tbpath : path for csv file of truth bounding box position
    threshold : Use an IoU threshold of 0.5 to 
                determine whether a detection is 
                successful (True Positive).
    
    Returns
    -------
    TP : True Positive, Detected feature is a real crater 
    FP : False Positive, Detected feature is not a crater
    FN : False Negative, A real crater is undetected   
    
    """
    # output TP-FP-FN csv file to a folder
    crtP = []
    crtT = []

    with open(bbpath) as bboxloc:
        reader = csv.reader(bboxloc)
        for i, rows in enumerate(reader):
            crtP.append([float(rows[0]), float(rows[1]), float(rows[2]), float(rows[3])])

    with open(tbpath) as tboxloc:
        reader = csv.reader(tboxloc)
        for i, rows in enumerate(reader):
            crtT.append([float(rows[0]), float(rows[1]), float(rows[2]), float(rows[3])])
    TP = 0
    FP = 0
    FN = 0
    for i in range(0, len(crtP)):
        temiouPeak = 0
        for o in range(0, len(crtT)):
            temiou = iouCal(crtP[i][0], crtP[i][1], crtT[o][0], crtT[o][1], crtP[i][2], crtP[i][3], crtT[o][2], crtT[o][3])
            if temiou >= temiouPeak:
                temiouPeak = temiou
        if temiouPeak >= threshold:
            TP = TP + 1
        else:
            FP = FP + 1
    FN = len(crtT) - TP

    #triOut = [[TP, FP, FN]]
    #triName=['TP','FP','FN']
    #triCsv=pd.DataFrame(columns=triName,data=triOut)
    #triCsv.to_csv(outpath, index=False)
    return TP, FP, FN

# run: python convert.py -v 
if __name__ == "__main__":
    import doctest
    doctest.testmod()