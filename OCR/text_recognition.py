# text_recognition.py

from imutils.object_detection import non_max_supression
import numpy as np
import pytesseract
import argparse
import cv2

def text_detector (image, min_confidence = 0.5):
    # note width and height must me multiple of 32
    east =
    orig = image.copy()
    (H, W) = image.shape[:2]
    rW = int(W/32)*32
    rH = int(H/32)*32

    image = cv2.resize(image, (rW, rH))
    (H,W) = (rH, rW)

    # define output lyer names for EAST detector model
    # probobilities, boundig box
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    print("loading EAST text detector")
    net = cv2.dnn.readNet(east)

    #perform forward pass of model to get two output layers
    blob = cv2.dnn.blobFromImage(image, 1.0, (W,H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    
    #set init bounding boxes from scores
    (numRows, numCols) = scores.shape[2:4]
    rects = list() # stores bounding box coors
    confidences = list() # stores prbability associated with each bounding box 

    for y in range(0, numRows):
        #extract probabilities and bounding box coors
        scoresData = scores[0,0,y]
        xData0 = geometry[0,0,y]
        xData1 = geometry[0,1,y]
        xData2 = geometry[0,2,y]
        xData3 = geometry[0,3,y]
        anglesData = geometry[0,4,y]

    for x in range(0, numCols):
        if scoresData[x] < min_confidence:
            continue
        
        #compute offset factor as feature maps will be 4x smaller
        (offsetX, offsetY) = (x * 4.0, y * 4.0)

        #extract rotation angle for prediction and compute sin cos
        angle = anglesData[x]
        cos = np.cos(angle)
        sin = np.sin(angle)

        #derive width and height of bounding box
        h = xData0[x] + xData2[x]
        w = xData1[x] = xData3[x]

        #find starting and ending points of bounding box
        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
		endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
		startX = int(endX - w)
		startY = int(endY - h)

        #add bounding box and probability to lists
        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])

        #apply non maxima suppression to suppres weak,overlapping boxes
        boxes = non_max_supression(np.array(rects), probs=confidences)

        for(startX, startY, endX, endY) in boxes:

            startX = int(startX * rW)
            startY = int(startY *rH)
            endX = int(endX * rW)
            endY = int(endY *rH)

            # draw the bounding box on the image
	        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        cv2.imshow("Text Detect", orig )
        cv2.waitKey(0)

    

