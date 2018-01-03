from django.db import transaction

from Production.models import ProcessDetail


def create_process_details(*args, **kwargs):
    if not kwargs['created']:
        return
    sub_material = kwargs['instance']
    with transaction.atomic():
        process_details = []
        process_route = sub_material.material.processroute
        process_steps = process_route.steps.all().order_by('pk')
        for process_step in process_steps:
            process_details.append(ProcessDetail(sub_material=sub_material,
                                                 process_step=process_step))
        ProcessDetail.objects.bulk_create(process_details)
