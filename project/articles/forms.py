from django.forms import ModelForm
from .models import Article
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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
