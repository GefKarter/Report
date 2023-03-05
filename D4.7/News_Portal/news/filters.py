from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    added_after = DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )
    class Meta:
        model = Post
        fields = {
            'title',
            'categoryType',
            'author',
        }

