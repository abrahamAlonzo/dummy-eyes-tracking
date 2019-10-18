from BarcodeDecoder import decode
from DraculaConversation import CharacterAudio, InitialDialog, LeaveDialog
import numpy as np
import cv2
import time


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
        self.camera = 1
        self.status = self.statusConstants['faceRecognition']
        self.faceRecognited = False
        self.barcode = ''
        self.video = 'video'
        self.eye_cascade = ''
        self.face_cascade = ''
        self.displayVideo = True
        self.eyeRecognition = False

    def EyeRecognitionInitialization(self):
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def FaceRecognitionInitialization(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def MotorController(self):
        return

    def TakeVideo(self):
        capture = cv2.VideoCapture(self.camera)

        if self.eyeRecognition == True:
            self.EyeRecognitionInitialization()

        self.FaceRecognitionInitialization()
        while(True):
            time.sleep(0.1)
            ret, self.frame = capture.read()
            self.MotorController()
            print(self.statusConstantsLog[self.status])
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
                if (len(faces) != 0):
                    self.faceRecognited = True
                    self.status = self.statusConstants['initialDialog']
                    #print('faceRecognited True')
                else:
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


# Main 
if __name__ == '__main__':
	#cam = cv2.VideoCapture(0)
	#s, im = cam.read() # captures image
	#cv2.imshow("Test Picture", im) # displays captured image
	#cv2.imwrite("some2.png",im) # writes image test.bmp to disk
	# imageBarcode = cv2.imread('barcode.png')
	# decodedObjects = decode(imageBarcode)
	# print(decodedObjects)
	# display(imageBarcode, decodedObjects)
    Video = VideoStream()
    Video.TakeVideo()



    