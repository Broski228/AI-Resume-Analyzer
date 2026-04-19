import django_filters
from .models import Resume


class ResumeFilter(django_filters.FilterSet):
    profession = django_filters.ChoiceFilter(choices=Resume.PROFESSION_CHOICES)
    level = django_filters.ChoiceFilter(choices=Resume.LEVEL_CHOICES)
    city = django_filters.ChoiceFilter(choices=Resume.CITY_CHOICES)
    experience_min = django_filters.NumberFilter(field_name='experience_years', lookup_expr='gte')
    experience_max = django_filters.NumberFilter(field_name='experience_years', lookup_expr='lte')
    has_bachelor = django_filters.BooleanFilter()
    has_master = django_filters.BooleanFilter()
    language = django_filters.CharFilter(method='filter_language')

    class Meta:
        model = Resume
        fields = ['profession', 'level', 'city', 'has_bachelor', 'has_master']

    def filter_language(self, queryset, name, value):
        # Фильтр по языку: ?language=english
        return queryset.filter(languages__contains=value)
