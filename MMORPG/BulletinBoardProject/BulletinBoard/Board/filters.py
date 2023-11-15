import django_filters
from django_filters import FilterSet
from .models import Notification
from django.db.models import Q


class ProductFilter(FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="search")

    class Meta:
        model = Notification
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(text__icontains=value)
        )
