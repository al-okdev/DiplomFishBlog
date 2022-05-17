from django.contrib import admin
from .models import Profile, Post, PhotoPost, CommentPost, ReplyCommentPost, Shop

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PhotoPost)
admin.site.register(CommentPost)
admin.site.register(ReplyCommentPost)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass