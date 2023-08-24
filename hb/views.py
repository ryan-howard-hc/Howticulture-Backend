from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from corsheaders.middleware import CorsMiddleware
from django.views.decorators.http import require_POST

class PlantListViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantDetail(viewsets.ModelViewSet):
    queryset = Plant.objects.all().order_by('id')
    serializer_class = PlantSerializer

class UserCreateViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = ()
    
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data 
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserFavoritePlantsListViewSet(viewsets.ModelViewSet):
    queryset = UserFavoritePlants.objects.all()
    serializer_class = UserFavoritePlantsSerializer

class UserNotificationListViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer

class CommunityPostListViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
@api_view([ 'POST'])
def createPost(request):
    print(request)
    serializer = CommunityPostSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @require_POST
# def upload_file(request):
#     file = request.FILES['file']
#     with open('path/to/file', 'wb') as f:
#         f.write(file.read())
#     return HttpResponse('File uploaded successfully.')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_plant(request):
    try:
        user = request.user
        plant_id = request.data.get('plant_id')  # You need to send the plant_id from the frontend

        # Check if the plant already exists in favorites
        existing_favorite = UserFavoritePlants.objects.filter(user=user, plant_id=plant_id).first()

        if existing_favorite:
            return Response({"detail": "Plant already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new UserFavoritePlants entry
        plant = Plant.objects.get(pk=plant_id)
        user_favorite_plant = UserFavoritePlants(user=user, plant=plant)
        user_favorite_plant.save()

        return Response({"detail": "Plant added to favorites."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)