from django.test import TestCase
from django.core import exceptions
from django.core.files.uploadedfile import SimpleUploadedFile
from model_mommy import mommy

from Distribution import (REVIEW_STATUS_DEFAULT, REVIEW_STATUS_PASS,
                          REVIEW_STATUS_FAIL)


class ProductTest(TestCase):
    def setUp(self):
        self.product = mommy.prepare('Product')

    def test_str(self):
        product = self.product
        expected_str = product.name
        self.assertEqual(str(product), expected_str)

    def test_review_fail(self):
        product = self.product
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_fail(None)
        self.assertEqual(product.status, REVIEW_STATUS_FAIL)

    def test_review_fail_raise_exception(self):
        product = self.product
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            product.review_fail(None)

    def test_review_pass(self):
        product = self.product
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)

    def test_review_pass_raise_exception(self):
        product = self.product
        self.assertEqual(product.status, REVIEW_STATUS_DEFAULT)
        product.review_pass(None)
        self.assertEqual(product.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            product.review_pass(None)

    def test_terminate(self):
        product = self.product
        self.assertIs(product.terminated, False)
        product.terminate(None)
        self.assertIs(product.terminated, True)
        with self.assertRaises(exceptions.ValidationError):
            product.terminate(None)


class BiddingDocumentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = mommy.prepare('Product')
        cls.departments = mommy.prepare('Department', _quantity=2)

    def setUp(self):
        product = self.product
        dep_1, dep_2 = self.departments
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        self.bidding_document = mommy.prepare(
            'BiddingDocument',
            product=product,
            src=dep_1,
            dst=dep_2,
            path=upload_file)

    def test_str(self):
        doc = self.bidding_document
        self.assertIn('UploadFile', str(doc))

    def test_path_name(self):
        doc = self.bidding_document
        self.assertEqual('UploadFile.txt', doc.path_name)

    def test_review_fail(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_fail(None)
        self.assertEqual(doc.status, REVIEW_STATUS_FAIL)

    def test_review_fail_raise_exception(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_fail(None)

    def test_review_pass(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)

    def test_review_pass_raise_exception(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_pass(None)

    def test_review_reset(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_fail(None)
        self.assertEqual(doc.status, REVIEW_STATUS_FAIL)
        doc.review_reset(None)
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)

    def test_review_reset_raise_exception(self):
        doc = self.bidding_document
        self.assertEqual(doc.status, REVIEW_STATUS_DEFAULT)
        doc.review_pass(None)
        self.assertEqual(doc.status, REVIEW_STATUS_PASS)
        with self.assertRaises(exceptions.ValidationError):
            doc.review_reset(None)
