from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
