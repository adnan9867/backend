from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from user_module.models import *


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
    likes_count = serializers.SerializerMethodField('get_like')
    dislike_count = serializers.SerializerMethodField('get_dislike')

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
            likes = PostLikeDislike.objects.filter(reaction__iexact='Like',  post__id=obj.id)
            return likes.count()
        except:
            return None

    def get_dislike(self, obj):
        try:
            dislike = PostLikeDislike.objects.filter(reaction__iexact='Dislike', post__id=obj.id)
            return dislike.count()
        except:
            return None


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeDislike
        fields = '__all__'

    def create(self, validated_data):
        obj = PostLikeDislike.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        if validated_data.get('reaction') == 'Like' and instance.reaction == 'Like':
            raise serializers.ValidationError(_('Post is already liked'))
        if validated_data.get('reaction') == 'Dislike' and instance.reaction == 'Dislike':
            raise serializers.ValidationError(_('Post is already disliked'))
        if instance.reaction == 'Like' and validated_data.get('reaction') == 'Dislike':
            instance.reaction = 'Dislike'
            instance.save()

        if instance.reaction == 'Dislike' and validated_data.get('reaction') == 'Like':
            instance.reaction = 'Like'
            instance.save()
        return instance
