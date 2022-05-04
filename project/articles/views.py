from pyexpat import model
from re import template
from django.shortcuts import render
from .models import Article
from django.views.generic import ListView


class ArticleList(ListView):
    model = Article
    template_name = 'articles/main.html'
    context_object_name = 'articles'
