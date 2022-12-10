import numpy as np
import cv2
import sys, getopt

def detect(img, cascade):
    '''Detect objects of different sizes in the input image. The detected objects are returned as a list of rectangles.'''
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

#intersection rate of two rectangles
#-- 1. Load the cascades
cascade_fn = self.repoPath + '/data/haarcascades/haarcascade_frontalface_alt.xml'
nested_fn  = self.repoPath + '/data/haarcascades/haarcascade_eye.xml'
#-- 2. Read the image
cascade = cv2.CascadeClassifier(cascade_fn)
nested = cv2.CascadeClassifier(nested_fn)
#-- 3. Apply the classifier to the image
samples = ['samples/data/lena.jpg', 'cv/cascadeandhog/images/mona-lisa.png']

faces = []
eyes = []
#faces and eyes of test images
testFaces = [
#lena
[[218, 200, 389, 371],
[ 244, 240, 294, 290],
[ 309, 246, 352, 289]],

#lisa
[[167, 119, 307, 259],
[188, 153, 229, 194],
[236, 153, 277, 194]]
]

#intersection rate of two rectangles
#-- 4. For the first test image, show the image and the face detections
#-- 5. For the second test image, show the image and the face detections
#-- 6. Save the result
for sample in samples:

    img = self.get_sample(  sample)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 5.1)

    rects = detect(gray, cascade)
    faces.append(rects)

    if not nested.empty():
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested)

            for rect in subrects:
                rect[0] += x1
                rect[2] += x1
                rect[1] += y1
                rect[3] += y1

            eyes.append(subrects)

faces_matches = 0
eyes_matches = 0

eps = 0.8

#check faces
#-- 7. Compare the results with the test images
#-- 8. Check if the results are correct
#-- 9. Save the result
for i in range(len(faces)):
    for j in range(len(testFaces)):
        if intersectionRate(faces[i][0], testFaces[j][0]) > eps:
            faces_matches += 1
            #check eyes
            if len(eyes[i]) == 2:
                if intersectionRate(eyes[i][0], testFaces[j][1]) > eps and intersectionRate(eyes[i][1] , testFaces[j][2]) > eps:
                    eyes_matches += 1
                elif intersectionRate(eyes[i][1], testFaces[j][1]) > eps and intersectionRate(eyes[i][0], testFaces[j][2]) > eps:
                    eyes_matches += 1

self.assertEqual(faces_matches, 2)
self.assertEqual(eyes_matches, 2)
