from django.urls import path, include
from .views import ArticleList, BaseRegisterView, articleDetailView, ArticleCreateView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', ArticleList.as_view()),
    path('article/<int:pk>', articleDetailView, name='article_detail'),

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
]
