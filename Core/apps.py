from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    name = 'Core'

    def ready(self):
        from Core import signals

        post_save.connect(signals.create_sub_work_orders,
                          sender='Core.WorkOrder')
