import cv2
print(cv2.__version__)
import random as rm

class mphands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
    def marks(self,frame):
        myHands=[]
        handsType=[]
        rgbFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(rgbFrame)
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*640),int(landMark.y*360)))
                myHands.append(myHand)
        return myHands,handsType



def loc():
    x=rm.choice([3,-3])
    y=rm.choice([3,-3])
    return x,y
leftPos=(0,0)
rightPos=(0,0)
leftPaddleH=64
leftPaddleW=10
rightPaddleH=64
rightPaddleW=10
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
handFinder=mphands()
a,b=loc()
x=320
y=180
rScore=0
lScore=0
while True:
    ignore,  frame = cam.read()
    handsData,handsType=handFinder.marks(frame)
    for hand,handType in zip(handsData,handsType):
        if handType=="Left":
            leftPos=hand[8]
            print(leftPos)
            print(y)
            cv2.rectangle(frame,(0,leftPos[1]-32),(10,leftPos[1]+32),(0,0,255),-1)
        if handType=="Right":
            rightPos=hand[8]
    cv2.rectangle(frame,(0,leftPos[1]-32),(10,leftPos[1]+32),(0,0,255),-1)
    cv2.rectangle(frame,(630,rightPos[1]-32),(width,rightPos[1]+32),(0,0,255),-1)

    cv2.circle(frame,(x,y),8,(0,0,255),-1)
    if (x-8<=leftPaddleW and x-8>=0 and leftPos[1]-32<=y and leftPos[1]+32>=y) or (x+8>=640-rightPaddleW and x+8<=640 and rightPos[1]-32<=y and rightPos[1]+32>=y):

        a*=-1
        print("EHDUIO")

    x=x+a
    y=y+b
    if y-8<0 or y+8>360:
        b*=-1
        y+=b
        print("HTI")
    if x<0:
        a,b=loc()
        x=320
        y=rm.randint(0,360)
        rScore+=1
    if x>640:
        a,b=loc()
        x=320
        y=rm.randint(0,360)
        lScore+=1
    cv2.putText(frame,"Left Score: {}".format(lScore),(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1)
    cv2.putText(frame,"Right Score: {}".format(rScore),(300,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1)









    cv2.imshow('my WEBcam',frame)
    cv2.moveWindow('my WEBcam',0,0)

    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()