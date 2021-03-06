import cv2
import numpy as np
import os

#generate list of faces in folder
faces_dir = "/Users/pavangollapalli/repos/face-ratios/current/relativedistances/faces/"
faces = os.listdir(faces_dir)
faces.remove('.DS_Store')

#sets up classifiers
face_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/lbpcascades/lbpcascade_frontalface.xml')
left_eye_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_lefteye.xml')
right_eye_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_righteye.xml')
nose_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_mouth.xml')

#reads image (do only 1 for now, but run for each picture later)
img = cv2.imread(faces_dir + 'face1.jpg')
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#creates mask
mask = np.zeros(img.shape[:2], np.uint8)

#detects face
def detect_face(grey):
	faces = face_cascade.detectMultiScale(grey, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	return {'face_area':grey[y:y+h,x:x+w], 'face_x': faces[0][0],'face_y':faces[0][1]}

#objective: run detector on each feature: start with the one that's most accurate

#detects feature from originial roi, draws box on original, applies mask to grey and returns it
def find_mouth(face):
	mouth = mouth_cascade.detectMultiScale(face['face_area'],1.3,5)
	face_x = face['face_x']
	face_y = face['face_y']
	for i,(x,y,w,h) in enumerate(mouth):
		print i, " mouth ",x,y,x+w,y+h
		mask = np.ones(img.shape[:2], np.uint8)*255
		mask[y:y+h,x:x+w] = 0
		cv2.bitwise_and(grey,grey,mask=mask)
		cv2.rectangle(img,(face_x+x,face_y+y),(face_x+x+w,face_y+y+h),(0,128,255),2)
		cv2.putText(img, 'mouth', (face_x+x,face_y+y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0)) 


def find_nose(face):
	nose = mouth_cascade.detectMultiScale(face['face_area'],1.3,5)
	face_x = face['face_x']
	face_y = face['face_y']
	for (x,y,w,h) in nose:
		mask = np.ones(img.shape[:2], np.uint8)*255
		mask[y:y+h,x:x+w] = 0
		cv2.bitwise_and(grey,grey,mask=mask)
		cv2.rectangle(img,(face_x+x,face_y+y),(face_x+x+w,face_y+y+h),(0,128,255),2)
		cv2.putText(img, 'nose', (face_x+x,face_y+y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0)) 

def find_eyes(face):
	eyes = mouth_cascade.detectMultiScale(face['face_area'],1.3,5)
	face_x = face['face_x']
	face_y = face['face_y']
	for (x,y,w,h) in eyes:
		mask = np.ones(img.shape[:2], np.uint8)*255
		mask[y:y+h,x:x+w] = 0
		cv2.bitwise_and(grey,grey,mask=mask)
		cv2.rectangle(img,(face_x+x,face_y+y),(face_x+x+w,face_y+y+h),(0,128,255),2)
		cv2.putText(img, 'eye', (face_x+x,face_y+y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0)) 


''' for face in faces:
		run program for each picture'''
face = detect_face(grey)
cv2.imshow('face_area',face['face_area'])
find_mouth(face)
#find_nose(face)
#find_eyes(face)
cv2.imshow('grey',grey)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()