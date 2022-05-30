import django_filters
from django_filters import CharFilter

from aplicatie2.models import ResortUserRating
from webscrapping.models import Resorts


class ResortFilter(django_filters.FilterSet):

    class Meta:
        model = Resorts
        fields = '__all__'
        exclude = ('difference', 'img', 'lowest_point')

