from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ujson import loads as load_json

from backend.models import Profile, Post, CommentPost, ReplyCommentPost, PhotoPost, Shop, Category, ProductInfo, \
    Product, \
    Parameter, ProductParameter, Order, OrderItem, Contact
from backend.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyProfile
from backend.serializer import ProfileSerializer, PostSerializer, CommentPostSerializer, ReplyCommentPostSerializer, \
    PhotoPostSerializer, ShopSerializer, CategorySerializer, ProductInfoSerializer, ProductSerializer, OrderSerializer, \
    OrderItemSerializer, ContactSerializer


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


class BasketViewSet(APIView):
    """
    Класс для работы с корзиной пользователя
    """

    # получить корзину
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    # редактировать корзину
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = items_sting
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': basket.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return JsonResponse({'Status': False, 'Errors': str(error)})
                        else:
                            objects_created += 1

                    else:

                        JsonResponse({'Status': False, 'Errors': serializer.errors})

                return JsonResponse({'Status': True, 'Создано объектов': objects_created})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить товары из корзины
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # добавить позиции в корзину
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        print(items_sting)
        if items_sting:
            try:
                items_dict = items_sting
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['quantity']) == int:
                        objects_updated += OrderItem.objects.filter(order_id=basket.id, id=order_item['id']).update(
                            quantity=order_item['quantity'])

                return JsonResponse({'Status': True, 'Обновлено объектов': objects_updated})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ContactView(APIView):
    """
    Класс для работы с контактами покупателей
    """

    # получить мои контакты
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        contact = Contact.objects.filter(
            user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    # добавить новый контакт
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone'}.issubset(request.data):
            # request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить контакт
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # редактировать контакт
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if 'id' in request.data:
            if request.data['id'].isdigit():
                contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
                print(contact)
                if contact:
                    serializer = ContactSerializer(contact, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'Status': True})
                    else:
                        JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})