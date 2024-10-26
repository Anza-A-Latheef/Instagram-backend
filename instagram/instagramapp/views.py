# instagramapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import login
from rest_framework.permissions import AllowAny

from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import CreateSerializer

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken  # Make sure to import AccessToken


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'username': user.username,
                'email': user.email,
                'profile_picture_url': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate access and refresh tokens
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(access),
            "refresh": str(refresh),
            "username": user.username,
            "email": user.email,
            "user_id":user.id,
            'profile_picture_url': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,

        }, status=status.HTTP_200_OK)

class PostsViews(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()  
        serializer = CreateSerializer(posts, many=True, context={'request': request})  
        data = serializer.data
        
        for post in data:
            post['image'] = request.build_absolute_uri(post['image'])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = CreateSerializer(data=request.data,context={'request': request})
           
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(id=request.data['id']).delete()

        return Response("Sucessfully deleted", status=status.HTTP_200_OK)