from django_filters import rest_framework as filters

from Production.models import ProcessDetail

from Process import PROCESS_CHOICES


class ProcessDetailFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(label='工作令', name='sub_order',
                                        method='filter_sub_order_uid')
    material_index = filters.CharFilter(
        label='票号', name='sub_material__material__ticket_number',
        lookup_expr='icontains')
    process_name = filters.ChoiceFilter(label='工序名称',
                                        name='process_step__step',
                                        choices=PROCESS_CHOICES)
    production_workgroup = filters.CharFilter(label='工作组',
                                              name='work_group__name',
                                              lookup_expr='icontains')
    plan_status = filters.BooleanFilter(label='计划状态',
                                        name='estimated_start_dt',
                                        method='filter_not_empty')
    allocation_status = filters.BooleanFilter(label='分配状态',
                                              name='work_group',
                                              method='filter_not_empty')
    confirm_status = filters.BooleanFilter(label='完成状态',
                                           name='actual_finish_dt',
                                           method='filter_not_empty')

    class Meta:
        model = ProcessDetail
        fields = ('work_order_uid', 'material_index', 'process_name',
                  'production_workgroup', 'plan_status', 'allocation_status',
                  'confirm_status')

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

    def filter_not_empty(self, queryset, name, value):
        lookup_field = '__'.join([name, 'isnull'])
        value = not value
        return queryset.filter(**{lookup_field: value})
