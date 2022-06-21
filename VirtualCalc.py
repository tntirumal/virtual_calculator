#this is a mini project by Tirumal and Monish
import cv2,os
from cvzone.HandTrackingModule import HandDetector
import pyttsx3

#create speak module
def speak(content):
        '''eng=pyttsx3.init()
        eng.setProperty('rate',100)
        eng.say(content)
        eng.runAndWait()'''
        os.system("espeak "+content)

def pspeak(content):
        eng=pyttsx3.init()
        eng.setProperty('rate',150)
        eng.say(content)
        eng.runAndWait()

#create Button class
class Button:
    def __init__(self,pos,width,height,value):
        super().__init__()

        self.position=pos
        self.width=width
        self.height=height
        self.value=value
        
    
    def  draw(self,img):
        '''
        create a box to fill the number box for the calculator
        location where the box is to be palced -->img
        height of the box                      -->(hhh,hhh)
        width of the box                       -->(www,www)
        color of the box                       -->(ccc,ccc,ccc)
    '''

        cv2.rectangle(img,self.position,(self.position[0]+self.width,self.position[1]+self.height),(150,150,150),cv2.FILLED)
        cv2.rectangle(img,self.position,(self.position[0]+self.width,self.position[1]+self.height),(50,50,50),3)#outline
        cv2.putText(img,self.value,(self.position[0]+20,self.position[1]+30),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50))
    
    def checkClick(self,x,y):
        #check x axis and y axis for defining position...
        if self.position[0]<x<self.position[0]+self.width and self.position[1]<y<self.position[1]+self.width:
            cv2.rectangle(img,self.position,(self.position[0]+self.width,self.position[1]+self.height),(255,255,255),cv2.FILLED)
            cv2.rectangle(img,self.position,(self.position[0]+self.width,self.position[1]+self.height),(50,50,50),3)
            cv2.putText(img,self.value,(self.position[0]+20,self.position[1]+30),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)
                        

            return  self.value
    

#capture the video and set frames....
capture=cv2.VideoCapture(0)
capture.set(3,1080)#size
capture.set(4,720)#height
detector=HandDetector(detectionCon=0.8,maxHands=1)#detector object for hand detector

#creating button objects...
b1=Button((23,112),50,50,'1')
b2=Button((77,112),50,50,'2')
b3=Button((134,112),50,50,'3')
ba=Button((187,112),50,50,'+')
b4=Button((24,167),50,50,'4')
b5=Button((79,167),50,50,'5')
b6=Button((136,167),50,50,'6')
bs=Button((188,167),50,50,'-')
b7=Button((27,221),50,50,'7')
b8=Button((78,221),50,50,'8')
b9=Button((135,221),50,50,'9')
be=Button((187,221),50,50,'=')
bm=Button((25,276),50,50,'*')
b0=Button((80,276),50,50,'0')
bd=Button((131,276),50,50,'/')
bc=Button((184,276),50,50,'C')


#variables
myEquation=''
delaycounter=0
buttonList=[b1,b2,b3,ba,b4,b5,b6,bs,b7,b8,b9,be,b0,bd,bc,bm]



while True:
    success,img=capture.read()
    
    #Hand detection
    hands, img = detector.findHands(img)  # with draw
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        fingers1 = detector.fingersUp(hand1)
    
        
    #draw buttons on screen
    for i in buttonList:
        i.draw(img)

    #processing check for hands

    if hands:
        lmList=hands[0]['lmList']
        length, _,img=detector.findDistance(lmList[8][0:2],lmList[12][0:2],img)
        #print(length)
        x,y=lmList[8][0:2]
        
        print(length)

        if length<50:#for clicking
            
            for i in buttonList:
                if i.checkClick(x,y) and  delaycounter==0:
                    myvalue=i.checkClick(x,y)
                    
                    try:
                        if myvalue == '=':
                            ans=str(eval(myEquation))
                            
                            pspeak("the result of "+myEquation+"is"+ans)
                            myEquation=ans
                            #myEquation=''
                            
                            
                            

                    except:
                        print("error statement")
                        continue
                    if myvalue == 'C':
                        speak("cleared")
                        myEquation= ''
                    else:
                        if myvalue == '=':
                            continue
                        speak(myvalue)
                        myEquation+=myvalue
                    delaycounter=1

    #avoid duplicates
    if  delaycounter !=0:
        delaycounter+=1
        if delaycounter>5:
            delaycounter=0

    #display result
    
    cv2.putText(img,myEquation,(23,88),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),3)

    #display image
    cv2.imshow("Virtual Calculator",img)
    cv2.waitKey(1)