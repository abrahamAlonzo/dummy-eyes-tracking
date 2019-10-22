from BarcodeDecoder import decode
from DraculaConversation import CharacterAudio, InitialDialog, LeaveDialog
import numpy as np
import cv2
import time
import logging
import threading
from ArduinoExampleInterface import MotorController
# Pending for motor controllers
# Pending for sounds of dialogs and interactivity
#

class VideoStream:
    def __init__(self):
        self.statusConstants = {
            'initialDialog': 0,
            'faceRecognition': 1,
            'barcodeRecognition': 2,
            'scanIDDialog': 3,
            'LeaveDialog': 4
        }
        self.statusConstantsLog = {
            0: 'initialDialog',
            1: 'faceRecognition',
            2: 'barcodeRecognition',
            3: 'scanIDDialog',
            4: 'LeaveDialog'
        }
        self.frame = []
        self.frameWidth = 0
        self.frameHeight = 0
        self.camera = 0
        self.status = self.statusConstants['faceRecognition']
        self.faceRecognited = False
        self.barcode = ''
        self.video = 'video'
        self.eye_cascade = ''
        self.face_cascade = ''
        self.displayVideo = True
        self.eyeRecognition = False
        self.debugFaceRecognition = True
        self.eyeController = MotorController()
        self.leftEyeTheta = 0
        self.leftEyePhi = 0
        self.rightEyeTheta = 0
        self.rightEyePhi = 0
        self.xFacePosition = 0
        self.yFacePosition = 0
        #after many drops the conclution is than there is no person at all
        self.faceIterationDrops = 0

    def EyeRecognitionInitialization(self):
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def FaceRecognitionInitialization(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def MotorController(self):
        return

    def Translate(self, sensor_val, in_from, in_to, out_from, out_to):
        out_range = out_to - out_from
        in_range = in_to - in_from
        in_val = sensor_val - in_from
        val=(float(in_val)/in_range)*out_range
        out_val = out_from+val
        return out_val

    def TakeVideo(self):
        capture = cv2.VideoCapture(self.camera)
        ret, self.frame = capture.read()
        self.frameWidth = self.frame.shape[1]
        self.frameHeight = self.frame.shape[0]
        if self.eyeRecognition == True:
            self.EyeRecognitionInitialization()

        self.FaceRecognitionInitialization()
        while(True):

            ret, self.frame = capture.read()
            self.MotorController()
            #print(self.statusConstantsLog[self.status])
            if (self.status == self.statusConstants['barcodeRecognition']):
                decodedObjects = decode(self.frame)
                self.barcode = decodedObjects
                if len(self.barcode) != 0:
                    for character in self.barcode:
                        print(character)
                        CharacterAudio(character)
                    self.status = self.statusConstants['LeaveDialog']
                    
            elif (self.status == self.statusConstants['faceRecognition']):
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                #print(faces)
                if (len(faces) != 0):
                    self.faceRecognited = True
                    # if is higher something need to be triggered
                    self.faceIterationDrops = 0
                    #Just for debuggin porpusitiones of face recogn
                    if self.debugFaceRecognition == False:
                        self.status = self.statusConstants['initialDialog']
                    else:
                        for (x,y,w,h) in faces:
                            #only see one person in the same time and in a certain velocity
                            if ( self.xFacePosition - x < 200   and self.yFacePosition - y < 200):
                                print('Faces: ' + 'x' + str(x) + ' '+ 'y' +  str(y))
                                self.xFacePosition = x
                                self.yFacePosition = y
                                self.leftEyeTheta = self.Translate(x, 0, self.frameWidth, 0, 185) 
                                self.leftEyePhi = self.Translate(x, 0, self.frameHeight, 0, 185) 
                        self.eyeController.LeftEyePhiController(self.leftEyeTheta)
                        self.eyeController.LeftEyeThetaController(self.leftEyeTheta)
                        
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = self.frame[y:y+h, x:x+w]
                        if self.eyeRecognition == True:
                            self.EyeRecognition(roi_gray, roi_color)
                        #print('faceRecognited True')
                else:
                    self.faceIterationDrops += 1
                    print('faceIterationDrops: ' + str(self.faceIterationDrops))
                    self.faceRecognited = False
                    #print('faceRecognited False')
                if self.displayVideo == True:
                    for (x,y,w,h) in faces:
                        self.frame = cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = self.frame[y:y+h, x:x+w]
                       
                        if self.eyeRecognition == True:
                            self.EyeRecognition(roi_gray, roi_color)
            elif (self.status == self.statusConstants['initialDialog']):
                InitialDialog()
                self.status = self.statusConstants['barcodeRecognition']
            elif (self.status == self.statusConstants['LeaveDialog']):
                time.sleep(2)
                LeaveDialog()
                self.status = self.statusConstants['faceRecognition']
            if self.displayVideo ==True:
                cv2.imshow(self.video, self.frame)

            if cv2.waitKey(1) == 27:
                break
    
        capture.release()
        cv2.destroyAllWindows()


    def EyeRecognition(self, roi_gray, roi_color):
        eyes = self.eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            if self.debugFaceRecognition == True:
                print('Eyes' + 'ex' + str(ex) + ' '+ 'ey' +  str(ey))





# Display barcode and QR code location  
def display(im, decodedObjects):

    # Loop over all decoded objects
    for decodedObject in decodedObjects: 
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else : 
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0,n):
            cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    # Display results 
    cv2.imshow("Results", im)
    cv2.waitKey(0)

def DraculaThread(*args):
    Video = VideoStream()
    Video.TakeVideo()

def EyesThread():
    #some python code for servo motor controlling with serial 
    return

# Main 
if __name__ == '__main__':
    # loggin config
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    Video = VideoStream()
    Video.TakeVideo()
    # #thread config
    #draculaAI = threading.Thread(target=DraculaThread)
    # eyesMovement = threading.Thread(target=DraculaThread, args=(1,))
    
    # #initial of threading
    #draculaAI.start()
    # eyesMovement.start()
    
    # #end of execution
    # logging.info("Main    : wait for the thread to finish")
    # logging.info("Main    : all done")
    

    



    
