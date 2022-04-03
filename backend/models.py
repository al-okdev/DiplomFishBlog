from django.contrib.auth.models import User
from django.db import models
from backend import get_photo


USER_TYPE = (
    ('limited', 'Ограниченный'),
    ('simple', 'Обычный'),
    ('representative', 'Представитель Магазина')
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE, max_length=25, default='simple')
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_profile, blank=True, null=True)

class Post(models.Model):
    pass