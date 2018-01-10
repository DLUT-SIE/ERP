from unittest.mock import Mock

from django.test import TestCase

from Inventory import (INVENTORY_DETAIL_STATUS_EXHAUST,
                       INVENTORY_DETAIL_STATUS_NORMAL)
from Inventory.signals import update_inventory_status


class UpdateInventoryStatusSignalTest(TestCase):
    def test_signal_apply(self):
        inventory = Mock()
        inventory.count = 10
        inventory.status = INVENTORY_DETAIL_STATUS_EXHAUST
        kwargs = {
            'instance': inventory
        }
        update_inventory_status(**kwargs)
        self.assertIs(inventory.status, INVENTORY_DETAIL_STATUS_NORMAL)

    def test_signal_refund(self):
        inventory = Mock()
        inventory.count = 0
        inventory.status = INVENTORY_DETAIL_STATUS_NORMAL
        kwargs = {
            'instance': inventory
        }
        update_inventory_status(**kwargs)
        self.assertIs(inventory.status, INVENTORY_DETAIL_STATUS_EXHAUST)
