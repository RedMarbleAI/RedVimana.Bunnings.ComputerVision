import cv2
import numpy
import tensorflow
import time

from BoundingBox import *

class HumanDetector(object):
    def __init__(this):
        pass

    def Detect(this, image):
        return []

class COCOTensorflowHumanDetector(HumanDetector):
    def __init__(this, modelPath, threshold):
        this.mModelPath = modelPath
        this.mThreshold = threshold

        this.detection_graph = tensorflow.Graph()
        with this.detection_graph.as_default():
            od_graph_def = tensorflow.GraphDef()
            with tensorflow.gfile.GFile(this.mModelPath, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tensorflow.import_graph_def(od_graph_def, name='')

        this.default_graph = this.detection_graph.as_default()
        this.sess = tensorflow.Session(graph=this.detection_graph)

        this.image_tensor = this.detection_graph.get_tensor_by_name('image_tensor:0')
        this.detection_boxes = this.detection_graph.get_tensor_by_name('detection_boxes:0')
        this.detection_scores = this.detection_graph.get_tensor_by_name('detection_scores:0')
        this.detection_classes = this.detection_graph.get_tensor_by_name('detection_classes:0')
        this.num_detections = this.detection_graph.get_tensor_by_name('num_detections:0')
    
    def Detect(this, image):
        image_np_expanded = numpy.expand_dims(image, axis=0)
        start_time = time.time()
        (boxes, scores, classes, num) = this.sess.run(
            [this.detection_boxes, this.detection_scores, this.detection_classes, this.num_detections],
            feed_dict={this.image_tensor: image_np_expanded})
        end_time = time.time()

        im_height, im_width,_ = image.shape
        boxesList = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            # xTopLeft, yTopLeft, xBottomRight, yBottomRight
            boxesList[i] = BoundingBox(int(boxes[0,i,1]*im_width), int(boxes[0,i,0] * im_height), int(boxes[0,i,3]*im_width), int(boxes[0,i,2] * im_height))

        # scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])
        scoresList = scores[0].tolist()
        classesList = [int(x) for x in classes[0].tolist()]
        result = []
        for i in range(len(boxesList)):
            if classesList[i] == 1 and scoresList[i] > this.mThreshold:
                result.append(boxesList[i])
        
        return result

    def Close(this):
        this.sess.close()
        this.default_graph.close()

class YoloV3OpenCVDetector(HumanDetector):
    def __init__(this, modelCfgPath, modelWeightsPath, modelClassesFile, threshold):
        this.confThreshold = threshold  #Confidence threshold
        this.nmsThreshold = 0.35   #Non-maximum suppression threshold
        this.inpWidth = 416       #Width of network's input image
        this.inpHeight = 416      #Height of network's input image
        this.modelCfgPath = modelCfgPath
        this.modelWeightsPath = modelWeightsPath
        classes = None
        with open(modelClassesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
        this.classes = classes
        net = cv2.dnn.readNetFromDarknet(modelCfgPath, modelWeightsPath)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        this.net = net
        # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(this, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = numpy.argmax(scores)
                confidence = scores[classId]
                if confidence > this.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        new_boxes = []
        indices = cv2.dnn.NMSBoxes(boxes, confidences, this.confThreshold, this.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            # xTopLeft, yTopLeft, xBottomRight, yBottomRight
            if(this.classes[classIds[i]] == "person"):
                new_boxes.append(BoundingBox(int(left), int(top), int(left + width), int(top+height)))
        return new_boxes
    # Get the names of the output layers
    def getOutputsNames(this, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    def Detect(this, image):
        blob = cv2.dnn.blobFromImage(image, 1/255, (this.inpWidth, this.inpHeight), [0,0,0], 1, crop=False)
        # Sets the input to the network
        this.net.setInput(blob)
        # Runs the forward pass to get output of the output layers
        outs = this.net.forward(this.getOutputsNames(this.net))
        # Remove the bounding boxes with low confidence
        result = this.postprocess(image, outs)
        return result
    def Close(this):
        return