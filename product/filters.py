import django_filters

from .choices import PlantSizeChoices
from .models import Plant, Category


class PlantFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )
    size = django_filters.ChoiceFilter(
        field_name='size',
        choices=PlantSizeChoices.choices
    )

    class Meta:
        model = Plant
        fields = ['category', 'size']

