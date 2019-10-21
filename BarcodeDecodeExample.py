from BarcodeDecoder import decode
import numpy as np
import cv2



if __name__ == "__main__":
	cam = cv2.VideoCapture(0)
	s, im = cam.read() # captures image
	cv2.imshow("Test Picture", im) # displays captured image
	cv2.imwrite("some2.png",im) # writes image test.bmp to disk
	imageBarcode = cv2.imread('barcode.png')
	decodedObjects = decode(imageBarcode)
	print(decodedObjects)
	display(imageBarcode, decodedObjects)