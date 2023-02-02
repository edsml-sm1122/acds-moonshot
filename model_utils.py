import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import shlex, subprocess
import runpy
import os
from pathlib import Path
from gui_helper import remove_ds_store

from data_manager import DataManager


class MyModel(DataManager):
    def __init__(self,model_dir='yolov5',mymodel='yolov5x', hyps='hyps/moon_hyp_params.yaml',yaml='moon.yaml'):
      self.model_dir = model_dir
      self.model = mymodel
      self.cfg = f'{mymodel}.yaml'
      self.weights = f'{mymodel}.pt'
      self.hyps = hyps
      self.yaml = yaml

    def predict(self, best_w, img_size=416, conf=0.4, dir_predictions='' ):
      self.delete_if_exists(path_name= os.path.join(self.model_dir,'runs','detect','exp'))
      
      command = f"python {self.model_dir}/detect.py --weights {best_w} --img {img_size} --conf {conf} --source {dir_predictions} --save-txt --save-conf"
      print(command)
      args = shlex.split(command)
      try: 
        subprocess.run(args, capture_output=True) 
      except RuntimeError as error: 
        return(error)
      
      return 0

    def plot_test_image(self,img):
      #plot example test image with lable
      
      _ = Image.open(img)
      fig, ax = plt.subplots()
      ax.imshow(_, cmap='gray')

      #load the lable
      lbl = img.replace("images", "labels").replace("png", "txt")
      my_coords = np.genfromtxt(lbl, delimiter=' ')

      w,h = _.size
      if my_coords.ndim == 1:
        rect = patches.Rectangle((my_coords[1]*w-(my_coords[3]*w/2), my_coords[2]*h-(my_coords[4]*h/2)), my_coords[3]*w, my_coords[4]*h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
      else:  
        rect={}
        for i in range(my_coords.shape[0]):
            rect[i] = patches.Rectangle((my_coords[i][1]*w-(my_coords[i][3]*w/2), my_coords[i][2]*h-(my_coords[i][4]*h/2)), my_coords[i][3]*w, my_coords[i][4]*h, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect[i])
      plt.show()
      return

    def plot_train_metircs(self,which_run='yolo_moons5'):
      #results 5x model
      _ = Image.open(os.path.join(which_run, 'results.png', ))
      fig, ax = plt.subplots(figsize=(15, 15))
      ax.imshow(_)

      _ = Image.open(os.path.join(which_run, 'confusion_matrix.png', ))
      fig, ax = plt.subplots(figsize=(15, 15))
      ax.imshow(_)

    def get_predicted_labels_for_images(self, dir_images, planet, output):
   
      self.delete_if_exists(path_name= os.path.join(output, 'detections'))
      self.create_dir(path_name=os.path.join(output, 'detections'))

      if planet == 'mars':
        pt = 'weights/mars_best.pt'
        
        self.predict(best_w=pt, img_size=416, conf=0.4, dir_predictions=dir_images)
        
        paths = sorted(Path(self.model_dir,f'runs/detect/').iterdir(), key=os.path.getmtime)
        latest = paths[-1]
        basepath = os.path.join(latest,'labels')

        for lbl in os.listdir(basepath):
            coords = pd.read_csv (os.path.join(basepath,lbl),header=None,index_col=None, sep = " ")
            coords.drop(columns=coords.columns[-1],  axis=1,  inplace=True)
            coords.drop(columns=coords.columns[0],  axis=1,  inplace=True)
            
            _=os.path.join(output, 'detections',lbl).replace("txt", "csv")
            print(_)
            print(coords)
            coords.to_csv(_,header=None, index=None, sep = ",")     
      
      elif planet == 'moon':
          for size in ['small','medium','large']:
            pt = f'wights/moon_best_{size}.pt'
            self.predict(best_w=pt, img_size=2048, conf=0.4, dir_predictions=dir_images)
      
      return 0

    def get_predicted_images(self,which_run='exp10'):
      return os.path.join(self.model_dir,f'runs/detect/{which_run}/')

    def get_predicted_labels(self,which_run='exp10'):
      return os.path.join(self.model_dir,f'runs/detect/{which_run}/labels/')
    
    
    
def bigimgpix2cellpix(img,res,remain=False): 
    '''Crop image to cells.
    
    Parameters
    ----------
    img : np.array
        cropped image
    res : int
        the size of the cell cropped into (suqare cell)
    remain : bool
        Whether keep the residuals. As the image shape not necessarily times of res.
        
    Returns
    -------
    tiles : list of np.array
        the cells
    indexes: list of tuple
        the (row, col) that each cell lies, relative to the original image.
    '''        
    shape=img.T.shape

    if remain:
         cell_x,cell_y = math.ceil(shape[0]/res) , math.ceil(shape[1]/res) 
    else:
        cell_x,cell_y = shape[0]//res, shape[1]//res
        
    
    indexes = [(i,j) for i in range(0,cell_y * res,res) for j in range(0,cell_x * res,res)]# first rightward, then downward
    tiles = [img[i:i+res,j:j+res] for i in range(0,cell_y * res,res) for j in range(0,cell_x * res,res)]# first rightward, then downward
    
    return tiles,indexes
  
  
