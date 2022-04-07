from django.contrib.auth.models import User
from django.db import models
from backend import get_photo


USER_TYPE = (
    ('limited', 'Ограниченный'),
    ('simple', 'Обычный'),
    ('representative', 'Представитель Магазина')
)

STATUS = (
    (0, 'Не активен'),
    (1, 'Активен')
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE, max_length=25, default='simple')
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_profile, blank=True, null=True)

class PhotoPost(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_photo.get_upload_to_post, blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=1)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    photo = models.ManyToManyField(PhotoPost, blank=True)
    video = models.CharField(max_length=255, blank=True)


