from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from user_module.models import User, Post


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'full_name', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
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
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at')
