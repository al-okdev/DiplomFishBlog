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

POST_TYPE = (
    ('report', 'Отчет'),
    ('informing', 'Информирование'),
    ('article', 'Статья'),
    ('service', 'Услуга'),
    ('sale', 'Продажа')
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE, max_length=25, default='simple')
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_profile, blank=True, null=True)


class PhotoPost(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=get_photo.get_upload_to_post, blank=True, null=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=1)
    type = models.CharField(verbose_name='Тип поста', choices=POST_TYPE, max_length=25, default='report')
    price = models.IntegerField(verbose_name='Цена', blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    photo = models.ManyToManyField(PhotoPost, blank=True)
    video = models.CharField(max_length=255, blank=True)


class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=1)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_comment, blank=True, null=True)


class ReplyCommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentPost, related_name='replycomment', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=1)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_replycomment, blank=True, null=True)



STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

class Shop(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='статус получения заказов', default=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_shop, blank=True, null=True)
    coordinates = models.CharField(max_length=150, verbose_name='Координаты', blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True, null=True)

    # filename

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    shops = models.ForeignKey(Shop, verbose_name='Магазины', related_name='categories', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_photo.get_upload_to_category, blank=True, null=True)
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=1)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name