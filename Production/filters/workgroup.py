from django_filters import rest_framework as filters

from Production.models import ProductionUser, ProductionWorkGroup

from Process import PROCESS_CHOICES


class ProductionWorkGroupFilter(filters.FilterSet):
    name = filters.CharFilter(name='name', lookup_expr='icontains')
    process_name = filters.ChoiceFilter(name='process',
                                        choices=PROCESS_CHOICES)

    class Meta:
        model = ProductionWorkGroup
        fields = ('name', 'process_name')


class ProductionUserFilter(filters.FilterSet):
    work_group = filters.CharFilter(name='work_group__name',
                                    lookup_expr='icontains')
    name = filters.CharFilter(name='user_info__user__first_name',
                              lookup_expr='icontains')

    class Meta:
        model = ProductionUser
        fields = ('work_group', 'name')
