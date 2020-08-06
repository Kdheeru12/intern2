from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile
from .models import Teacher
from .models import Class
from .models import Students
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
from django.core.mail import send_mail,BadHeaderError
from .form import ProfileForm
from .form import SchoolForm
def homepage(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile,user=str(request.user))
        print(profile)
        context={
            'profile':profile
        }
        return render(request,'index.html',context)
    else:
        return redirect('/signup')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        schoolname =request.POST['schoolname']
        city = request.POST['city']
        globals()['first_name']=first_name
        globals()['last_name']=last_name
        globals()['email'] = email
        globals()['password']= password
        globals()['schoolname']=schoolname
        globals()['city']= city
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email Already exist')
            return redirect('signup')
        else:
            print('aaa')
            otp = random.randint(100000,999999)
            #user = User.objects.create_user(username=phonenumber,password=password,email=email,first_name=first_name,last_name=last_name)
            #user.save()
            globals()['otp']=otp
            subject = 'Regarding Login To The Site'
            message = 'Hello'+str(first_name)+'Otp For Login Is:'+str(otp)
            sender = 'hello@shunya.tech'
            recipients = [email]
            send_mail(subject,message,sender,recipients)
            return redirect('verification')
        return render(request,'register.html')
    else:
        return render(request,'register.html')
# Create your views here.
def verification(request):
    if request.method == 'POST':
        email_otp = int(request.POST['otp'])
        try:
            user=User.objects.filter(email=email).exists()
            print(otp)
            otp is not None
        except:
            return redirect('signup')
        print(user)
        if email_otp == otp and user == False:
            messages.info(request,'otp verified')
            user = User.objects.create_user(username=email,password=password,email=email,first_name=first_name,last_name=last_name)
            user_profile = Profile(user=email,firstname=first_name,lastname=last_name,school_name=schoolname,school_city=city)
            user.save()
            user_profile.save()
            return redirect('login')
        elif user == True:
            messages.info(request,'user already verified')
            return redirect('login')
        else:
            messages.info(request,'otp invalid')
            return redirect('verification')
    else:
        return render(request,'verification.html')
def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'invalid phone or password')
            return redirect('/login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'login.html')
def profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile,user=str(request.user))
        print(profile)
        instance = get_object_or_404(Profile,user=str(request.user))
        form = ProfileForm(request.POST or None,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('/profile')
        context={
            'profile':profile,
            'form':form
        }
        return render(request,'profile.html',context)
    else:
        return redirect('login')
def logout(request):
    auth.logout(request)
    return redirect('homepage')
def settings(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Profile,user=str(request.user))
        context={
                'instance':instance,
            }
        return render(request,'settings.html',context)
    else:
        return redirect('/')
def settingsedit(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Profile,user=str(request.user))
        form = SchoolForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('/settings')
        context={
            'form':form
        }
        return render(request,'settings-edit.html',context)
    else:
        return render(request,'settings.html')
def teachers(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['mobile']
        email = request.POST['email']
        teacher = Teacher.objects.filter(teacher_name=name,teacher_class=clas,teacher_mobile=mobile,teacher_email=email)
        teacher.delete()
        return redirect('/teachers')
    else:
        teacher = Teacher.objects.all()
        print(teacher)
        return render(request,'teachers.html',{'teacher':teacher})
def teachersadd(request):
    if request.method == 'POST': 
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['mobile']
        email = request.POST['email']
        landline = request.POST['landline']
        aboutme = request.POST['aboutme']
        teacher = Teacher(teacher_name=name,teacher_class=clas,teacher_mobile=mobile,teacher_email=email,teacher_landline=landline,teacher_about_me=aboutme)
        teacher.save()
        return redirect('/teachers')
    else:
        clas = Class.objects.all()
        return render(request,'teachers-add.html',{'clas':clas})
def Classes(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        section = request.POST['section']
        print(clas,section,name)
        Clas = Class.objects.filter(Class_name=clas,Class_section=section)
        print(clas)
        Clas.delete()
        return redirect('/classes')
    else:
        clas = Class.objects.all()
        return render(request,'classes.html',{'clas':clas})
def Classesadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        section = request.POST['section']
        clas = Class(Class_name=name,Class_section=section)
        clas.save()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/classes')
    else:
        teacher = Teacher.objects.all()
        return render(request,'classes-add.html',{'teacher':teacher})
def students(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        section = request.POST['section']
        students = Students.objects.filter(student_class=clas,student_name=name,student_section=section)
        students.delete()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/students')
    else:
        students = Students.objects.all() 
        return render(request,'students.html',{'students':students})
def studentsadd(request):
    if request.method == 'POST':
        name = request.POST['name']
        clas = request.POST['class']
        mobile = request.POST['number']
        email = request.POST['email']
        section = request.POST['section']
        students = Students(student_name=name,student_section=section,student_class=clas,student_mobile=mobile)
        students.save()
        studentcount = Students.objects.filter(student_section=section,student_class=clas).count()
        instance = get_object_or_404(Class,Class_name=clas,Class_section=section)
        instance.Class_size = int(studentcount)
        instance.save()
        return redirect('/students')
    clas = Class.objects.all()
    return render(request,'students-add.html',{'clas':clas})
def edit(request):
    instance = User.objects.filter(username='kdheerureddy@gmail.com')
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
