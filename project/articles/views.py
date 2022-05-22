from sys import flags
from django.shortcuts import redirect, render
from .models import Article, Category, Comment, LikedArticle
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .forms import ArticleCreateForm, LoginForm, UserRegistrationForm, EmailConfirmationForm
from django import forms
from .filters import CommentFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.models import User


def likeArticle(request, article):
    user = request.user
    if user.is_authenticated:
        article = article
        if not user.likedArticle.filter(article=article).exists():
            liketdArticle = LikedArticle(user=user, article=article)
            liketdArticle.save()
            article.rating += 1
            article.save()
    else:
        return False
    return True


class ArticleDelete(LoginRequiredMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    queryset = Article.objects.all()
    success_url = '/'


def authenticate(username=None, password=None):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
        else:
            return None
    except User.DoesNotExist:
        user = User(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return None


def emailConfirmation(request, pk):
    if request.user.is_authenticated:
        return redirect('articleList')
    else:
        if User.objects.filter(pk=pk):
            user = User.objects.get(pk=pk)
        if request.method == 'POST':
            form = EmailConfirmationForm(request.POST)
            if form.is_valid():

                if user.profile.confirmationCode == form.cleaned_data.get('confirmationCode'):
                    if user.is_active == False:
                        user.is_active = True
                        user.save()
                        login(request, user)
                        return redirect('articleList')
        else:
            form = EmailConfirmationForm()
            email = user.email
            return render(request, 'articles/email_confirmation.html', {'form': form, 'email': email})


def registerUser(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            return redirect('emailConfirmation', pk=new_user.pk)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'articles/signup.html', {'form': user_form})


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('articleList')
                else:
                    return redirect('emailConfirmation', pk=user.pk)
            else:
                user = authenticate(
                    username=cd['username'], password=cd['password'])
                print(user)
                return render(request, 'articles/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'articles/login.html', {'form': form})


def articleList(request):
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')
    likeArticle_query = request.GET.get('likeArticle', '')
    context = {}
    articles = Article.objects.select_related('user', 'category').annotate(commentsCount=Count('comments', filter=Q(
        comments__status='accepted'))).all().order_by('-create_at')
    categories = Category.objects.all()
    if search_query:
        articles = articles.filter(Q(title__icontains=search_query) | Q(
            content__icontains=search_query) | Q(shortDescription__icontains=search_query))
        context['getName'] = 'search'
        context['getValue'] = search_query
    if category_query:
        articles = articles.filter(category__name=category_query)
        context['getName'] = 'category'
        context['getValue'] = category_query
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['categories'] = categories
    if likeArticle_query:
        article = articles.get(pk=likeArticle_query)
        if not likeArticle(request, article):
            return redirect('login')

    return render(request, 'articles/main.html',
                  context=context)


def articleDetail(request, pk):
    article = Article.objects.annotate(commentsCount=Count('comments', filter=Q(
        comments__status='accepted'))).select_related('user').get(pk=pk)
    context = {
        'article': article,
    }
    likeArticle_query = request.GET.get('likeArticle', '')
    comments = article.comments.select_related('user').all().order_by('-pk')
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    user = request.user

    if (request.method == 'POST') & (request.user.is_authenticated):
        text = request.POST['comment_text']

        article = Article.objects.get(pk=pk)
        comment = Comment(text=text, user=user,
                          article=article, status="expects")
        comment.save()
        return redirect('article_detail', pk=pk)
    commentManagement(request)
    if likeArticle_query:
        if not likeArticle(request, article):
            return redirect('login')
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


@login_required
def myArticles(request):
    likeArticle_query = request.GET.get('likeArticle', '')
    articles = Article.objects.all().filter(user=request.user).annotate(commentsCount=Count('comments', filter=Q(
        comments__status='accepted'))).all().order_by('-create_at')
    context = {}
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    if likeArticle_query:
        article = articles.get(pk=likeArticle_query)
        if not likeArticle(request, article):
            return redirect('login')

    return render(request, 'articles/my_articles.html',
                  context=context)


@login_required
def myComments(request):
    context = {}
    user = request.user
    comments = Comment.objects.select_related(
        'user', 'article__user').all().filter(article__user=user)
    filter = CommentFilter(
        request.GET, queryset=comments, request=request)
    context['filter'] = filter
    paginator = Paginator(filter.qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    commentManagement(request)

    return render(request, 'articles/my_comments.html',
                  context=context)


def commentManagement(request):
    delete = request.GET.get('delete', '')
    accept = request.GET.get('accept', '')
    reject = request.GET.get('reject', '')
    user = request.user
    if delete:
        comment = Comment.objects.get(pk=delete)
        if (comment.user == user) | (comment.article.user == user):
            comment.delete()

    if accept:
        comment = Comment.objects.get(pk=accept)
        if comment.article.user == user:
            comment.status = 'accepted'
            comment.save()

    if reject:
        comment = Comment.objects.get(pk=reject)
        if comment.article.user == user:
            comment.status = 'rejected'
            comment.save()
