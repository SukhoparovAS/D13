from dataclasses import field
from django.forms import ModelForm
from .models import Article
from django import forms
from django.contrib.auth.models import User


class EmailConfirmationForm(forms.Form):
    confirmationCode = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EmailConfirmationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login__input'
        self.fields['confirmationCode'].widget.attrs['placeholder'] = 'Код подтверждения'


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'email'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login__input'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "пользователь с таким email уже существует")

        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль'}),)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login__input'


class ArticleCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['content'].label = ''
        self.fields['shortDescription'].label = ''
        self.fields['category'].label = 'Категория'
        self.fields['preview'].label = 'preview image'

    class Meta:
        model = Article
        fields = ['title', 'preview',
                  'shortDescription', 'content', 'category']

        widgets = {
            'title': forms.Textarea(attrs={'class': 'create-form__title'}),
            'shortDescription': forms.Textarea(attrs={'class': 'create-form__shortDescription'}),

        }
