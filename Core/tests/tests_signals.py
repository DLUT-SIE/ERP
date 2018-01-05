from unittest.mock import patch, Mock

from django.test import TestCase

from Core.signals import create_sub_work_orders
from Core.models import WorkOrder


class CreateSubWorkOrdersSignalTest(TestCase):
    def test_signal_created(self):
        kwargs = {
            'created': True,
            'instance': Mock(spec=WorkOrder, count=5, _state=Mock()),
        }
        with patch('Core.models.work_order.'
                   'SubWorkOrder.objects') as mock:
            self.assertIsNone(create_sub_work_orders(**kwargs))
            mock.bulk_create.assert_called()

    def test_signal_updated(self):
        kwargs = {
            'created': False,
        }
        self.assertIsNone(create_sub_work_orders(**kwargs))
