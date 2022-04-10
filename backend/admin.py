from django.contrib import admin
from .models import Profile, Post, PhotoPost, CommentPost, ReplyCommentPost

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(ReplyCommentPost)