from Point2 import *
from Size2 import *

class BoundingBox(object):
    def __init__(this, xTopLeft, yTopLeft, xBottomRight, yBottomRight):
        if (xTopLeft > xBottomRight):
            raise ValueError("Top left point must have a x-coordinate smaller or equal to the bottom right point's x-coordinate.")
        if (yTopLeft > yBottomRight):
            raise ValueError("Top left point must have a y-coordinate smaller or equal to the bottom right point's y-coordinate.")
        
        this.mTopLeft = Point2(xTopLeft, yTopLeft)
        this.mBottomRight = Point2(xBottomRight, yBottomRight)
        this.mPoints = [Point2(xTopLeft, yTopLeft), Point2(xBottomRight, yTopLeft), Point2(xBottomRight, yBottomRight), (xTopLeft, yBottomRight)]
        this.mCenter = Point2(((xTopLeft + xBottomRight) / 2), ((yTopLeft + yBottomRight) / 2))
        this.mSize = Size2(xBottomRight - xTopLeft, yBottomRight - yTopLeft)
        
    @property
    def Size(this):
        return this.mSize
    
    @property
    def Points(this):
        return this.mPoints
    
    @property
    def Center(this):
        return this.mCenter
    
    @property
    def TopLeft(this):
        return this.mTopLeft
    
    @property
    def BottomRight(this):
        return this.mBottomRight