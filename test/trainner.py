import os
import cv2
import numpy as np
from PIL import Image

def train():
    detector=cv2.face.LBPHFaceRecognizer_create()
    path='dataset'

    def getImagesWithID(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]

        benches=[]
        IDs=[]
        for imagePath in imagePaths:
            benchImg=Image.open(imagePath).convert('L')
            benchNp=np.array(benchImg,'uint8')
            ID=int(os.path.split(imagePath)[-1].split('_')[1])
            benches.append(benchNp)
            IDs.append(ID)
            cv2.imshow("training",benchNp)
            cv2.waitKey(10)
        return np.array(IDs),benches

    Ids,benches=getImagesWithID(path)
    detector.train(benches,Ids)
    detector.save('detector/trainingData.yml')
    cv2.destroyAllWindows()

train()