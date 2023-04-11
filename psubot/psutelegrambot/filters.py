import django_filters

from psutelegrambot.models import UserNotFoundQuestion


class UserNotFoundQuestionFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    username = django_filters.CharFilter(lookup_expr='icontains')
    text = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserNotFoundQuestion
        fields = ['first_name', 'last_name', 'username', 'text']

