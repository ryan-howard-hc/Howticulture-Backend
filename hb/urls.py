from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers, viewsets
from .views import *
from . import views
from rest_framework.response import Response

from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'user-favorite-plants', UserFavoritePlantsListViewSet)
router.register(r'community-posts', CommunityPostListViewSet)
router.register(r'user-posts', UserPostListViewSet, basename='user-posts') 


urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', UserDetailViewSet.as_view({'get': 'retrieve'}), name="user_detail"), 
    path('user/signup/', UserCreateViewSet.as_view(), name="create_user"),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),

    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('add-favorite-plant/',views.add_favorite_plant, name="add_favorite_plant"), 
    path('user-favorite-plants/<int:pk>/', UserFavoritePlantsListViewSet.as_view({'get': 'list'}), name="user_favorite_plants_detail"), 

    path('api/save-slug/', save_slug, name='save_slug'),

    path('community-posts/<int:pk>/', CommunityPostListViewSet.as_view({'get':'list'})), 
    path('create-community-posts/',views.createCommunityPost), 
    path('user-posts/<int:user_id>/', UserPostListViewSet.as_view({'get': 'list', 'post': 'create'}), name="user_posts"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)