import mediapipe as mp
import cv2 as cv
import time

cap=cv.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
inTime=0
while True:
    # fps=cap.get(cv.CAP_PROP_FPS)
    outtime=time.time()
    fps=int(1/(outtime-inTime))
    inTime=outtime
    success,img=cap.read()
    img=cv.flip(img,1)
    h,w,c=img.shape

    imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                if id==4:
                    print(id,lm.x,lm.y)
                    # cv.circle(img, center_coordinates, radius, color, thickness)
                    # cv.circle(image, (int(w*lm.x,h*h*lm.y)), 1, (250,250,250), 1)
            mpDraw.draw_landmarks(img,handLms)
    image = cv.putText(img, str(fps), (20,40), cv.FONT_HERSHEY_SIMPLEX, 
                   0.5, (255,0,0), 1, cv.LINE_AA)

    # print(results.multi_hand_landmarks)
    cv.imshow('OUT',img)
    cv.waitKey(1)
