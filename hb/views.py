from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


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
    @action(detail=True, methods=['post'])
    def add_favorite_plant(self, request, pk=None):
        # Assuming you're passing the plant ID in the request data as 'plant_id'
        plant_id = request.data.get('plant_id')
        user = self.get_object()  # Get the user based on the user ID in the URL
        
        try:
            # Check if the user already has this plant in favorites
            existing_favorite = UserFavoritePlants.objects.filter(user=user, plant_id=plant_id).exists()

            if existing_favorite:
                return Response({'message': 'Plant is already in favorites.'}, status=400)

            # Create a new UserFavoritePlants instance
            favorite_plant = UserFavoritePlants(user=user, plant_id=plant_id)
            favorite_plant.save()

            return Response({'message': 'Plant added to favorites successfully'}, status=201)
        except Exception as e:
            return Response({'message': 'Failed to add plant to favorites.', 'error': str(e)}, status=500)

class UserNotificationListViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer

class CommunityPostListViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

@api_view([ 'POST'])
@authentication_classes([])
def createPost(request):
    print(request)
    serializer = CommunityPostSerializer(data=request.data)
    if serializer.is_valid():
        user = self.request.user
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([])
# def createCommunityPost(request):
#     serializer = CommunityPostSerializer(data=request.data, context={'request': request})

#     if serializer.is_valid():
#         # Get the user from the request
#         user = request.user

#         # Check if the user is authenticated
#         if user.is_authenticated:
#             serializer.save(user=user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @api_view(['POST'])
# @authentication_classes([TokenAuthentication])  # Use TokenAuthentication for token-based auth
# @permission_classes([IsAuthenticated])  # Use IsAuthenticated to require authentication
# def createCommunityPost(request):
#     # The user object is accessible via request.user if authenticated
#     user = request.user

#     # You can also access the Authorization header to extract the token
#     authorization_header = request.META.get('HTTP_AUTHORIZATION')

#     if user.is_authenticated:
#         # Access token successfully extracted and user is authenticated
#         serializer = CommunityPostSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCommunityPost(request):
    serializer = CommunityPostSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @require_POST
# def upload_file(request):
#     file = request.FILES['file']
#     with open('path/to/file', 'wb') as f:
#         f.write(file.read())
#     return HttpResponse('File uploaded successfully.')


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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