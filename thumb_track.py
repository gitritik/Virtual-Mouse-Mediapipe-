import mediapipe as mp
import cv2 as cv
import time
import pyautogui
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os


sc_w=1920
sc_h=1080


print(pyautogui.size())
cap=cv.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
inTime=0

isClicked=False
isrClicked=False

altmode=False

altcooltime=0


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetVolumeRange()
minVol=volume.GetVolumeRange()[0]
maxVol=volume.GetVolumeRange()[1]
fps=cap.get(cv.CAP_PROP_FPS)
while True:
    outtime=time.time()
    fps=int(1/(outtime-inTime))
    inTime=outtime
    # fps=cap.get(cv.CAP_PROP_FPS)
    success,img=cap.read()
    img=cv.flip(img,1)
    h,w,c=img.shape

    imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                if id==20:
                    # print(lm.x,lm.y)
                    # cv.circle(img, (int(w*lm.x),int(h*lm.y)), 1, (250,250,250), 1)
                    if lm.x<0.8*w and lm.y<0.8*h:
                        pyautogui.moveTo(abs(int(1920*lm.x/0.8)),abs(int(1080*lm.y/0.8)))
            thumb=handLms.landmark[4]
            index=handLms.landmark[8]
            middle=handLms.landmark[12]
            ring=handLms.landmark[16]
            pinky=handLms.landmark[20]

            # thumb_ind_dis=(((thumb.x-index.x)*w)**2+((thumb.y-index.y)*h)**2)**0.5
            # thumb_mid_dis=(((thumb.x-middle.x)*w)**2+((thumb.y-middle.y)*h)**2)**0.5
            # thumb_ring_dis=(((thumb.x-ring.x)*w)**2+((thumb.y-ring.y)*h)**2)**0.5
            # thumb_pinky_dis=(((thumb.x-pinky.x)*w)**2+((thumb.y-pinky.y)*h)**2)**0.5
            diag=math.hypot(h,w)
            thumb_ind_dis=math.hypot(((thumb.x-index.x)*w),((thumb.y-index.y)*h))
            thumb_mid_dis=math.hypot(((thumb.x-middle.x)*w),((thumb.y-middle.y)*h))
            thumb_ring_dis=math.hypot(((thumb.x-ring.x)*w),((thumb.y-ring.y)*h))
            thumb_pinky_dis=math.hypot(((thumb.x-pinky.x)*w),((thumb.y-pinky.y)*h))
            print(thumb_mid_dis)
            if not altmode:
                if thumb_ind_dis<0.03*diag:
                    if not isClicked:
                        pyautogui.click(abs(int(1920*lm.x/0.8)),abs(int(1080*lm.y/0.8)))
                        isClicked=True
                elif thumb_ind_dis>0.05:
                    isClicked=False
                
                if thumb_mid_dis<0.03*diag:
                    if not isrClicked:
                        pyautogui.rightClick(abs(int(1920*lm.x/0.8)),abs(int(1080*lm.y/0.8)))
                        isrClicked=True
                elif thumb_mid_dis>0.05*diag:
                    isrClicked=False

            if thumb_ring_dis<0.03*diag:
                if altcooltime>3:
                    altmode=not(altmode)
                    altcooltime=0

            if thumb_ind_dis>0.08*diag and fps!=0:
                altcooltime+=(1/fps)
            
            if altmode:
                cv.line(img,(int(thumb.x*w),int(thumb.y*h)),((int(index.x*w),int(index.y*h))),(0,255,0),3)
                cv.line(img,(int(thumb.x*w),int(thumb.y*h)),((int(middle.x*w),int(middle.y*h))),(0,0,255),3)

                vol=np.interp(thumb_ind_dis,[15,125],[minVol,maxVol])
                bright=np.interp(thumb_mid_dis,[20,200],[0,100])
                os.system('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{})'.format(bright))
                # print(vol)
                # volume.GetMute()
                # volume.GetMasterVolumeLevel()
            # print(volume.GetVolumeRange())
                volume.SetMasterVolumeLevel(vol, None)
                









            
            




            mpDraw.draw_landmarks(img,handLms)
    img = cv.putText(img, str(fps), (20,40), cv.FONT_HERSHEY_SIMPLEX, 
                   0.5, (255,0,0), 1, cv.LINE_AA)
    cv.imshow('OUT',img)
    cv.waitKey(1)
