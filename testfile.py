import numpy as np
import gui_helper
from convert_tool import convert_function
from gui_helper import *
from statistic import *

H = 27291
W = 54582
x = 2048
n = 89
x1 = 0.053192
y1 = 0.628065
w1 = 0.519336
h1 = 0.486487




def test_convert():
    res1 = convert_function(W,H,x,n,x1,y1,w1,h1)
    value1 = (0.2646465357810267, 0.27226107947675054, 0.019486279872485437, 0.036507470448133086)
    """Test the function"""
    assert np.isclose(value1, res1).all()
    


def test_gui_helper():
    dummy = ['.DS_Store', '.DS_Store', '.DS_Store', 'aeolis_42_0.csv', 
             'aeolis_42_5.csv', '.DS_Store', 'aeolis_35_0.csv', 
             'aeolis_40_1.csv', '.DS_Store', 'aeolis_30_6.csv', 'aeolis_30_6.csv']
    res = remove_ds_store(dummy)
    goal = ['aeolis_42_0.csv', 'aeolis_42_5.csv', 'aeolis_35_0.csv',
            'aeolis_40_1.csv', 'aeolis_30_6.csv', 'aeolis_30_6.csv']
    
    assert np.compare_chararrays(res,goal,'==',rstrip = True).all()

def test_check_image_folder():
    a = check_image_folder('Archive/data')
    print('Test for test for check_image_folder starts','\n')
    print(a,'\n','Test terminated.')
    
    return 0
test_check_image_folder()

def test_check_image_folder():
    a1,b1,c1,d1 = 0.8557692307692307,0.48677884615384615,0.1201923076923077,0.12259615384615384
    a2,b2,c2,d2 = 0.9423076923076923,0.7584134615384616,0.08173076923076923,0.07932692307692307
    res = iouCal(a1,b1,a2,b2,c1,d1,c2,d2)
    goal1 = 0
    assert np.isclose(res, goal1).all()
    
    a1,b1,c1,d1 = 0.7175480769230769,0.6225961538461539,0.06009615384615385,0.057692307692307696
    a2,b2,c2,d2 = 0.7236538461538461,0.624,0.078461538461538464,0.038461538461538464
    
    res2 = iouCal(a1,b1,a2,b2,c1,d1,c2,d2)
    goal2 = 0.8337628845764702
    assert np.isclose(goal2, res2).all()

def test_tripleStatic():
    bbpath = 'Archive/test export folder/detections/test1.csv'
    tbpath = 'Archive/test export folder/detections/test4.csv'
    res = tripleStatic(bbpath, tbpath, threshold=0.5)
    goal = (0, 5, 3)
    assert np.isclose(res, goal).all()
    
def test_count_files():
    res = gui_helper.count_files('Archive/data')
    goal = 12
    assert np.isclose(res, goal).all()


def test_ends_with_csv():
    res1 = gui_helper.ends_with_csv('Archive/data/images') 
    assert res1
    


def test_check_file_names():
    res1 = gui_helper.check_file_names('Archive/data/images', 'Archive/data/labels')
    # res2 = gui_helper.check_file_names('Archive/data', 'Archive/data/labels')
    assert res1 
    


def test_check_label_folder():
    res1 = gui_helper.check_label_folder('Archive/data/images', 'Archive/data/images')
    goal1 = ('labels', ['Archive/data/images/.DS_Store', 'Archive/data/images/test4.png', 'Archive/data/images/test1.png', 'Archive/data/images/test3.png', 'Archive/data/images/test2.png'])
    assert np.compare_chararrays(res1[0],goal1[0],'==',rstrip = True).all()


def test_check_location_folder():
    res1 = gui_helper.check_location_folder('Archive/data/images', 'Archive/data/images') # wrong data type
    goal1 = ('locations', {'latitudes': [], 'longitudes': []})
    assert np.compare_chararrays(res1[0],goal1[0],'==',rstrip = True).all()


    


    
    

