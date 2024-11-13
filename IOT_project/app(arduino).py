import cv2
import numpy as np
import logging
import time
import serial

animals = ['bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','person']

logging.basicConfig(
    filename='app(arduino).log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = 'coco.names'
modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

with open(classesfile, 'rt', encoding='utf-8') as f:
    classNames = f.read().rstrip('\n').split('\n')

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

arduino_port = 'COM8'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)

def findObjects(outputs, img):
    hT, wT, _ = img.shape
    bbox, classIds, confs = [], [], []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    detected_person = False

    if indices is not None and len(indices) > 0:
        for i in indices.flatten():
            box = bbox[i]
            x, y, w, h = box
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            label = f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%'
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            if classNames[classIds[i]] not in animals:
                detected_person = True
                arduino.write(b'1') 

    return detected_person

def get_frame():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Cannot open camera.")
        return None
    time.sleep(0.2)
    ret, img = cap.read()
    cap.release()  
    return img if ret else None

def main():
    while True:
        img = get_frame()
        if img is None:
            continue
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        layernames = net.getLayerNames()
        outputNames = [layernames[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
        outputs = net.forward(outputNames)

        if findObjects(outputs, img):
            logging.info("Person detected, servo activated.")
        else:
            logging.info("No person detected.")

        cv2.imshow('Object Detection', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
    