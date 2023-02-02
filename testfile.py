import numpy as np

from convert import convert_function
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

H_ = 27291
W_ = 54582
x_ = 256
n_ = 9163
x1_ = 0.527457
y1_ = 0.033216
w1_ = 0.395133
h1_ = 0.390618


def test_convert():
    res1 = convert_function(H,W,x,n,x1,y1,w1,h1)
    value1 = np.array([20588.937216, 7430.27712, 1063.600128, 996.325376])
    """Test the function"""
    assert np.isclose(value1, res1).all()
    
    res2 = convert_function(H_,W_,x_,n_,x1_,y1_,w1_,h1_)
    value2 = np.array([903.028992, 11016.503296, 101.154048, 99.998208])
    assert np.isclose(value2, res2).all()


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

    


    
    

