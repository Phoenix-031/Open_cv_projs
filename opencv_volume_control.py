import time
import cv2
import mediapipe as mp
import numpy as np
import math
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import pyautogui


vid = cv2.VideoCapture(0)
vid.set(3,640)
vid.set(4,480)
vid.set(10,60)

mphands = mp.solutions.hands  
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

dev = AudioUtilities.GetSpeakers()
inter = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(inter, POINTER(IAudioEndpointVolume))
ran = volume.GetVolumeRange()
min = ran[0]
max = ran[1]
change =0


while 1:
    var, img = vid.read()
    hflip = cv2.flip(img, 1)
    imgrgb = cv2.cvtColor(hflip, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)
    lst = []
    
    if res.multi_hand_landmarks:
        for i in  res.multi_hand_landmarks:
            for id,val in enumerate(i.landmark):
                h,w,c = hflip.shape
                cx,cy = int(val.x*w), int(val.y*h)
                lst.append([id,cx,cy])
            mpdraw.draw_landmarks(hflip,i,mphands.HAND_CONNECTIONS)

    if len(lst):
        x1,y1 = lst[4][1],lst[4][2]
        x2,y2 = lst[8][1],lst[8][2]

        xm = (x1+x2)//2
        ym = (y1+y2)//2

        cv2.circle(hflip,(x1,y1),10,(0,0,0),cv2.FILLED)
        cv2.circle(hflip,(x2,y2),10,(0,0,0),cv2.FILLED)
        cv2.circle(hflip,(xm,ym),5,(0,0,0),cv2.FILLED)
        cv2.line(hflip,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        if lst[12][2] > lst[10][2]:
            change = 1
        if lst[12][2] < lst[10][2]:
            change = 0
        if (lst[12][2] > lst[10][2])  and (lst[8][2] > lst[6][2]):
            pyautogui.hotkey('space')
            time.sleep(0.4)
        if (lst[12][2] < lst[10][2])  and (lst[8][2] < lst[6][2]) and (lst[16][2] < lst[14][2]) and (lst[20][2] < lst[18][2]):
            pyautogui.hotkey('win', 'd')
            time.sleep(0.3)

        if change:
            vol = np.interp(length,[18,150],[min,max])
            volume.SetMasterVolumeLevel(vol, None)
            change = 0
       

    cv2.imshow("webcam",hflip)
    key = cv2.waitKey(1)
    if key == 113:
        break