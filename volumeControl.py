import os
import time 
import cv2
import matplotlib.pyplot as plt
import numpy as np
import hand_tracking_module as htm 
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
#Min=-65.25, Max=0.0
a=cv2.VideoCapture(0)
detector=htm.handDetector()
length=0
vol=0
bar=400
percentage=0
while(True):
    success,img=a.read()
    img= cv2.flip(img, 1)
    image=detector.findHands(img,draw=False)
    lmList=detector.findPosition(img)
    if lmList:
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(0,255,0),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(0,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        Min=-65.25
        Max=0.0
        length=math.hypot(x2-x1,y2-y1)
        #print(length)
        vol=np.interp(length,[20,180],[Min,Max])
        bar=np.interp(length,[20,180],[400,150])
        percentage=np.interp(length,[20,180],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(bar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,(f'{int(percentage)}%'),(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(20,20,20),3)
    cv2.imshow("img",image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break