from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend.models import Profile, Post, CommentPost, ReplyCommentPost, PhotoPost, Shop, Category
from backend.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyProfile
from backend.serializer import ProfileSerializer, PostSerializer, CommentPostSerializer, ReplyCommentPostSerializer, \
    PhotoPostSerializer, ShopSerializer, CategorySerializer


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


class PhotoPostViewSet(ModelViewSet):
    queryset = PhotoPost.objects.all()
    serializer_class = PhotoPostSerializer


class CommentPostViewSet(ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentPostSerializer

    # Проверка прав, IsAuthenticated - проверка аунтификации, IsOwnerOrReadOnly - проверка прав действия с объектом
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # можем переопределять методы, например что бы сопоставть поля
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Запрет изменения поста и разрешение частичного обновления модели
    def update(self, request, *args, **kwargs):
        if request.data.get('post'):
            raise ValidationError('Нельзя изменять пост')

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ReplyCommentViewSet(ModelViewSet):
    queryset = ReplyCommentPost.objects.all()
    serializer_class = ReplyCommentPostSerializer

    # Проверка прав, IsAuthenticated - проверка аунтификации, IsOwnerOrReadOnly - проверка прав действия с объектом
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # можем переопределять методы, например что бы сопоставть поля
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Запрет изменения поста и разрешение частичного обновления модели
    def update(self, request, *args, **kwargs):
        if request.data.get('comment'):
            raise ValidationError('Нельзя изменять id комментария')

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ShopViewSet(ModelViewSet):
    """
    Класс для просмотра списка магазинов
    """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer

    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request):
        raise ValidationError('Нельзя создать магазин')

    def destroy(self, request, pk=None):
        raise ValidationError('Нельзя удалить магазин')


class CategoryViewSet(ModelViewSet):
    """
    Класс для просмотра списка категорий
    """
    queryset = Category.objects.filter(status=1)
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.data.get('shops'):
            raise ValidationError('Необходимо передать id магазина')
        else:
            user = self.request.user
            # print(Shop.objects.filter(user=user))
            if Shop.objects.filter(user=user, id=request.data.get('shops')):
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=201, headers=headers)
            else:
                raise ValidationError('Не верный id магазина')

    def update(self, request, *args, **kwargs):
        if not request.data.get('shops'):
            raise ValidationError('Необходимо передать id магазина')
        else:
            user = self.request.user
            # print(Shop.objects.filter(user=user))
            if Shop.objects.filter(user=user, id=request.data.get('shops')):
                partial = True
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                raise ValidationError('Магазин Вам не пренадлежит')