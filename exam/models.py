from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
)
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Video(models.Model):
    url = models.CharField(max_length=800)
class Profile(models.Model):
    user = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50,null=True,blank=True)
    school_city = models.CharField(max_length=50,null=True,blank=True)
    About_me = models.TextField(blank=True,null=True)
    Class = models.CharField(max_length=300,null=True,blank=True)
    Mobile = models.IntegerField(blank=True,null=True)
    school_name = models.CharField(max_length=300,null=True,blank=True)
    school_logo = models.ImageField(blank=True,null=True)
    school_address = models.TextField(blank=True,null=True)
    school_state = models.CharField(max_length=60,null=True,blank=True)
    school_country = models.CharField(max_length=80,null=True,blank=True)
    school_pincode = models.IntegerField(blank=True,null=True)
    school_contact_person = models.CharField(max_length=80,null=True,blank=True)
    school_email = models.EmailField(blank=True,null=True)
    school_mobile = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.firstname
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=80,null=True,blank=True)
    teacher_class = models.CharField(max_length=80,null=True,blank=True)
    teacher_mobile = models.IntegerField(blank=True,null=True)
    teacher_email = models.EmailField(blank=True,null=True)
    teacher_landline = models.IntegerField(blank=True,null=True)
    teacher_about_me = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.teacher_name
class Class(models.Model):
    Class_name = models.CharField(max_length=80,null=True,blank=True)
    Class_section = models.CharField(max_length=30,null=True,blank=True)
    Class_size = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.Class_name
class Students(models.Model):
    student_name = models.CharField(max_length=80,null=True,blank=True)
    student_class = models.CharField(max_length=80,null=True,blank=True)
    student_section = models.CharField(max_length=80,null=True,blank=True)
    student_email = models.CharField(max_length=80,null=True,blank=True)
    student_mobile = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.student_name


    
    