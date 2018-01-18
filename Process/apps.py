from django.apps import AppConfig
from django.db.models.signals import post_save


class ProcessConfig(AppConfig):
    name = 'Process'

    def ready(self):
        from Process import signals
        post_save.connect(signals.init_process,
                          sender='Core.WorkOrder')
