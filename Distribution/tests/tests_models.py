from django.test import TestCase
from django.contrib.auth.models import Group
from django.core import exceptions
from django.core.files.uploadedfile import SimpleUploadedFile

from Core.models import Department
from Distribution import (REVIEW_STATUS_DEFAULT, REVIEW_STATUS_PASS,
                          REVIEW_STATUS_FAIL)
from Distribution.models import Product, BiddingDocument


class ProductTest(TestCase):
    def setUp(self):
        Product.objects.create(name='product')

    def test_str(self):
        product = Product.objects.get()
        expected_str = product.name
        self.assertEqual(str(product), expected_str)

    def test_review_fail(self):
        product = Product.objects.get()
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_fail(None)
        self.assertEqual(product.status, REVIEW_STATUS_FAIL)

    def test_review_fail_raise_exception(self):
        product = Product.objects.get()
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            product.review_fail(None)

    def test_review_pass(self):
        product = Product.objects.get()
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)

    def test_review_pass_raise_exception(self):
        product = Product.objects.get()
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            product.review_pass(None)

    def test_terminate(self):
        product = Product.objects.get()
        self.assertIs(product.terminated, False)
        product.terminate(None)
        self.assertIs(product.terminated, True)
        with self.assertRaises(exceptions.ValidationError):
            product.terminate(None)


class BiddingDocumentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name='product')
        group_1 = Group.objects.create(name='Group_1')
        group_2 = Group.objects.create(name='Group_2')
        Department.objects.create(group=group_1, short_name='dep_1')
        Department.objects.create(group=group_2, short_name='dep_2')

    def setUp(self):
        product = Product.objects.get()
        dep_1, dep_2 = Department.objects.all()
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        BiddingDocument.objects.create(
            product=product,
            src=dep_1,
            dst=dep_2,
            path=upload_file)

    def test_str(self):
        doc = BiddingDocument.objects.get()
        self.assertIn('UploadFile', str(doc))

    def test_review_fail(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_fail(None)
        self.assertEqual(doc.status, REVIEW_STATUS_FAIL)

    def test_review_fail_raise_exception(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_fail(None)

    def test_review_pass(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)

    def test_review_pass_raise_exception(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_pass(None)

    def test_review_reset(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_fail(None)
        self.assertEqual(doc.status, REVIEW_STATUS_FAIL)
        doc.review_reset(None)
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)

    def test_review_reset_raise_exception(self):
        doc = BiddingDocument.objects.get()
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_reset(None)
