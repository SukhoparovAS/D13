
from django.shortcuts import redirect, render
from .models import Article, Category, Comment
from django.views.generic import CreateView, UpdateView
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.core.paginator import Paginator
from .forms import ArticleCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


def articleList(request):
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')
    context = {
    }

    articles = Article.objects.annotate(commentsCount=Count('comments', filter=Q(
        comments__status='accepted'))).all().order_by('-create_at')

    if search_query:
        articles = articles.filter(Q(title__icontains=search_query) | Q(
            content__icontains=search_query) | Q(shortDescription__icontains=search_query))
        context['getName'] = 'search'
        context['getValue'] = search_query
    if category_query:
        articles = articles.filter(
            category=Category.objects.get(name=category_query))
        context['getName'] = 'category'
        context['getValue'] = category_query

    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    context['categories'] = Category.objects.all()

    return render(request, 'articles/main.html',
                  context=context)


def articleDetail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }

    comments = article.comments.all().order_by('-pk')
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    if (request.method == 'POST') & (request.user.is_authenticated):
        text = request.POST['comment_text']
        user = request.user
        article = Article.objects.get(pk=pk)
        comment = Comment(text=text, user=user,
                          article=article, status="expects")
        comment.save()

        return redirect('article_detail', pk=pk)

    delete = request.GET.get('delete', '')
    accept = request.GET.get('accept', '')
    reject = request.GET.get('reject', '')

    if delete:
        comment = Comment.objects.get(pk=delete)
        if comment.user == request.user:
            comment.delete()

    if accept:
        comment = Comment.objects.get(pk=accept)
        if comment.article.user == request.user:
            comment.status = 'accepted'
            comment.save()

    if reject:
        comment = Comment.objects.get(pk=reject)
        if comment.article.user == request.user:
            comment.status = 'rejected'
            comment.save()

    return render(request, 'articles/article_detail.html',
                  context=context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/create.html'
    form_class = ArticleCreateForm
    success_url = '/'

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = self.request.user
        fields.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    ontext_object_name = 'article_update'
    template_name = 'articles/create.html'
    form_class = ArticleCreateForm
    success_url = '/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Article.objects.get(pk=id)

    def form_valid(self, form):
        fields = form.save(commit=False)

        if fields.user != self.request.user:
            raise forms.ValidationError("Вы не автор этой статьи!")
        fields.save()
        return super().form_valid(form)


def myArticles(request):
    articles = Article.objects.all().filter(user=request.user).annotate(commentsCount=Count('comments', filter=Q(
        comments__status='accepted'))).all().order_by('-create_at')
    context = {}
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, 'articles/my_articles.html',
                  context=context)
