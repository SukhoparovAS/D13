from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmationCode = models.IntegerField()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Article(models.Model):
    title = models.TextField(max_length=250, default='Заголовок статьи')
    shortDescription = models.TextField(
        max_length=500, default='Краткое описание')
    content = RichTextField(blank=True)
    preview = models.ImageField(
        upload_to='image', height_field=None, width_field=None, max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500, default='Текст комментария')

    ACCEPTEET = 'accepted'
    REJECTED = 'rejected'
    EXPECTS = 'expects'
    STATUS_COICES = {
        (ACCEPTEET, 'Принят'),
        (REJECTED, 'Отклонен'),
        (EXPECTS, 'Ожидает'),
    }
    status = models.CharField(
        max_length=11, choices=STATUS_COICES, default=EXPECTS)

    def __str__(self):
        return f'{self.user.username}/{self.article.title}'
