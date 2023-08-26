from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from corsheaders.middleware import CorsMiddleware
from django.views.decorators.http import require_POST
from django.conf import settings 
from dropbox import Dropbox, files


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
        try:
            user = self.get_object() 
            slug = request.data.get('slug')

            plant = Plant.objects.get(slug=slug)

            existing_favorite = UserFavoritePlants.objects.filter(user=user, plant=plant).first()

            if existing_favorite:
                return Response({"detail": "Plant already in favorites."}, status=status.HTTP_400_BAD_REQUEST)
            user_favorite_plant = UserFavoritePlants(user=user, plant=plant)
            user_favorite_plant.save()

            return Response({"detail": "Plant added to favorites."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CommunityPostListViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CommunityPostSerializer(queryset, many=True, context={'request': request})
        data = serializer.data

        # Exclude 'image' field from the response data
        for item in data:
            item.pop('image', None)

        return Response(data)


@api_view(['POST'])
def createPost(request):
    try:
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'user': None,
            'image_url': request.data.get('image_url'),  # Include the image URL
        }

        serializer = CommunityPostCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image_to_dropbox(image, filename):
    access_token = "sl.Bk0Cuvh1AMQUPB6VY62pKD-2NWzkMy3p9c1rpnbtrn9KnTL31knFSQfinkR6aMgodYoqtM2mnAgWL5ULmZKMtEgszTUyXhaKSUpK5qfAq_7XAYvjlzgxbzdQjQYUZKIKNQVd6gZagMpr" 

    dbx = Dropbox(access_token)
    with image.open('rb') as img_file:
        dbx.files_upload(img_file.read(), filename, mode=files.WriteMode('overwrite'))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCommunityPost(request):
    try:
        title = request.data.get('title')
        content = request.data.get('content')
        user_id = request.user.id
        postId = request.data.get('postId')
        image_url = request.data.get('image_url')  # Get the image URL from the request

        post = CommunityPost(title=title, content=content, user_id=user_id, postId=postId, image_url=image_url)

        # Save the post to the database.
        post.save()

        # Serialize the post data
        serializer = CommunityPostCreateSerializer(post, context={'request': request})

        # Return the serialized post data in the response
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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


@api_view(['POST'])
def save_slug(request):
    if request.method == 'POST':
        slug = request.data.get('slug')

        if slug:
            # You can save the slug to the database here, for example:
            # plant = Plant.objects.get(slug=slug)
            # plant.slug = slug
            # plant.save()

            return Response({'detail': 'Slug saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Slug is missing from the request data.'}, status=status.HTTP_400_BAD_REQUEST)