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
  # part of tripleStatic
  if abs(x1-x2) >= ((w1+w2)/2) or abs(y1-y2) >= ((h1+h2)/2):
    return 0
  else: 
    return (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))) / (w1*h1 + w2*h2 - (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))))


def tripleStatic(bbpath, tbpath, threshold=0.5, csv_exist = True):
  # output TP-FP-FN csv file to a folder
  crtP = []
  crtT = []
  TP = 0
  FP = 0
  FN = 0
  if csv_exist: 
    with open(bbpath) as bboxloc:
      reader = csv.reader(bboxloc)
      for i, rows in enumerate(reader):
        crtP.append([float(rows[0]), float(rows[1]), float(rows[2]), float(rows[3])])

    with open(tbpath) as tboxloc:
      reader = csv.reader(tboxloc)
      for i, rows in enumerate(reader):
        crtT.append([float(rows[0]), float(rows[1]), float(rows[2]), float(rows[3])])

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



def plot_frequency_distribution(imgpath, bbpath, R, image_scale, outpath, tbpath = 'None'):   
    df = pd.read_csv(bbpath, header = None)
    rawimg = Image.open(imgpath)
    w,h = rawimg.size
    values = (df[[2, 3]].max(axis=1))*w*(image_scale/1000)

    hist, bins = np.histogram(values, bins=70)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    plt.xlabel("Crater Size (km)")
    plt.ylabel("Frequency")
    plt.title("Size-Frequency Distribution of Craters")
    label1=plt.plot(bin_centers,hist,'r--',label='Detections')


    plt.loglog(bin_centers, hist, 'r^-', markersize=10, markeredgecolor='r')
    if tbpath != 'None':   
      df2 = pd.read_csv(tbpath, header = None)
      values2 = (df2[[2, 3]].max(axis=1))*w*(image_scale/1000)
      hist2, bins2 = np.histogram(values2, bins=70)
      bin_centers2 = (bins2[:-1] + bins2[1:]) / 2
      plt.loglog(bin_centers2, hist2, 'bo-', markersize=7, markeredgecolor='b')
      label2=plt.plot(bin_centers2,hist2,'b--',label='True labels')

    
    plt.legend()
    plt.savefig(outpath)

