from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('videorecording',views.videorecording,name='videorecording'),
    path('myvideos',views.myvideos,name='myvideos'),
    path('facedetection',views.faceidentificaton,name='facedection'),

]
