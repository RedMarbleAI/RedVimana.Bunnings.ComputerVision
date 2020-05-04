from CameraConfiguration import *

class Configuration(object):
    def __init__(this):
        this.mCameras = []
        return
    
    @property
    def ModelPath(this):
        return this.mModelPath
    
    @ModelPath.setter
    def ModelPath(this, modelPath):
        this.mModelPath = modelPath
    
    @property
    def Cameras(this):
        return this.mCameras
    
    @Cameras.setter
    def Cameras(this, cameras):
        if isinstance(cameras, list) and all(isinstance(x, CameraConfiguration) for x in cameras):
            this.mCameras = cameras
        else:
            raise ValueError("Cameras must be a list of CameraConfigurations.")
            
    @property
    def ModelImageSize(this):
        return this.mModelImageSize
    
    @ModelImageSize.setter
    def ModelImageSize(this, modelImageSize):
        this.mModelImageSize = modelImageSize