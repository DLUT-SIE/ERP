from django.test import TestCase

from Distribution.models import Product


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name='product')

    def test_str(self):
        product = Product.objects.all()[0]
        expected_str = product.name
        self.assertEqual(str(product), expected_str)
