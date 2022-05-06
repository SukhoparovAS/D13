from multiprocessing import context
from pyexpat import model
from re import template
from django.shortcuts import redirect, render
from .models import Article, Category, Comment
from django.views.generic import ListView, CreateView
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.core.paginator import Paginator
from .forms import ArticleCreateForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ArticleList(ListView):
    model = Article
    template_name = 'articles/main.html'
    context_object_name = 'articles'
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.annotate(comments=Count('comment', filter=Q(comment__status='accepted'))).all().order_by('-create_at')


def articleDetailView(request, pk):
    context = {
        'article': Article.objects.get(pk=pk),
    }
    comments = Comment.objects.all().filter(
        article=context['article'], status="accepted")
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    if (request.method == 'POST') & (request.user.is_authenticated):
        text = request.POST['comment_text']
        user = request.user
        article = Article.objects.get(pk=pk)
        comment = Comment(text=text, user=user,
                          article=article, status="accepted")
        comment.save()

        return redirect('article_detail', pk=pk)

    return render(request, 'articles/article_detail.html',
                  context=context)


class ArticleCreateView(CreateView):
    template_name = 'articles/create.html'
    form_class = ArticleCreateForm
    success_url = '/'

    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        fields.user = self.request.user
        # Через реквест передаем недостающую форму, которая обязательна
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)
