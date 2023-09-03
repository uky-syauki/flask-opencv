import cv2 as cv
import numpy as np
from PIL import Image
import os
from app.dbHandle import DB

class OPENCV:
    def __init__(self, user):
        self.face_cascade = cv.CascadeClassifier('cascade/face_detect.xml')
        self.eyes_cascade = cv.CascadeClassifier('cascade/eye_detect.xml')
        self.recognition = cv.face.LBPHFaceRecognizer_create()
        self.path_dataset = f'dataset/'
        self.path_training = f'training/latih.yml'
        self.path_img_sample = f'sampleimg/{user["nama"]}'
        self.user = user
        self.buat_directory_user()
    def buat_directory_user(self):
        if not os.path.exists(self.path_dataset):
            os.mkdir(self.path_dataset)
        if not os.path.exists(self.path_dataset):
            os.mkdir(self.path_img_sample)
    def add_dataset_img(self):
        hitung = 0
        daftar_img_user = f"{self.path_img_sample}"
        ls = os.listdir(daftar_img_user)
        jumlah = 30 if ls >= 30 else len(ls)
        for isi in ls[:jumlah]:
            # print(isi.split('.')[-1])
            print(f"{daftar_img_user}/{isi}")
            img = cv.imread(f"{daftar_img_user}/{isi}")
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            face = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in face:
                hitung += 1
                cv.imwrite(f"{self.path_dataset}/{self.user['nama']}.{self.user['id']}.{hitung}.jpg", gray[y:y+h, x:x+w])
        self.training()
    def get_image_and_label(self,path):
        path_image = [os.path.join(path, f) for f in os.listdir(path)]
        sample_wajah = []
        ids = []
        for path_img in path_image:
            PIL_Image = Image.open(path_img).convert('L')
            img_numpy = np.array(PIL_Image, 'uint8')
            id = int(os.path.split(path_img)[-1].split('.')[1])
            face = self.face_cascade.detectMultiScale(img_numpy)

            for (x, y, w, h) in face:
                sample_wajah.append(img_numpy)
                ids.append(id)
        return sample_wajah, ids
    def training(self):
        faces, ids = self.get_image_and_label(self.path_dataset)
        self.recognition.train(faces, np.array(ids))
        self.recognition.write(self.path_training)
    def deteksi_wajah_img(self,img_target):
        self.recognition.read(self.path_training)
        # font = cv.FONT_HERSHEY_COMPLEX
        id = 0
        #names = ['None', f'{self.user["nama"]}'] # ganti menjadi sesuai database
        names = ["None"]
        for isi in DB().getAllUser():
            names.append(isi[1])
        while True:
            img = cv.imread(img_target)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            wajah = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
            id = 0
            confidance = 100
            for (x, y, w, h) in wajah:
                id, confidance = self.recognition.predict(gray[y:y+h, x:x+w])
                if (confidance < 50):
                    id = names[id]
                    confidance = (100 - round(confidance))
                else:
                    id = "Siapa ini"
                    confidance = (100 - round(confidance))
                    
            return id, confidance
    def latih_sampleimg(self):
        sample_user = os.listdir(self.path_img_sample)
        for isi in sample_user:
            hasil = self.deteksi_wajah_img(f'{self.path_img_sample}/{isi}')
            if hasil[1] < 50:
                if os.path.exists(f'{self.path_img_sample}/{isi}'):
                    os.remove(f'{self.path_img_sample}/{isi}')
                    print("Hapus file:", isi, hasil[1])
        self.add_dataset_img()
    def tes_deteksi_wajah_img(self,img_target):
        self.recognition.read(self.path_training)
        font = cv.FONT_HERSHEY_COMPLEX
        id = 0
        #names = ['None', f'{self.user["nama"]}'] # ganti menjadi sesuai database
        names = ["None"]
        for isi in DB().getAllUser():
            names.append(isi[1])
        while True:
            img = cv.imread(img_target)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            wajah = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
            id = 0
            confidance = 100
            for (x, y, w, h) in wajah:
                cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidance = self.recognition.predict(gray[y:y+h, x:x+w])
                if (confidance < 50):
                    id = names[id]
                    confidance = f"{(100 - round(confidance))}%"

                else:
                    id = "Siapa ini"
                    confidance = f"{(100 - round(confidance))}%"

                cv.putText(img, f"    {str(id)}", (x+5, y+5), font, 1, (255,255,255),2)
                cv.putText(img, str(confidance), (x+5, y+5), font, 1, (255,255,0), 1)
            
            cv.imshow("Foto", img)
            k = cv.waitKey(0)
            if k == 27:
                break
        
        cv.destroyAllWindows()
            #return id, confidance


