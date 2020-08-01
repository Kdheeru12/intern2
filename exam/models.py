from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.db.models.fields import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
)
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Video(models.Model):
    url = models.CharField(max_length=800)