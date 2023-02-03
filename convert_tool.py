"""This module is used calculate coordinates"""

import numpy as np
import pandas as pd
from pathlib import Path  
import os
import math

def convert_function(W,H,res,n,x,y,w,h):
    
    """
    Given Width(W), Height(H) of the picture, length of the square x
    and the crater position (x1,y1,w1,h1) in small tiles, return position
    and size of crater relative to the input image.
    Parameters
    ----------
    W : Width of input image
    H : Height of input image
    res : length of small tiles
    n : number of picture
    x1, y1, w1, h1 : crater position
    Returns
    -------
    result : array 
        Position and size of crater relative to the input image.
    """
    num_x = math.ceil(W/res)
    num_y = math.ceil(H/res)
    
    row = math.ceil(n/num_x)
    col = n - (row-1)*num_x

    
    if col == num_x:
        X2 = (res*(col-1) + x*(W-res*(col-1)))/H
        W2 = ((W-res*(col-1))*w)/W
        
    else:
        X2 = (res*(col-1)+x*res)/W
        W2 = res*w/W
        
    if row == num_y:
        Y2 = (res*(row-1)+y*(H-res*(row-1)))/H
        H2 = (H-res*(row-1))*h/H
        
    else:
        Y2 = (res*(row-1) + y*res)/H
        H2 = res*h/H
        
    # print(num_x,num_y,row,col)
    return (X2,Y2,W2,H2)

def output_function(rootdir,outpath):
    """Convert the data in smaller tiles to data in the full picture

    Args:
        rootdir (string): the directory of input csv
        outpath (string): the directory of output csv

    Returns:
        .csv file
    """
    res = []
    for root, dirs, files in os.walk(rootdir,topdown=True):
        files.sort()
        dirs.sort()

        for filename in files:
            if filename.__contains__('.DS_Store') == True:
                continue
            if root.__contains__('detections') == False:
                continue
            
            # print(filename)
            n = int(filename.split('.')[0])    
            original_image_size = [0.0, 0.0]
            original_image_size[0] = float(root.rsplit("/")[0].rsplit("_")[-2])
            original_image_size[1] = float(root.rsplit("/")[0].rsplit("_")[-1])
            # print(root)
            # print(original_image_size)

            # print(n)
            # print(original_image_size)
            
            # print(root.rsplit("/")[-1])
            splited_image_size = float(root.rsplit("/")[-1].rsplit("_")[1])
            # print(splited_image_size)
            
            n_row = original_image_size[1]//splited_image_size+1 # lie you ji ge
            row_left = original_image_size[1]%splited_image_size
            
            n_col = original_image_size[0]//splited_image_size+1
            col_left = original_image_size[0]%splited_image_size
            
            right_rem = n%n_col == 0
            bottom_rem = (n_row-1)*n_row < n <= n_col*n_row
            if n%n_col == 0 & bottom_rem:
                splited_image_size_x = col_left
                splited_image_size_y = row_left
            elif n%n_col == 0:
                splited_image_size_x = col_left
                splited_image_size_y = splited_image_size
            elif bottom_rem:
                splited_image_size_x = splited_image_size
                splited_image_size_y = row_left
            else:
                splited_image_size_x = splited_image_size
                splited_image_size_y = splited_image_size

            
            with open(os.path.join(root, filename)) as f:            
                    for line in f:
                        data = np.array(line.strip().split(','),dtype=float)
                        # out = convert_function(original_image_size[0],original_image_size[1],
                        #                        splited_image_size_x,splited_image_size_y,n,
                        #                        data[0],data[1],data[2],data[3])
                        # print(original_image_size[0])
                        out = convert_function(original_image_size[0],original_image_size[1],
                                               splited_image_size,n,
                                               data[0],data[1],data[2],data[3])
                        res.append(out)

    df = pd.DataFrame(res)
    
    f_name = rootdir
    # f_name = rootdir.split("/")[1]
    f_name = '_'.join(f_name.split('_')[:-2]) + ".csv"
     #print(f_name)
    
    filepath = Path(outpath + "/" + f_name)
    df.to_csv(filepath,index=False, header=False) 
    
    return np.array(res)

# run: python convert_tool.py -v 
if __name__ == "__main__":
    import doctest
    doctest.testmod()
