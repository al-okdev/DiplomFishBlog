from djoser.serializers import UserCreateSerializer
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from backend.models import Post, Profile, CommentPost, ReplyCommentPost, PhotoPost, Shop, Category, Product, \
    ProductParameter, ProductInfo, OrderItem, Contact, Order

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


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'state', 'description', 'photo', 'coordinates', 'address',)
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'shops', 'user', 'photo', 'status',)
        read_only_fields = ('id', 'user',)


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category', 'user', 'photo', 'status')
        read_only_fields = ('id', 'user',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)