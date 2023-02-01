import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

from data_manager import DataManager

class MyModel(DataManager):
    def __init__(self,model_dir='yolov5',mymodel='yolov5x', hyps='moon_hyp_params.yaml'):
        self.model_dir = model_dir
        self.model = mymodel
        self.cfg = f'{mymodel}.yaml'
        self.weights = f'{mymodel}.pt'
        self.hyps = hyps

    def train(self,img_size=416,batch=32,epochs=100):
        python '{yolo_dir}/train.py' --img 416 --cfg '{self.cfg}' --hyp moon_hyp_params.yaml --batch 32 --epochs 100 --data moon.yaml --weights yolov5x.pt --workers 24 --name yolo_moons

    def predict():
