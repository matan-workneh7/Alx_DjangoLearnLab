from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Includes password validation and token creation.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
    
    def validate_email(self, value):
        """Validate that email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        """Create user and generate token."""
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(**validated_data)
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Generate token
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates credentials and returns token.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validate credentials and return user with token."""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError("Must include username and password.")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'date_joined', 'followers_count', 
            'following_count', 'is_following'
        )
        read_only_fields = ('id', 'date_joined', 'followers_count', 'following_count')
    
    def get_is_following(self, obj):
        """Check if current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
    def update(self, instance, validated_data):
        """Update user profile."""
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']
        
        instance.save()
        return instance


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user profile including extended profile information.
    """
    profile = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'date_joined', 'profile',
            'followers_count', 'following_count', 'is_following'
        )
        read_only_fields = ('id', 'date_joined', 'followers_count', 'following_count')
    
    def get_profile(self, obj):
        """Get extended profile information."""
        try:
            profile = obj.profile
            return {
                'website': profile.website,
                'location': profile.location,
                'birth_date': profile.birth_date,
                'is_verified': profile.is_verified
            }
        except UserProfile.DoesNotExist:
            return None
    
    def get_is_following(self, obj):
        """Check if current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class UserListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for user lists.
    """
    followers_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 
            'profile_picture', 'followers_count', 'is_following'
        )
    
    def get_is_following(self, obj):
        """Check if current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class ExtendedProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for extended user profile fields.
    """
    class Meta:
        model = UserProfile
        fields = ('website', 'location', 'birth_date')
        read_only_fields = ('is_verified',)


class FollowUserSerializer(serializers.Serializer):
    """
    Serializer for follow/unfollow actions.
    """
    user_id = serializers.IntegerField(required=True)
    
    def validate_user_id(self, value):
        """Validate that user exists and is not the current user."""
        try:
            user_to_follow = User.objects.get(id=value)
            request = self.context.get('request')
            if request and request.user == user_to_follow:
                raise serializers.ValidationError("You cannot follow yourself.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
