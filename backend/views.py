from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend.models import Profile, Post, CommentPost, ReplyCommentPost
from backend.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyProfile
from backend.serializer import ProfileSerializer, PostSerializer, CommentPostSerializer, ReplyCommentPostSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    serializer_class = ProfileSerializer

    permission_classes = [IsOwnerOrReadOnlyProfile]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Проверка прав, IsAuthenticated - проверка аунтификации, IsOwnerOrReadOnly - проверка прав действия с объектом
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # можем переопределять методы, например что бы сопоставть поля
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentPostViewSet(ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentPostSerializer

    # Проверка прав, IsAuthenticated - проверка аунтификации, IsOwnerOrReadOnly - проверка прав действия с объектом
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # можем переопределять методы, например что бы сопоставть поля
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReplyCommentViewSet(ModelViewSet):
    queryset = ReplyCommentPost.objects.all()
    serializer_class = ReplyCommentPostSerializer

    # Проверка прав, IsAuthenticated - проверка аунтификации, IsOwnerOrReadOnly - проверка прав действия с объектом
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # можем переопределять методы, например что бы сопоставть поля
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)