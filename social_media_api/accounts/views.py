from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db import models

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserProfileDetailSerializer, UserListSerializer, ExtendedProfileSerializer,
    FollowUserSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Returns authentication token upon successful registration.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user, context={'request': request}).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    API endpoint for user login.
    Returns authentication token upon successful login.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        # Login the user (optional, for session authentication)
        login(request, user)
        
        return Response({
            'user': UserProfileSerializer(user, context={'request': request}).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


class UserLogoutView(generics.GenericAPIView):
    """
    API endpoint for user logout.
    Deletes the authentication token.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Delete the user's token
            request.user.auth_token.delete()
            return Response(
                {'message': 'Successfully logged out.'},
                status=status.HTTP_200_OK
            )
        except Token.DoesNotExist:
            return Response(
                {'message': 'Already logged out.'},
                status=status.HTTP_200_OK
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveAPIView):
    """
    API endpoint for viewing detailed user profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


class UserListView(generics.ListAPIView):
    """
    API endpoint for listing users.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset


class FollowUserView(generics.GenericAPIView):
    """
    API endpoint for following/unfollowing users.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_to_follow_id = serializer.validated_data['user_id']
        user_to_follow = get_object_or_404(User, id=user_to_follow_id)
        
        if request.user.follow(user_to_follow):
            return Response({
                'message': f'You are now following {user_to_follow.username}',
                'is_following': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'You are already following {user_to_follow.username}',
                'is_following': True
            }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    API endpoint for unfollowing users.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_to_unfollow_id = serializer.validated_data['user_id']
        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'is_following': False
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'You are not following {user_to_unfollow.username}',
                'is_following': False
            }, status=status.HTTP_200_OK)


class UserFollowingListView(generics.ListAPIView):
    """
    API endpoint for listing users that the current user follows.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    
    def get_queryset(self):
        return self.request.user.user_following.all()


class UserFollowersListView(generics.ListAPIView):
    """
    API endpoint for listing users that follow the current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    
    def get_queryset(self):
        return self.request.user.followers.all()


class UpdateExtendedProfileView(generics.UpdateAPIView):
    """
    API endpoint for updating extended user profile information.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExtendedProfileSerializer
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """
    API endpoint to get current user information.
    """
    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_refresh_view(request):
    """
    API endpoint to refresh authentication token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user or not user.is_active:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create new token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserProfileSerializer(user, context={'request': request}).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request, user_id=None):
    """
    API endpoint to get user statistics.
    """
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user
    
    return Response({
        'followers_count': user.followers_count,
        'following_count': user.following_count,
        'date_joined': user.date_joined,
        'is_verified': user.profile.is_verified if hasattr(user, 'profile') else False
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user_view(request):
    """
    API endpoint to follow a user.
    Updates the following relationship.
    """
    serializer = FollowUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user_to_follow_id = serializer.validated_data['user_id']
    user_to_follow = get_object_or_404(User, id=user_to_follow_id)
    
    if request.user.follow(user_to_follow):
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'is_following': True
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': f'You are already following {user_to_follow.username}',
            'is_following': True
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user_view(request):
    """
    API endpoint to unfollow a user.
    Updates the following relationship.
    """
    serializer = FollowUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user_to_unfollow_id = serializer.validated_data['user_id']
    user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
    
    if request.user.unfollow(user_to_unfollow):
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'is_following': False
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': f'You are not following {user_to_unfollow.username}',
            'is_following': False
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def following_list_view(request):
    """
    API endpoint to get list of users that current user follows.
    """
    following_users = request.user.user_following.all()
    serializer = UserListSerializer(following_users, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def followers_list_view(request):
    """
    API endpoint to get list of users that follow current user.
    """
    followers_users = User.objects.all().filter(user_following=request.user)
    serializer = UserListSerializer(followers_users, many=True, context={'request': request})
    return Response(serializer.data)
