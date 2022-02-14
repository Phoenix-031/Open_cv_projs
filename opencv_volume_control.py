from operator import length_hint
import cv2
import mediapipe as mp
import numpy as np
import math
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

vid = cv2.VideoCapture(0)
vid.set(3,800)
vid.set(4,800)
vid.set(10,60)

mphands = mp.solutions.hands  
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

dev = AudioUtilities.GetSpeakers()
inter = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(inter, POINTER(IAudioEndpointVolume))

min,max = volume.GetVolumeRange()[:2]

while 1:
    var, img = vid.read()
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)
    lst = []
    
    if res.multi_hand_landmarks:
        for i in  res.multi_hand_landmarks:
            for id,val in enumerate(i.landmark):
                # print(id,val)
                h,w,c = img.shape
                cx,cy = int(val.x*w), int(val.y*h)
                lst.append([id,cx,cy])
            mpdraw.draw_landmarks(img,i,mphands.HAND_CONNECTIONS)
    if len(lst):
        x1,y1 = lst[4][1],lst[4][2]
        x2,y2 = lst[8][1],lst[8][2]

        cv2.circle(img,(x1,y1),10,(0,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)
        vol = np.interp(length,[15,220],[min,max])
        volume.SetMasterVolumeLevel(vol, None)
        
        
    cv2.imshow("webcam",img)
    key = cv2.waitKey(1)
    if key == 113:
        break