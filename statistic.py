"""This module is used to calculate the IoU of our detections. It is also used to calculate the True Positive, False Negative and False Positive values."""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def iouCal(x1, y1, x2, y2, w1, h1, w2, h2):
  """
        Calculates the IoU.

        Parameters
        ----------
        x1: float, x coordinate of the centre of the detected bounded box.
        y1: float, y coordinate of the centre of the detected bounded box.
        x2: float, x coordinate of the centre of the ground truth bounded box.
        y2: float, y coordinate of the centre of the ground truth bounded box.
        w1: float, width of the detected bounded box.
        h1: float, height of the detected bounded box.
        w2: float, width of the ground truth bounded box.
        h2: float, height of the ground truth bounded box.

        Returns
        -------
        IoU score.

        """
  # part of tripleStatic
  if abs(x1-x2) >= ((w1+w2)/2) or abs(y1-y2) >= ((h1+h2)/2):
    return 0

  else: 
    return (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))) / (w1*h1 + w2*h2 - (((w1+w2)/2 - abs(x1-x2)) * ((h1+h2)/2 - abs(y1-y2))))


def tripleStatic(bbpath, tbpath, threshold=0.5, csv_exist = True):
  """
        Calculates the TP, FN and FP.

        Parameters
        ----------
        bbpath: str, path to csv file generated by the model containing information about detected bounded boxes.
        tbpath: str, path to csv file containing ground truth bounded boxes information.
        threshold: float, IoU threshold, default = 0.5.
        csv_exist: Boolean, True if bbpath exists (False if the model does not detect any craters).

        Returns
        -------
        TP: int, True Positive value
        FP: int, False Positive value
        FN:, int, False Negative value

        """

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

  return TP, FP, FN



def plot_frequency_distribution(imgpath, bbpath, R, image_scale, outpath, tbpath = 'None'):   

    """
        Plots the frequency distribution (the plot is saved to a directory).

        Parameters
        ----------
        imgpath: str, path to input images.
        bbpath: str, path to csv file generated by the model containing information about detected bounded boxes.
        R: float, planet radius (not used because we are only plotting for the planet Moon).
        image_scale: float, image resolution (m/px)
        outpath: str, path to png output images.
        tbpath: str, path to csv file containing ground truth bounded boxes information (default is "None")
        
        Returns
        -------
        None

        """

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

