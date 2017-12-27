from django.apps import AppConfig
from django.db.models.signals import pre_save


class InventoryConfig(AppConfig):
    name = 'Inventory'

    def ready(self):
        from Inventory import signals
        from Inventory.models import (
            WeldingMaterialInventoryDetail,
            SteelMaterialInventoryDetail,
            AuxiliaryMaterialInventoryDetail,
            BoughtInComponentInventoryDetail)

        for model in (WeldingMaterialInventoryDetail,
                      SteelMaterialInventoryDetail,
                      AuxiliaryMaterialInventoryDetail,
                      BoughtInComponentInventoryDetail):
            pre_save.connect(signals.update_inventory_status, sender=model)
