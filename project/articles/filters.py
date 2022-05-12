from .models import Comment
import django_filters
from django_filters import FilterSet, DateFilter, CharFilter


class CommentFilter(FilterSet):

    class Meta:
        model = Comment
        fields = {
            'status': ['in'],

        }
