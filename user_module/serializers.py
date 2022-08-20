from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from user_module.models import *
from user_module.utils import user_holiday_info


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'full_name', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        if User.objects.filter(email=validated_data['email']).exists():  # get user by email
            raise serializers.ValidationError(_('Email already exists'))  # raise error if email already exists
        if User.objects.filter(username=validated_data['username']).exists():  # get user by username
            raise serializers.ValidationError(_('Username already exists'))  # raise error if username already exists
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone']
        )  # create user
        user.set_password(validated_data['password'])  # set password
        user.save()
        user_holiday_info(user=user, request=request)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone')


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField('get_like')

    class Meta:
        model = Post
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context['request']
        if not instance.author.id == request.user.id:
            raise serializers.ValidationError(_('You are not author'))
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance

    def get_like(self, obj):
        try:
            likes = PostLikes.objects.filter(post__id=obj.id)
            return likes.count()
        except:
            return None


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'
