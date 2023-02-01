import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def plot_test_image(img):
    #plot example test image with lable
    
    _ = Image.open(img)
    fig, ax = plt.subplots()
    ax.imshow(_, cmap='gray')

    #load the lable
    lbl = img.replace("images", "labels").replace("png", "csv")
    my_coords = np.genfromtxt(lbl, delimiter=',')

    w,h = _.size
    if my_coords.ndim == 1:
        rect = patches.Rectangle((my_coords[0]*w-(my_coords[2]*w/2), my_coords[1]*h-(my_coords[3]*h/2)), my_coords[2]*w, my_coords[3]*h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    else:  
        rect={}
    for i in range(my_coords.ndim):
        rect[i] = patches.Rectangle((my_coords[i][0]*w-(my_coords[i][2]*w/2), my_coords[i][1]*h-(my_coords[i][3]*h/2)), my_coords[i][2]*w, my_coords[i][3]*h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect[i])

    plt.show()
