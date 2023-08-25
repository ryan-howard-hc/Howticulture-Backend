from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings 

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

class UserFavoritePlants(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
 
    
class CommunityPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)