from django.db import transaction

from Process import QUOTA_LIST_CATEGORY_USING
from Process.models import QuotaList, ProcessLibrary


def init_process(*args, **kwargs):
    """
    监听工作令的创建，当工作令创建完成后，建立相应的工艺库和所有的定额表
    """
    if not kwargs['created']:
        return
    work_order = kwargs['instance']
    with transaction.atomic():
        quota_lists = []
        process_library = ProcessLibrary.objects.create(work_order=work_order)
        for item in QUOTA_LIST_CATEGORY_USING:
            quota_list = QuotaList(lib=process_library,
                                   category=item)
            quota_lists.append(quota_list)
        QuotaList.objects.bulk_create(quota_lists)
