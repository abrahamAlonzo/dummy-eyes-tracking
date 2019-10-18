from BarcodeDecoder import decode
from DraculaConversation import CharacterAudio
import numpy as np
import cv2


class VideoStream:
    def __init__(self):
        self.frame = []
        self.camera = 1
        self.barcode = ''
        self.video = 'video'
        self.eye_cascade = ''
        self.face_cascade = ''

    def EyeRecognitionInitialization(self):
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def FaceRecognitionInitialization(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def TakeVideo(self):
        capture = cv2.VideoCapture(self.camera)
        #self.EyeRecognitionInitialization()
        #self.FaceRecognitionInitialization()
        while(True):
            ret, self.frame = capture.read()
            decodedObjects = decode(self.frame)
            self.barcode = decodedObjects
            if len(self.barcode) != 0:
                for character in self.barcode:
                    print(character)
                    CharacterAudio(character)
            #display(self.frame, decodedObjects)
            ##cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3) 
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            # for (x,y,w,h) in faces:
            #     self.frame = cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
            #     roi_gray = gray[y:y+h, x:x+w]
            #     roi_color = self.frame[y:y+h, x:x+w]
            #     #self.EyeRecognition(roi_gray, roi_color)
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



    