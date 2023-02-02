import numpy as np

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
    result : np.array 
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
    array([20588.937216,  7430.27712 ,  1063.600128,   996.325376])
    
    """
    r = W // x 
    c = H // x
    row = (n-1) // c
    col = n - row*c -1
    x2 = (col*x+x*x1)
    y2 = (row*x+x*y1)
    w2 = w1*x
    h2 = h1*x
    
    return np.array([x2,y2,w2,h2])

# run: python convert.py -v 
if __name__ == "__main__":
    import doctest
    doctest.testmod()