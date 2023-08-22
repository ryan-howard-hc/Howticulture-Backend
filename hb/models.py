from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    def __str__(self):
        return self.email
#---------------------------------------
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    # username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    date_registered = models.DateTimeField()