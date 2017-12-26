from django_filters import rest_framework as filters

from Production.models import ProcessDetail


class ManHourMessageFilter(filters.FilterSet):
    sub_order_uid = filters.CharFilter(label='工作令', name='sub_order',
                                       method='filter_sub_order_uid')
    ticket_number = filters.CharFilter(
        label='工作票号', name='sub_material__material__ticket_number')
    work_group = filters.CharFilter(label='组号', name='work_group')

    class Meta:
        model = ProcessDetail
        fields = ('sub_order_uid', 'ticket_number', 'work_group')

    def filter_sub_order_uid(self, queryset, name, value):
        splits = value.rsplit('-', 1)  # eg, WO1234-1
        if not splits:
            return queryset
        elif len(splits) > 1:
            uid, index = splits
            index = int(index)
            return queryset.filter(
                sub_material__sub_order__work_order__uid=uid,
                sub_material__sub_order__index=index)
        else:
            uid = splits[0]
            return queryset.filter(
                sub_material__sub_order__work_order__uid__icontains=uid)
