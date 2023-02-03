import numpy as np
import pandas as pd
from pathlib import Path  
import os

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
    x2 = (col*x+x*x1)
    y2 = (row*x+x*y1)
    w2 = w1*x
    h2 = h1*x
    
    return (x2,y2,w2,h2)

def output(rootdir,outpath):
    """Convert the data in smaller tiles to data in the full picture

    Args:
        rootdir (string): the directory of input csv
        outpath (string): the directory of output csv

    Returns:
        .csv file
    """
    res = []
    n = 0
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
            
            if n == 0:
                sml = root.rsplit("/")[2].rsplit("_")[0]
                
            sml_now = root.rsplit("/")[2].rsplit("_")[0]
            if sml != sml_now:
                n = 1
            else:
                n += 1
            
            # print(root)
            # print(sml)
            # print(sml_now)
            # print(n)
            
            sml = sml_now
            
            original_image_size = [0.0, 0.0]
            original_image_size[0] = float(root.rsplit("/")[1].rsplit("_")[2])
            original_image_size[1] = float(root.rsplit("/")[1].rsplit("_")[3])
            #print(original_image_size)
            
            splited_image_size = float(root.rsplit("/")[2].rsplit("_")[1])
            #print(splited_image_size)
            
            with open(os.path.join(root, filename)) as f:            
                    for line in f:
                        data = np.array(line.strip().split(','),dtype=float)
                        out = convert_function(original_image_size[0],original_image_size[1],splited_image_size,n,
                                                data[0],data[1],data[2],data[3])
                        res.append(out)
                        #print(root)

    df = pd.DataFrame(res)
    f_name = rootdir.split("/")[1].split("_")[0] + ".csv"
    # np.savetxt(f_name, res, delimiter=",")
    filepath = Path(outpath + "/" + f_name)
    df.to_csv(filepath,index=False, header=False) 
    
    return np.array(res)

# run: python convert.py -v 
if __name__ == "__main__":
    import doctest
    doctest.testmod()