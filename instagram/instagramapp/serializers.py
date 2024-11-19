from .models import UserProfile,Post  
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Comment  


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password','first_name', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        user = UserProfile(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        request = self.context.get('request')
        if user.profile_picture:
            user.profile_picture_url = request.build_absolute_uri(user.profile_picture.url)
        else:
            user.profile_picture_url = None  
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            try:
                user = authenticate(username=self.get_user_by_email(username), password=password)
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs

    def get_user_by_email(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.get(email=email).username


 
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id','user', 'post', 'content','username']


class CreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.ImageField(source='user.userprofile.profile_picture', read_only=True)
    is_same_user=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    profile_picture=serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True) 

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    def get_is_same_user(self,obj):
        return True if self.context['request'].user == obj.created_by else False
    
    def get_user(self,obj):
        return obj.created_by.username

    def get_profile_picture(self,obj):
        return obj.created_by.profile_picture.url


    class Meta:
        model = Post
        fields = ('id','caption','image','created_at','user','username','profile_picture','created_by','is_same_user', 'comments')
        read_only_fields = ['created_by']
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    

