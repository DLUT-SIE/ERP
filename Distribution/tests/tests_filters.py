from unittest.mock import patch
from django.test import TestCase

from Distribution import filters


class ProductFilterTest(TestCase):
    @patch('Distribution.models.Product')
    def test_filter_by_department(self, mocked_queryset):
        filter = filters.ProductFilter()
        mocked_queryset.filter.return_value = mocked_queryset
        filter.filter_by_department(mocked_queryset, 'department', 1)
        mocked_queryset.filter.assert_called()
        mocked_queryset.distinct.assert_called()
