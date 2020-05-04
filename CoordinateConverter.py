import math

from Point2 import *

class CoordinateConverter(object):
    def __init__(this):
        pass

    def ConvertCoordinates(this, imagePoint):
        return imagePoint

class TopDownCoordinateConverter(CoordinateConverter):
    def __init__(this, fieldOffset, fieldSize, imageSize):
        this.mFieldOffset = fieldOffset
        this.mFieldSize = fieldSize
        this.mImageSize = imageSize

    @property
    def FieldOffset(this):
        return this.mFieldOffset

    @property
    def FieldSize(this):
        return this.mFieldSize

    def ConvertCoordinates(this, imagePoint):
        localSize = this.FieldSize
        globalOffset = this.FieldOffset
        localPoint = Point2((imagePoint.X / this.mImageSize.Width) * localSize.Width, (imagePoint.Y / this.mImageSize.Height) * localSize.Height)

        return globalOffset + localPoint

class BarycentricCoordinateConverter(CoordinateConverter):
    def __init__(this, polygonFrom, polygonTo):
        this.mPolygonFrom = polygonFrom
        this.mPolygonTo = polygonTo

    def ConvertCoordinates(this, imagePoint):
        return barycentricToCartesian(cartesianToBarycentric(imagePoint, this.mPolygonFrom), this.mPolygonTo)

def cartesianToBarycentric(p, Q):
    weights = []
    n = len(Q)
    weightSum = 0
    for j in range(len(Q)):
        vertex = Q[j]
        prev = (j + n - 1) % n
        next = (j + 1) % n
        omegaJ = (cotangent(p, vertex, Q[prev]) + cotangent(p, vertex, Q[next])) / math.pow((p - vertex).Length, 2)
        omegaJ = abs(omegaJ)
        weights.append(omegaJ)
        weightSum += omegaJ
    
    return [omegaJ/weightSum for omegaJ in weights]

def barycentricToCartesian(p, Q):
    n = len(Q)
    if len(p) != n:
        raise ValueError("The barycentric coordinate dimensionality must agree with the polygon dimensionality.")
    
    dimensionality = len(Q[0])
    if dimensionality == 2:
        result = Point2(0, 0)
    elif dimensionality == 3:
        result = Point3(0, 0, 0)
    else:
        raise ValueError("Only 2D and 3D space is supported")
    
    for i in range(n):
        if dimensionality == 2:
            component = Point2(p[i] * Q[i][0], p[i] * Q[i][1])
            result = result + component
        elif dimensionality == 3:
            component = Point3(p[i] * Q[i][0], p[i] * Q[i][1], p[i] * Q[i][2])
            result = result + component
    
    return result

def cotangent(a, b, c):
    ba = a - b
    bc = c - b
    theta = math.acos(ba.DotProduct(bc) / (ba.Length * bc.Length))
    return 1 / math.tan(theta)