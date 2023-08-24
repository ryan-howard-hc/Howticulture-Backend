from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import *
from . import views
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'plants', PlantListViewSet)
router.register(r'user-favorite-plants', UserFavoritePlantsListViewSet)
router.register(r'user-notifications', UserNotificationListViewSet)
router.register(r'community-posts', CommunityPostListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', UserDetailViewSet.as_view({'get': 'retrieve'}), name="user_detail"),  # Example: /user/1/

    path('user/signup/', UserCreateViewSet.as_view(), name="create_user"),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('plant/<int:pk>/', PlantDetail.as_view({'get': 'list'}), name="plant_detail"), 
    path('user-favorite-plants/<int:pk>/', UserFavoritePlantsListViewSet.as_view({'get': 'list'}), name="user_favorite_plants_detail"), 
    
    path('user-favorite-plants/<int:pk>/add-favorite-plant/', UserFavoritePlantsListViewSet.as_view({'post': 'add_favorite_plant'}), name="add_favorite_plant"),

    # path('user-notifications/<int:pk>/', UserNotificationListViewSet.as_view({'get': 'list'}), name="user_notification_detail"),  # Example: /user-notifications/1/
    path('community-posts/<int:pk>/', CommunityPostListViewSet.as_view({'get':'list'})), 
    path('create-community-posts/',views.createCommunityPost), 

]