import cv2
import threading

from threading import Lock

class Camera(object):
    def __init__(this, configuration):
        this.mConfiguration = configuration

    def GetFrame(this):
        return None

    @property
    def Configuration(this):
        return this.mConfiguration

class OpenCVCamera(Camera):
    mLastFrame = None
    mLastReady = None
    mLock = Lock()

    def __init__(this, configuration, videoCapture):
        super().__init__(configuration)
        thread = threading.Thread(target=this.ReadCamera, args=(videoCapture,), name="OpenCV Video Capture")
        thread.daemon = True
        thread.start()

    def ReadCamera(this, videoCapture):
        while True:
            with this.mLock:
                this.mLastReady, this.mLastFrame = videoCapture.read()

    def GetFrame(this):
        if (this.mLastReady is not None) and (this.mLastFrame is not None):
            return this.mLastFrame.copy()
        else:
            return None

class RTSPCamera(OpenCVCamera):
    def __init__(this, configuration):
        super().__init__(configuration, cv2.VideoCapture(configuration.Url))

class GStreamerCamera(OpenCVCamera):
    def __init__(this, configuration):
        super().__init__(configuration, cv2.VideoCapture(configuration.ConfigurationString, cv2.CAP_GSTREAMER))

class FileCamera(Camera):
    mLastFrame = None
    mLastReady = None

    def __init__(this, configuration):
        super().__init__(configuration)
        this.mVideoCapture = cv2.VideoCapture(configuration.Path)

    def GetFrame(this):
        this.mLastReady, this.mLastFrame = this.mVideoCapture.read()
        if (this.mLastReady is not None) and (this.mLastFrame is not None):
            return this.mLastFrame.copy()
        else:
            return None


class FileStreamCamera(OpenCVCamera):
    def __init__(this, configuration):
        super().__init__(configuration, cv2.VideoCapture(configuration.Path))