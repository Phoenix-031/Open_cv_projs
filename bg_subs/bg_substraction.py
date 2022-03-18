import tkinter
import cv2
import mediapipe as mp                       # importing libraries
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation           # creating selfie segmentation object           

ls = os.listdir("./images")
lsimg = []
for i in ls:
    img = cv2.imread(f"./images/{i}")
    lsimg.append(img)

idx = 0

cap = cv2.VideoCapture(0)                                            # getting the web cam
cap.set(3,1280)                                                      # setting the width
cap.set(4,720)                                                       # setting the height
cap.set(10,100)                                                      # setting brightness

with mp_selfie_segmentation.SelfieSegmentation(model_selection = 1) as ssg:

    while True:

        _,img = cap.read()
        fim = cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)     
        res = ssg.process(fim)
        fim = cv2.cvtColor(fim, cv2.COLOR_RGB2BGR)

        condition = np.stack((res.segmentation_mask,) * 3, axis=-1) > 0.8

        output_image = np.where(condition, fim, lsimg[idx])                                # remove the bg with the image
        cv2.imshow("window" ,output_image)

        key = cv2.waitKey(1)
        if key == 113:
            break
        elif key == ord('a') and idx<len(lsimg)-1:
            idx+=1
        elif key == ord('d') and idx >=0:
            idx -=1



cap.release()
cv2.destroyAllWindows()



