import os
from os import listdir
import shutil
import csv
import random
from sklearn.model_selection import train_test_split

class DataManager:
  def __init__(self, root_dir, data_dir='data', data_key={'i':'images','l':'labels'} ,dataset_dir = 'dataset'):
    self.root_dir    = root_dir
    self.model_dir   = os.path.join(self.root_dir, model_dir)
    self.data_dir    = os.path.join(self.root_dir, data_dir)
    self.data_key    = data_key
    self.dataset_dir = os.path.join(self.root_dir, dataset_dir)

    #placeholders
    self.leaves = None
    self.model_dirs = None

  def construct_dataset_tree(self, delete = True, 
                                   leaves=['images','labels'], 
                                   model_dirs = ['train','val', 'test'], 
                                   predictions=False):
    
    #set the structure for future use
    self.leaves = leaves
    self.model_dirs = model_dirs

    #if path already exists and delete flag is set to True - clean up
    if delete: 
      try:
        self.delete_if_exists(self.dataset_dir)
      except OSError as error:
        return(error)

    #construct the dataset path
    for _ in leaves:
      try: 
        os.mkdir(os.path.join(self.dataset_dir, _)) 
      except OSError as error: 
        return(error)
      for __ in model_dirs:
        try: 
          os.mkdir(os.path.join(self.dataset_dir, _, __))  
        except OSError as error: 
          return(error) 

    #construct separate predictions path based on the root directory. 
    #Therefore to create inference dir inside dataset dir - use 'datasest/inference' 
    if predictions:
      try: 
        os.mkdir(os.path.join(self.root_dir, predictions))  
        self.predictions=predictions
      except OSError as error: 
        return(error) 

    return 0
    
  def delete_if_exists(self, path_name):
    if os.path.exists(path_name):
      if os.isdir(path_name):
        try: 
          shutil.rmtree(path_name)
        except OSError as error: 
          return(error)  
      else:
        try: 
          os.remove(path_name)
        except OSError as error: 
          return(error)
    return 0

  def convert_csv_to_txt(self):

    # we need to convert csv to txt for lables
    for _ in self.model_dirs:
      __ = os.path.join(self.dataset_dir,self.leaves[1],_)
      for i in os.listdir(__):
        csv_file = os.path.join(__,i)
        txt_file = os.path.join(__,i).replace('csv','txt') 
        print((f'Converting: {csv_file} to {txt_file}'))
        if os.path.exists(txt_file):
          os.remove(txt_file)
        with open(txt_file, "w") as my_output_file:
            with open(csv_file, "r") as my_input_file:
                [ my_output_file.write("0 "+" ".join(row)+'\n') for row in csv.reader(my_input_file)] 
            my_output_file.close()
        os.remove(csv_file)


  def split_for_model(self, model_chunks={'train':0.7,'val':0.2,'test':0.1}):

    if(self.model_dirs.size!=model_chunks.size):
       raise Exception(f"Dataset folders don't match requested split {self.model_dirs} vs {model_chunks}")
    elif(self.data_key.size, self.leaves.size):
      raise Exception(f"Dataset leaves don't match in size {self.data_key} vs {self.leaves}")
    else:
      #splitting the dataset
      random.seed(41)

      # Read images and labels - this is vital - we assume data folder has 
      images = os.listdir(os.path.join(self.data_dir,self.data_key['i'])) 
      labels = os.listdir(os.path.join(self.data_dir,self.data_key['l']))
      images.sort()
      labels.sort()

      # Split the dataset into train-valid-test splits 
      train_images, val_images, train_labels, val_labels = train_test_split(images, labels, train_size = model_chunks['train'], random_state = 1)
      val_images, test_images, val_labels, test_labels = train_test_split(val_images, val_labels, train_size = model_chunks['val'], random_state = 1)

      for _ in self.model_dirs:
        for _o, _d in zip(self.data_key, self.leaves):
          
          print(globals()[f"{_}_{_o}"])
          
          for i in globals()[f"{_}_{_o}"]:  
            origin = os.path.join(self.data_dir,_o,i)
            dest = os.path.join(self.dataset_dir,_d,_,i)
            
            print((f'Copying: {origin} to {dest}'))   
            try: 
              shutil.copyfile(origin, dest)
            except OSError as error: 
              return(error)
            
      return 0


