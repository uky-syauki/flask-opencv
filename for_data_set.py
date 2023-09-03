import cv2 as cv
import os

def setDataset(im,nama):
    try:
        hitung = len(os.listdir(f"dataset/{nama}"))
        hitung = hitung if hitung > 0 else 1
    except:
        os.mkdir(f'dataset/{nama}')
        hitung = len(os.listdir(f"dataset/{nama}"))
        hitung = hitung if hitung > 0 else 1

    img = cv.imread(im)
    face_detec = cv.CascadeClassifier('cascade/face_detect.xml')
    target = 'dataset/'
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face = face_detec.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    for (x, y, w, h) in face:
        cv.imwrite(f"{target}{nama}/{hitung}.jpg", gray[y:y+h, x:x+w])



setDataset('sampleimg/uki/1-1.png','maman')