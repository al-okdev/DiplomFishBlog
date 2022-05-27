from django.contrib import admin
from .models import Profile, Post, PhotoPost, CommentPost, ReplyCommentPost, Shop, Category, Product, ProductInfo, \
    ProductParameter, Parameter, Contact, Order, OrderItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PhotoPost)
admin.site.register(CommentPost)
admin.site.register(ReplyCommentPost)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class Category(admin.ModelAdmin):
    pass

@admin.register(Product)
class Product(admin.ModelAdmin):
    pass

@admin.register(ProductInfo)
class ProductInfo(admin.ModelAdmin):
    pass

@admin.register(Parameter)
class Parameter(admin.ModelAdmin):
    pass

@admin.register(ProductParameter)
class ProductParameter(admin.ModelAdmin):
    pass

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    pass

@admin.register(Order)
class Order(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    pass