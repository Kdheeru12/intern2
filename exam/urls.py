from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('verification',views.verification,name='verification'),
    path('videorecording',views.videorecording,name='videorecording'),
    path('myvideos',views.myvideos,name='myvideos'),
    path('facedetection',views.faceidentificaton,name='facedection'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('edit',views.edit,name='edit'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='index.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),
            
]
