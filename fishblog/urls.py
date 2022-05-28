"""fishblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from backend.views import ProfileViewSet, PostViewSet, CommentPostViewSet, ReplyCommentViewSet, PhotoPostViewSet, \
    ShopViewSet, CategoryViewSet, ProductViewSet, BasketViewSet, ContactView

r = DefaultRouter()
r.register('api_v1/profile', ProfileViewSet) #<int:profile>/
r.register('api_v1/posts', PostViewSet)
r.register('api_v1/comment', CommentPostViewSet)
r.register('api_v1/replycomment', ReplyCommentViewSet)
r.register('api_v1/photopost', PhotoPostViewSet)
r.register('api_v1/shops', ShopViewSet)
r.register('api_v1/categories', CategoryViewSet)
r.register('api_v1/products', ProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_v1/auth/', include('backend.urls')),
    path('api_v1/auth/', include('djoser.urls')),
    path('api_v1/auth/', include('djoser.urls.authtoken')),
    path('api_v1/basket/', BasketViewSet.as_view(), name='basket'),
    path('api_v1/user/contact', ContactView.as_view(), name='user-contact'),
] + r.urls
