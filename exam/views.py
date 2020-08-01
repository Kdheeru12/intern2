from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
import random
import requests
from django.db import models
from .models import Video
import shutil
import os
import numpy as np
import cv2
import face_recognition
import os
from datetime import datetime
def homepage(request):
    return render(request,'1.html')

# Create your views here.
def videorecording(request):
    if request.method == 'POST':
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y.%H.%M.%S")
        import socket
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        print("Your Computer IP Address is:" + IPAddr)
        
        filename = str(IPAddr)+str(dt_string)+'.avi'
        filename1 = str(IPAddr)+str(dt_string)+'.mp4'
        print(type(filename),type(filename1))
        print(filename1,filename)
        frames_per_seconds = 24.0
        myres = '720p'
        def change_res(cap, width, height):
            cap.set(3, width)
            cap.set(4, height)

        STD_DIMENSIONS =  {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        def get_dims(cap,res='1080p'):
            width,height = STD_DIMENSIONS['480p']
            if res in STD_DIMENSIONS:
                width,height = STD_DIMENSIONS[res]
                change_res(cap,width,height)
                return width,height
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
        def get_video_type(filename):
            path = ''
            filename, ext = os.path.splitext(filename)
            if ext in VIDEO_TYPE:
                return  VIDEO_TYPE[ext]
            return VIDEO_TYPE['avi']
        cap = cv2.VideoCapture(0) 
        dims = get_dims(cap,res=myres)
        VIDEO_TYPE_cv2 = get_video_type(filename)
        out = cv2.VideoWriter(filename,VIDEO_TYPE_cv2,frames_per_seconds,dims)
        while(True): 
            
            # Capture the video frame 
            # by frame 
            ret, frame = cap.read()

            out.write(frame)
            # Display the resulting frame 
            cv2.imshow('frame', frame) 
            
            # the 'q' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

        # After the loop release the cap object 
        cap.release() 
        # Destroy all the windows 
        out.release()
        cv2.destroyAllWindows()
        import moviepy.editor as moviepy
        clip = moviepy.VideoFileClip(filename)
        clip.write_videofile(filename1)
        os.remove(filename)
        files = [filename1]
        for f in files:
            shutil.move(f, 'media')
        deo = Video(url=filename1)
        deo.save()
        return redirect('/myvideos')
    return render(request,'video.html')

def myvideos(request):
    video=Video.objects.all()
    print(video)
    return render(request,'myvideos.html',{'video':video})
def faceidentificaton(request):
    
    path = 'imagesbasic'

    images = []
    classnames = []
    mylist = os.listdir(path)
    print(mylist)

    for cl in mylist:
        curimg = cv2.imread(f'{path}/{cl}')
        images.append(curimg)
        classnames.append(os.path.splitext(cl)[0])
    print(classnames)
    def findEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist
    def markAttendance(name):
        with open('attandance.csv','r+') as f:
            myDatalist = f.readlines()
            namelist = []
            for line in myDatalist:
                entry = line.split(',')
                namelist.append(entry[0])
            if name not in namelist:
                now = datetime.now()
                dtstring = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtstring}')

    encodelistknown = findEncodings(images)
    print(len(encodelistknown))
    cap = cv2.VideoCapture(0)
    notfound = 0
    while(True):
        success,img = cap.read()
        imgs = cv2.resize(img,(0,0),None,0.25,0.25)
        imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgs)
        encodesCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)
        for encodeface,faceloc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodelistknown,encodeface)
            facedis = face_recognition.face_distance(encodelistknown,encodeface)
            print(facedis)
            matchindex = np.argmin(facedis)
            if matches[matchindex]:
                name = classnames[matchindex].upper()
                print(name)
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
            else:
                notfound = notfound + 1
                ntfund = str(notfound)
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,'notfound'+ntfund,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        try:
            if notfound == 10:
                break
        except:
            pass
        cv2.imshow('webcam',img)
        cv2.waitKey(1)
    if notfound == 10:
        return render(request,'notrec.html')
    else:
        return redirect('/myvideos')
