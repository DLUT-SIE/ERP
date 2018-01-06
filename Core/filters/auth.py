from django.contrib.auth.models import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    phone = filters.CharFilter(name='info__phone', lookup_expr='icontains')
    mobile = filters.CharFilter(name='info__mobile', lookup_expr='icontains')
    first_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('first_name', 'phone', 'mobile')
