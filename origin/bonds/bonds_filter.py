import django_filters
from bonds.models import Bond


class BondFilter(django_filters.FilterSet):
    legal_name = django_filters.CharFilter(lookup_expr='iexact',
                                           field_name='legal_name')

    class Meta:
        model = Bond
        fields = ['legal_name']
