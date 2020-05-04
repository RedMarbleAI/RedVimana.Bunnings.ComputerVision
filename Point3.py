import math

class Point3(object):
    def __init__(this, x, y, z):
        this.mX = x
        this.mY = y
        this.mZ = z

    def __len__(this):
        return 3

    def __getitem__(this, key):
        if key is 0:
            return this.X
        elif key is 1:
            return this.Y
        elif key is 2:
            return this.Z
        else:
            raise ValueError("Key must be a valid index between 0 and 2.")

    def __setitem__(this, key, value):
        if key is 0:
            this.X = value
        elif key is 1:
            this.Y = value
        elif key is 2:
            this.Z = value
        else:
            raise ValueError("Key must be a valid index between 0 and 2.")

    def __repr__(this):
        return [this.X, this.Y, this.Z].__repr__()
    
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
    def Z(this):
        return this.mZ
    
    @Z.setter
    def Z(this, z):
        this.mZ = z

    @property
    def Length(this):
        return math.sqrt(math.pow(this.X, 2) + math.pow(this.Y, 2) + math.pow(this.Z, 2))
        
    def __add__(this, other):
        return Point3(this.X + other.X, this.Y + other.Y, this.Y + other.Z)
    
    def __sub__(this, other):
        return Point3(this.X - other.X, this.Y - other.Y, this.Z - other.Z)

    def DotProduct(this, other):
        return (this.X * other.X) + (this.Y * other.Y) + (this.Z * other.Z)

    def CrossProduct(this, other):
        return Point3((this.Y * other.Z) - (this.Z * other.Y), (this.Z * other.X) - (this.X - other.Z), (this.X * other.Y) - (this.Y - other.X))