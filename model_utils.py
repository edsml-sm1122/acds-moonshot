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
from matplotlib import pyplot as plt
from PIL import Image, ImageOps
from numpy import asarray
import os
import numpy as np
import shutil
import math
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

    def get_predicted_labels_for_images(self, dir_images, planet, output=False):
      
      if planet == 'mars':
        destination = os.path.join(output, 'detections')
        self.delete_if_exists(path_name = destination)
        self.create_dir(path_name = destination)

        pt = f'weights/{planet}_best.pt'
        
        self.predict(best_w=pt, img_size=416, conf=0.4, dir_predictions=dir_images)       
        basepath = self.get_latest_prediction()
        
        self.convert_txt_to_csv(basepath, destination)    
        
      elif planet == 'moon':
        #process dir_images location to derive image size and location
        loc = dir_images.split('/')[-1]
        print('this is loccccccc locccccccloccccccclocccccccloccccccclocccccccloccccccc')
        print(loc)
        model_type, img_size = loc.split('_')
        print(model_type, img_size)

        destination = f'{dir_images}_detections'

        self.delete_if_exists(path_name = destination)
        self.create_dir(path_name = destination)

        pt = f'weights/{planet}_{model_type}_best.pt'

        self.predict(best_w=pt, img_size=img_size, conf=0.4, dir_predictions=dir_images)
        basepath = self.get_latest_prediction()
        print(destination)
        self.convert_txt_to_csv(basepath, destination)    

      return 0

    def get_latest_prediction(self):
        #combine predictions into 1 csv - get the latest
        paths = sorted(Path(self.model_dir,f'runs/detect/').iterdir(), key=os.path.getmtime)
        latest = paths[-1]
        basepath = os.path.join(latest,'labels')
        print(basepath)
        return basepath

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
  
  
def crop(path,mppix=100,has_mppix = True):
    '''Read the images, crop each images into smaller cells as model inputs. Generally, each large image will be cropped three times with 3 small cell resolution.
    
    Parameters
    ----------
    path : str
        image file path
    mppix : int
        meters per mixel of the user input image.(all the image shall have the same mppix)
    has_mppix : bool
        Whether user has inout the image resolution 
        
    Returns
    -------
    cropped_path : list of str
        A list of path that store the cropped images. The lenth of the image equal to the number of images in 'path'
    '''   
#     os.rmdir('cropped')
    
    if os.path.exists(f'cropped'):
        shutil.rmtree('cropped')
        print('old data deleted')
    
    #read images
    images = []
    Image.MAX_IMAGE_PIXELS = 3723856950
    
    imname = []
    
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            img = Image.open(os.path.join(path,filename))
            img = ImageOps.grayscale(img)
            imname.append(filename[:-4])
            if img is not None:
                images.append(asarray(img))
            print(f'{filename} read')
    
    #crop
    print('start cropping')
    
    for n,i in enumerate(images):
    
        #determine the size of cells
#         plt.imshow(i)
        try:
            x,y = i.shape
        except ValueError:
            print("Oops! Imgae format not supported")

        x,y = x*mppix/1000, y*mppix/1000 # x, y in km

        if x<40 or y<40:
            if has_mppix:
                print('too small image')
                res=[np.array([x,y]).min()]
            else:
                res=[np.array([x,y]).min()]
                mppix=100
         
        elif x< 200 or y<200:
            res = [40]
        elif x< 400 or y<400:
            res = [40,200]   
        else:
            res = [40,200,400]
         
  
        #crop the image into cells and store them (such that the model can read)
        #As there can be many cells, the storage may take long time.
        W,H=i.T.shape[0],i.T.shape[1]
        
        name = ['small','medium','large']
        for j in range(len(res)):
            res[j]=int(res[j]/(mppix/1000))

            if not os.path.exists(f'cropped/{imname[n]}_{W}_{H}/{name[j]}_{res[j]}'):
                os.makedirs(f'cropped/{imname[n]}_{W}_{H}/{name[j]}_{res[j]}')       
            image,index = bigimgpix2cellpix(i,res[j],remain=True)
            for k in range(len(image)):
                image_ = Image.fromarray(image[k])
                image_.save(f'cropped/{imname[n]}_{W}_{H}/{name[j]}_{res[j]}/{k+1}.png')
    
        print(f'figure {n} cropped with size {res}')
    
    return 'cropped'
  
  
  
 
def convert_function(W,H,x,n,x1,y1,w1,h1):
    """
    Given Width(W), Height(H) of the picture, length of the sqaure x
    and the crater position (x1,y1,w1,h1) in small tiles, return position
    and size of crater relative to the input image.

    Parameters
    ----------
    W : Width of input image
    H : Height of input image
    x : length of small tiles
    n : number of picture
    x1, y1, w1, h1 : crater position

    Returns
    -------
    result : array 
        Position and size of crater relative to the input image.


    Examples
    --------
    >>> W = 27291
    >>> H = 54582
    >>> x = 2048
    >>> n = 89
    >>> x1 = 0.053192
    >>> y1 = 0.628065
    >>> w1 = 0.519336
    >>> h1 = 0.486487
    >>> result = convert_function(W,H,x,n,x1,y1,w1,h1)
    >>> result
    (20588.937216, 7430.27712, 1063.600128, 996.325376)
    """
    r = W // x 
    c = H // x
    row = (n-1) // c
    col = n - row*c -1
    x2 = (col*x+x*x1) / W
    y2 = (row*x+x*y1) / H
    w2 = w1*x / W
    h2 = h1*x / H
    
    return (x2,y2,w2,h2)

def output_combined_csv(rootdir,outpath):
    """Convert the data in smaller tiles to data in the full picture

    Args:
        rootdir (string): the directory of input csv
        outpath (string): the directory of output csv

    Returns:
        .csv file
    """
    res = []
    sml = "init"
    sml_now = "initt"
    for root, dirs, files in os.walk(rootdir,topdown=True):
        files.sort()
        dirs.sort()

        for filename in files:
            if filename.__contains__('.DS_Store') == True:
                continue
            if root.__contains__('detections') == False:
                continue
            
            n = int(filename.split('.')[0])
            
            original_image_size = [0.0, 0.0]
            original_image_size[0] = float(root.rsplit("/")[1].rsplit("_")[-2])
            original_image_size[1] = float(root.rsplit("/")[1].rsplit("_")[-1])
            
            
            splited_image_size = float(root.rsplit("/")[2].rsplit("_")[1])
            
            
            
            with open(os.path.join(root, filename)) as f:            
                    for line in f:
                        data = np.array(line.strip().split(','),dtype=float)
                        out = convert_function(original_image_size[0],original_image_size[1],splited_image_size,n,
                                                data[0],data[1],data[2],data[3])
                        res.append(out)

    df = pd.DataFrame(res)
    f_name = rootdir.split("/")[1]
    f_name = '_'.join(f_name.split('_')[:-2]) + ".csv"
    
    filepath = Path(outpath + "/" + f_name)
    df.to_csv(filepath,index=False, header=False) 
    
    return np.array(res)

