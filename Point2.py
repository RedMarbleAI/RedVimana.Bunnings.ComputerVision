import math

from Point3 import *

class Point2(object):
    def __init__(this, x, y):
        this.mX = x
        this.mY = y

    def __len__(this):
        return 2

    def __getitem__(this, key):
        if key is 0:
            return this.X
        elif key is 1:
            return this.Y
        else:
            raise ValueError("Key must be a valid index between 0 and 1.")

    def __setitem__(this, key, value):
        if key is 0:
            this.X = value
        elif key is 1:
            this.Y = value
        else:
            raise ValueError("Key must be a valid index between 0 and 1.")

    def __repr__(this):
        return [this.X, this.Y].__repr__()
    
    @property
    def X(this):
        return this.mX
    
    @X.setter
    def X(this, x):
        this.mX = x
    
    @property
    def Y(this):
        return this.mY
    
    @Y.setter
    def Y(this, y):
        this.mY = y

    @property
    def Length(this):
        return math.sqrt(math.pow(this.X, 2) + math.pow(this.Y, 2))
        
    def __add__(this, other):
        return Point2(this.X + other.X, this.Y + other.Y)
    
    def __sub__(this, other):
        return Point2(this.X - other.X, this.Y - other.Y)

    def DotProduct(this, other):
        return (this.X * other.X) + (this.Y * other.Y)

    def CrossProduct(this, other):
        return Point3(this.X, this.Y, 0).CrossProduct(Point3(other.X, other.Y, 0))