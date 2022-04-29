from djoser.serializers import UserCreateSerializer
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from backend.models import Post, Profile, CommentPost, ReplyCommentPost, PhotoPost

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    REQUIRED_FIELDS = ['first_name']

    def create(self, validated_data):
        uname = validated_data['username']
        password = validated_data['password']
        if validated_data.get('first_name'):
            first_name = validated_data['first_name']
        else:
            first_name = ''
        if validated_data.get('last_name'):
            last_name = validated_data['last_name']
        else:
            last_name = ''
        if validated_data.get('email'):
            email = validated_data['email']
        else:
            raise ValidationError('E-mail объязательно')
        user = get_user_model().objects.create(
            username=uname,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'type', 'date_of_birth', 'photo']

        # поля только для чтения
        read_only_fields = ['user', 'type']


class ReplyCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyCommentPost
        fields = ['id', 'user', 'comment', 'description', 'status', 'date_add', 'date_upd', 'photo']

        # поля только для чтения
        read_only_fields = ['id', 'user']

class CommentPostSerializer(serializers.ModelSerializer):
    replycomment = ReplyCommentPostSerializer(many=True, read_only=True)

    class Meta:
        model = CommentPost
        fields = ['id', 'user', 'post', 'description', 'status', 'date_add', 'date_upd', 'photo', 'replycomment']

        # поля только для чтения
        read_only_fields = ['id', 'user']


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPost
        fields = ['id', 'name', 'image']

        # поля только для чтения
        read_only_fields = ['id']


class PostSerializer(WritableNestedModelSerializer):
    comment = CommentPostSerializer(many=True, read_only=True)
    photo = PhotoPostSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'price', 'status', 'date_add', 'date_upd', 'photo', 'video', 'comment']

        # поля только для чтения
        read_only_fields = ['id', 'user']
