from django.urls import path, include
from .views import BaseRegisterView, articleDetail, ArticleCreateView, ArticleUpdateView, articleList, myArticles
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', articleList, name='articleList'),
    path('article/<int:pk>', articleDetail, name='article_detail'),

    path('login/',
         LoginView.as_view(template_name='articles/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='articles/main.html', next_page='/'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(
             template_name='articles/signup.html'),
         name='signup'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>', ArticleUpdateView.as_view()),
    path('my_articles', myArticles, name='myArticles'),
]
