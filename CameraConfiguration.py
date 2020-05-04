from Camera import *

class CameraConfiguration(object):
    def __init__(this, coordinateConverter):
        this.mCoordinateConverter = coordinateConverter
        pass
    
    def ConvertToGlobalCoordinates(this, imagePoint):
        return this.mCoordinateConverter.ConvertCoordinates(imagePoint)

    @property
    def CoordinateConverter(this):
        return this.mCoordinateConverter

    def CreateCamera(this):
        return None

class RTSPCameraConfiguration(CameraConfiguration):
    def __init__(this, url, coordinateConverter):
        super().__init__(coordinateConverter)
        this.mUrl = url
    
    @property
    def Url(this):
        return this.mUrl

    def CreateCamera(this):
        return RTSPCamera(this)

class GStreamerCameraConfiguration(CameraConfiguration):
    def __init__(this, configurationString, coordinateConverter):
        super().__init__(coordinateConverter)
        this.mConfigurationString = configurationString
    
    @property
    def ConfigurationString(this):
        return this.mConfigurationString

    def CreateCamera(this):
        return GStreamerCamera(this)

class FileCameraConfiguration(CameraConfiguration):
    def __init__(this, path, coordinateConverter):
        super().__init__(coordinateConverter)
        this.mPath = path
    
    @property
    def Path(this):
        return this.mPath

    def CreateCamera(this):
        return FileCamera(this)

class FileStreamCameraConfiguration(CameraConfiguration):
    def __init__(this, path, coordinateConverter):
        super().__init__(coordinateConverter)
        this.mPath = path
    
    @property
    def Path(this):
        return this.mPath

    def CreateCamera(this):
        return FileStreamCamera(this)