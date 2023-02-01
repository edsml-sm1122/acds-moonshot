import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import subprocess
import os


from data_manager import DataManager


class MyModel(DataManager):
    def __init__(self,model_dir='yolov5',mymodel='yolov5x', hyps='moon_hyp_params.yaml',yaml='moon.yaml'):
        self.model_dir = model_dir
        self.model = mymodel
        self.cfg = f'{mymodel}.yaml'
        self.weights = f'{mymodel}.pt'
        self.hyps = hyps
        self.yaml = yaml

    def train(self, mymodel_name,img_size=416,batch=32,epochs=100,workers=24):
        command = f"python '{self.yolo_dir}/train.py' --img {img_size} --cfg '{self.cfg}' --hyp {self.hyps} --batch {batch} --epochs {epochs} --data {self.yaml} --weights {self.weights} --workers {workers} --name {mymodel_name}"

        result = subprocess.run([command], capture_output=True)
        print(result.stdout)  
        return 0          
        
    def predict(self,img_size=416,conf=0.4,best_w='/runs/train/yolo_moons5/weights/best.pt'):
        command = f"python '{self.yolo_dir}/detect.py' --weights '{self.yolo}/{best_w}' --img {img_size} --conf {conf} --source {self.predictions} --save-txt --save-conf"
        
        #findout which run it is and return it
        return 'yolo_moons5'

    def plot_train_metircs(self,which_run='yolo_moons5'):
        #results 5x model
        img = f'/yolov5/runs/train/{which_run}'
        _ = Image.open(os.path.join(img, 'results.png', ))
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.imshow(_)

        _ = Image.open(os.path.join(img, 'confusion_matrix.png', ))
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.imshow(_)

    def get_predicted_images(self,which_run='exp10'):
        return os.path.join(self.model_dir,f'runs/detect/{which_run}/')

    def get_predicted_labels(self,which_run='exp10'):
        return os.path.join(self.model_dir,f'runs/detect/{which_run}/labels/')