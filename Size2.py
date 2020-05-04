class Size2(object):
    def __init__(this, width, height):
        this.mWidth = width
        this.mHeight = height
    
    @property
    def Width(this):
        return this.mWidth
    
    @property
    def Height(this):
        return this.mHeight
    
    @property
    def Area(this):
        return this.mWidth * this.mHeight