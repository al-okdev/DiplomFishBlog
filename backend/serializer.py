from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from backend.models import Post, Profile

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")

    def create(self, validated_data):
        uname = validated_data['username']
        password = validated_data['password']
        user = get_user_model().objects.create(
            username=uname,
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)


        return user



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'title', 'text', 'status', 'created_at']

        # поля только для чтения
        read_only_fields = ['user']