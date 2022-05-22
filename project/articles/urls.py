from django.urls import path, include
from .views import articleDetail, ArticleCreateView, ArticleUpdateView, articleList, myArticles, myComments, loginUser, registerUser, emailConfirmation, ArticleDelete
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', articleList, name='articleList'),
    path('article/<int:pk>', articleDetail, name='article_detail'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>', ArticleUpdateView.as_view()),
    path('my_comments', myComments, name='myComments'),
    path('my_articles', myArticles, name='myArticles'),
    path('login/', loginUser, name='login'),
    path('logout/', LogoutView.as_view(template_name='articles/main.html',
         next_page='/'), name='logout'),
    path('signup/', registerUser, name='signup'),
    path('email_confirmation/<int:pk>',
         emailConfirmation, name='emailConfirmation'),
    path('article_delete/<int:pk>', ArticleDelete.as_view()),
]
