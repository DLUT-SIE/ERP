from django.apps import AppConfig
from django.db.models.signals import post_save


class ProductionConfig(AppConfig):
    name = 'Production'

    def ready(self):
        from Production import signals

        post_save.connect(signals.create_process_details,
                          sender='Production.SubMaterial')
