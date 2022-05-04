from curses import A_CHARTEXT
from django.urls import path, include
from .views import ArticleList

urlpatterns = [
    path('', ArticleList.as_view()),
]
