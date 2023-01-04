# from app import extract
import time
import cv2
import numpy as np
import os 
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
import pymongo

def recog():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    start_time = time.time()
    count=0

    while True:
        ret, img =cam.read()
    # img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor = 1.2,minNeighbors = 5,minSize = (int(minW), int(minH)),)
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
            # If confidence is less them 100 ==> "0" : perfect match 
            if (confidence < 100):
                id = int(id)
                #id = names[id]
                print("correct")
                print(id)
                id=extract(str(id))
                print("correct")
                count=count+1
                print(id)
                confidence = "  {0}%".format(round(100 - confidence))
                break
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                count=count+1
            cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
            cv2.putText(img, str(confidence),(x+5,y+h-5),font,1,(255,255,0),1) 
            
        else:
            break 
    
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 1: # Take 30 face sample and stop video
            break
# Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()




def extract(phoneno):
    # myclient = pymongo.MongoClient("mongodb+srv://saikiran:Epm9durTM8SzJcg@cluster0.s2wlw.mongodb.net")
    # mydb = myclient["attendence_db"]
    # mycol = mydb["user"]
    # myquery = { "phoneno":phoneno }
    # #mydoc = mycol.find({},myquery)
    # #print(mydoc)
    # # for x in mycol.find():
    # #     print(x['name'])
    # #     x['count'] = int(x['count'])+1
    # #     #mycol.insert_one(x)
    # #mycol.update_one(myquery, {"$set": { "count": x['count'] }} )
    # mydoc = mycol.find({},myquery)
    # mycol.update_one(myquery, {"$set": { "count": mydoc[0]['count']+1 }} )
    # return mydoc['name']
    myclient = pymongo.MongoClient("mongodb+srv://saikiran:Epm9durTM8SzJcg@cluster0.s2wlw.mongodb.net")
    mydb = myclient["attendence_db"]
    mycol = mydb["user"]
    myquery = { "phoneno":phoneno }
    #mydoc = mycol.find({},myquery)
    #print(mydoc)
    # for x in mycol.find():
    #     print(x['name'])
    #     x['count'] = int(x['count'])+1
    #     #mycol.insert_one(x)
    #mycol.update_one(myquery, {"$set": { "count": x['count'] }} )
    mydoc = mycol.find(myquery)

    mydoc = mydoc[0]
    print("--------------------")
    print(mydoc)
    count1 = int(mydoc['count'])+1
    mycol.update_one({'_id': mydoc['_id']}, {"$set": { "count": str(count1)  }} )
    return mydoc['name']