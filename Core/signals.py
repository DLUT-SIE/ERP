from django.db import transaction

from Core.models import SubWorkOrder


def create_sub_work_orders(*args, **kwargs):
    if not kwargs['created']:
        return
    work_order = kwargs['instance']
    with transaction.atomic():
        sub_orders = []
        for index in range(1, 1 + work_order.count):
            sub_orders.append(SubWorkOrder(work_order=work_order, index=index))
        SubWorkOrder.objects.bulk_create(sub_orders)
