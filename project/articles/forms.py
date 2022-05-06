from cProfile import label
from dataclasses import fields
from turtle import title
from django.forms import ModelForm
from .models import Article
from django import forms
from ckeditor.fields import RichTextField


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
