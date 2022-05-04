from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)


class Article(models.Model):
    title = models.CharField(max_length=250, default='Заголовок статьи')
    content = models.TextField()
    preview = models.ImageField(
        upload_to='image', height_field=None, width_field=None, max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
