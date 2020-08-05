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
    schoolName = models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    About_me = models.TextField(blank=True,null=True)
    Class = models.CharField(max_length=300,null=True,blank=True)
    Mobile = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.firstname
    
    
    