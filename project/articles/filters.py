from .models import Comment, Article
from django_filters import FilterSet, ChoiceFilter


class CommentFilter(FilterSet):
    status_in = ChoiceFilter(
        field_name='status', lookup_expr='icontains', choices=Comment.STATUS_COICES)
    article_in = ChoiceFilter(field_name='article')

    class Meta:
        model = Comment
        fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs['request']
        all_articles = Article.objects.filter(user=request.user)
        my_choices = ()
        for i in all_articles:
            new = (str(i.id), str(i.title))
            my_choices += (new,)
        my_choices += (('', 'ALL'),)

        self.filters['article_in'].extra.update({'choices': my_choices, })
