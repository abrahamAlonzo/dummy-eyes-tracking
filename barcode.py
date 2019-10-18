from BarcodeDecoder import decode

import numpy as np
import cv2

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
	imageBarcode = cv2.imread('barcode.png')
	decodedObjects = decode(imageBarcode)
	print(decodedObjects)
	display(imageBarcode, decodedObjects)