from imutils.video import FileVideoStream
from imutils.video import FPS

import sqlite3

#import backend
#import MMSCODE_tablice

from openalpr import Alpr
#import urllib
#import urllib.request

import cv2
import numpy as np
import sys
import os
import imutils
import time
from _datetime import datetime
import datetime

conn = sqlite3.connect('zaposleni.db')
cur = conn.cursor()
cur.execute('SELECT ime, prezime, tablice FROM data1')
data= cur.fetchall()

def check():
    with open('nova_lista.txt') as f:
        datafile = f.readlines()
    found = False 
    for line in datafile:
        if tablica in line:
            return True
    return False 

def make_480p():
    cam.set(3, 120)
    cam.set(4, 80)

def tablica(name):

    Vrijeme1=datetime.datetime.now()
    #print (name, "Vrijeme" , Vrijeme)

    with open("C:/Users/princ/Desktop/KOD/realtimeplates/Vrijeme.txt", "a") as text_file:
       text_file.write(name)
       text_file.write(" u vremenu: ")
       text_file.write(str(Vrijeme1)+"\n")    

#cam = cv2.VideoCapture('20200224_112104.mp4')
#cam = cv2.VideoCapture('rtsp://admin:Admin2020@192.168.100.64/')
#cam = cv2.VideoCapture('rtsp://admin:Admin2020@192.168.100.64/doc/page/preview.asp') 

#Web kamera
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#IP kamera
#url='http://192.168.100.3:8080/shot.jpg'
#url='http://192.168.0.52/'
#url='http://192.168.1.30/'
#cv2.namedWindow("test")
#time.sleep(1)

#Threding
# fvs = FileVideoStream('rtsp://admin:Admin2020@192.168.100.64/').start()
#fvs = FileVideoStream(0).start()

#Threding


car_cascade = cv2.CascadeClassifier('cars.xml')


alpr = Alpr("eu", "C:/Users/princ/Desktop/KOD/realtimeplates/openalpr.conf", "C:/Users/princ/Desktop/KOD/realtimeplates/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)



alpr.set_top_n(20)
#alpr.set_default_region("eu")
i = 0
counter_nothing = 0
plates_list_second_camera = []
confidences = []
count = 0
otvori1=0

#Threding
#while fvs.more():
#Threding

while True:
    #Prvi clucaj za IP kameru
    #imgResp=urllib.request.urlopen(url)
    #imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #frame=cv2.imdecode(imgNp,-1)

    #Drugi slucaj za web kameru
    ret, frame = cam.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    #Pronadji auta
    #cars = car_cascade.detectMultiScale(gray, 1.1, 1) 
    #for (x,y,w,h) in cars: 
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    

    #Threding
    # frame = fvs.read()
    # frame = imutils.resize(frame, width=450)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = np.dstack([frame, frame, frame])
    #Threding
    #cv2.putText(frame, plates_list_second_camera[ind], (30,60),cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,0),5,)
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    cv2.imshow("Parking system - Camera 2", frame)
    cv2.imwrite(str(i)+'_cam_2'+".jpg", frame)
    #frame = imutils.resize(frame, width=450)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = np.dstack([frame, frame, frame])
    
    results = alpr.recognize_file(str(i)+'_cam_2'+".jpg")
    
    #for plate in results["results"]:
    #    if plate not in plates:
    #        plates.append(plate["plate"])
    #        confidences.append(plate["confidence"])
    #    print(confidences[plates.index(plate["plate"])])
    #    confidences[plates.index(plate["plate"])] = confidences[plates.index(plate["plate"])] + plate["confidence"]
    
    
    plates = results["results"]
    
    #if plates in cars:

    if len(plates) > 0:
        for candidate in plates[0]['candidates']:
            if candidate["plate"] not in plates_list_second_camera:
                plates_list_second_camera.append(candidate["plate"])
                confidences.append(candidate["confidence"])
                continue
            confidences[plates_list_second_camera.index(candidate["plate"])] += candidate["confidence"]
  
#Kada naidje tablica slikaj i zapamti
    # for plate in plates:
    #     cv2.imwrite("./output/frame%d.jpg" % count, frame)
    #     count = count + 1
    #     continue
        


        #for(x,y,w,h) in plates:

            #cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
    k=cv2.waitKey(20) & 0xff
    if k==27:        
        break 
    Vrijeme_za_otvaranje_rampe=datetime.datetime.now()

    # dozvola=['BM602BT','K810367', 'ZG2286AF','K81O367','J68M017','J68MO17','M85J901',
    #         'E32A501','K63M058','JA999AA','K13M972','HVO644B','TA003175','K75O178',
    #         'EUFOR2009','794J231','O72O608','0720608','TA025722','TA025702','T49O716',
    #         'E31J673','SA5153HA','E67O143','K70A112','HA8088','K19O187','TA034279',
    #         'T94O598','40A003','DOBARDAN','SA3293GA','YOURTEXT','Y0URTEXT','E93M343',
    #         '038T140', '277A325','E36K925','K08O557','K080557','TA261238','E64M067',
    #         'K77M808','K72J765','T53K493','K13M970','A52T150','TA168301','236M125',
    #         'SA345555','138J460','166K122','792K000','M48E415','TA003175','E41M530',
    #         '014T858','O83T259','083T259','075M311','SA98248','A00A000','AOOA000',
    #         'OSCE006MB','735T833','268M923','TA003175','A54M083','ZG2649FZ','A12A345']
    # #data=open('dozvola.csv', 'r+')
    if (not plates):
        counter_nothing += 1
    else:
        counter_nothing = 0

    if (counter_nothing == 1):
        plates_list_second_camera = []
        confidences = []
        counter_nothing = 0
    try:
        ind = confidences.index(max(confidences))
        #print(ind)
        print(' '+str(plates_list_second_camera[ind]))
        

        if str(plates_list_second_camera[ind]) in str(data):
            if otvori1==10:
                print("Otvori rampu za tablice:", str(plates_list_second_camera[ind]))
                #print(str(data[0]))

                time.sleep(8)

                
                with open('Vrijeme_nailaska-izlaz.txt','a+') as text:
                    text.write(str(plates_list_second_camera[ind]))
                    text.write(" u vremenu: ")
                    text.write(str(Vrijeme_za_otvaranje_rampe)+"\n")  
                otvori1=0
                continue
            else:
                otvori1+=1
        else:
            #print("Nisi ovlasten da pristupis:", str(plates_list_second_camera[ind]))
            print(' -------------------- ')
            #tablica(str(plates_list_second_camera[ind]))
        continue

    except:
        pass
    os.remove(str(i)+'_cam_2'+".jpg")
    #print(results)
    k = cv2.waitKey(1)
    i = i + 1

"""
Vrijeme=datetime.datetime.now()

if str(plates_list_second_camera) in open('Vrijeme.txt').read():
        Tablica(str(plates_list_second_camera))
"""
i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"

        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

"""
while True:
    k=cv2.waitKey(20) & 0xff
    if k==27:        
        break        
"""

# Call when completely done to release memory
alpr.unload()
cam.release()
cv2.destroyAllWindows()
#fvs.stop()