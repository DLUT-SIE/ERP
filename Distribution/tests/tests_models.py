from django.test import TestCase
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile

from Core.models import Department
from Distribution.models import Product, BiddingDocument


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name='product')

    def test_str(self):
        product = Product.objects.all()[0]
        expected_str = product.name
        self.assertEqual(str(product), expected_str)


class BiddingDocumentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name='product')
        group_1 = Group.objects.create(name='Group_1')
        group_2 = Group.objects.create(name='Group_2')
        dep_1 = Department.objects.create(group=group_1, short_name='dep_1')
        dep_2 = Department.objects.create(group=group_2, short_name='dep_2')
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        BiddingDocument.objects.create(
            product=product,
            src=dep_1,
            dst=dep_2,
            path=upload_file)

    def test_str(self):
        doc = BiddingDocument.objects.all()[0]
        self.assertIn('UploadFile', str(doc))
