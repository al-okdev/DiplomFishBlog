from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend.models import Profile, Post, CommentPost, ReplyCommentPost, PhotoPost, Shop, Category, ProductInfo, Product, \
    Parameter, ProductParameter
from backend.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyProfile
from backend.serializer import ProfileSerializer, PostSerializer, CommentPostSerializer, ReplyCommentPostSerializer, \
    PhotoPostSerializer, ShopSerializer, CategorySerializer, ProductInfoSerializer, ProductSerializer


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


class ProductViewSet(ModelViewSet):
    """
    Класс для поиска товаров
    """
    queryset = Product.objects.filter(status=1)
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        print(shop_id)
        print(category_id)


        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        # фильтруем и отбрасываем дуликаты
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()

        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.data.get('category'):
            raise ValidationError('Необходимо передать id категории')
        else:
            user = self.request.user
            print(user)

            if Category.objects.filter(user=user, id=request.data.get('category')):

                # serializer = self.get_serializer(data=request.data)
                # serializer.is_valid(raise_exception=True)
                # self.perform_create(serializer)
                # headers = self.get_success_headers(serializer.data)

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                obj_new_product = serializer.save(user=self.request.user)
                print(obj_new_product.id)


                if(obj_new_product.id):
                    product_info = ProductInfo.objects.create(product_id=obj_new_product.id,
                                                              external_id=request.data.get('external_id'),
                                                              model=request.data.get('model'),
                                                              price=request.data.get('price'),
                                                              price_rrc=request.data.get('price_rrc'),
                                                              quantity=request.data.get('quantity'),
                                                              shop_id=request.data.get('shop'))

                    for name_p, value in request.data.get('parameters').items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name_p)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)
                #
                #
                # return Response(serializer.data, status=201, headers=headers)
                return Response(serializer.data, status=201)
            else:
                raise ValidationError('Не верный id категории')