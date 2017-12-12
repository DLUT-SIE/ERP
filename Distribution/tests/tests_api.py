from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from Core.models import Department
from Distribution import REVIEW_STATUS_PASS
from Distribution.models import Product, BiddingDocument


class ProductAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(4):
            group, status = Group.objects.get_or_create(
                name='Group_{}'.format(i))
            Department.objects.get_or_create(id=i+1,
                                             group=group,
                                             short_name='Dep_{}'.format(i))

    def test_create_product(self):
        """
        测试创建产品
        """
        url = reverse('product-list')
        data = {'name': 'Product'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Product')

    def test_get_product_list(self):
        """
        测试产品列表自定义分页
        """
        url = reverse('product-list')
        for i in range(10):
            data = {'name': 'Product_{}'.format(i)}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 10)
        list_url = '{}?limit=5'.format(url)
        response = self.client.get(list_url)
        response_dict = response.data
        self.assertIn('count', response_dict)
        self.assertIn('next', response_dict)
        self.assertIn('previous', response_dict)
        self.assertIn('results', response_dict)
        self.assertEqual(response_dict['count'], 10)
        self.assertEqual(len(response_dict['results']), 5)

    def test_get_product(self):
        """
        测试返回产品字段
        """
        url = reverse('product-list')
        data = {'name': 'Product'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get()
        item_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.get(item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_keys = set(response.data.keys())
        self.assertEqual(
            response_keys,
            {'id', 'name', 'actions', 'documents_to_distribution',
             'documents_from_distribution', 'terminated', 'status',
             'pretty_status'})

    def test_update_product(self):
        """
        测试更新产品字段
        """
        url = reverse('product-list')
        data = {'name': 'Product'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get()
        item_url = reverse('product-detail', kwargs={'pk': product.pk})

        data = {'terminated': True}
        response = self.client.patch(item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('terminated', response.data)
        self.assertEqual(response.data['terminated'], True)

        data = {'status': REVIEW_STATUS_PASS}
        response = self.client.patch(item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], REVIEW_STATUS_PASS)

    def test_delete_product(self):
        """
        测试删除产品, 应返回 `HTTP_405_METHOD_NOT_ALLOWED`
        """
        url = reverse('product-list')
        data = {'name': 'Product'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get()
        item_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(item_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class BiddingDocumentAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name='product')
        group_1 = Group.objects.create(name='Group_1')
        group_2 = Group.objects.create(name='Group_2')
        Department.objects.create(group=group_1, short_name='dep_1')
        Department.objects.create(group=group_2, short_name='dep_2')
        cls.product = Product.objects.get()
        cls.deps = Department.objects.all()

    def test_create_documents(self):
        """
        测试创建招标文件
        """
        product = self.product
        dep_1, dep_2 = self.deps
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')

        url = reverse('biddingdocument-list')
        data = {
            'product': product.pk,
            'src': dep_1.pk,
            'dst': dep_2.pk,
            'path': upload_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BiddingDocument.objects.count(), 1)
        self.assertEqual(BiddingDocument.objects.get().product.pk, product.pk)

    def test_get_document(self):
        """
        测试返回招标文件字段
        """
        product = self.product
        dep_1, dep_2 = self.deps
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')

        url = reverse('biddingdocument-list')
        data = {
            'product': product.pk,
            'src': dep_1.pk,
            'dst': dep_2.pk,
            'path': upload_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = BiddingDocument.objects.get()
        item_url = reverse('biddingdocument-detail', kwargs={'pk': doc.pk})
        response = self.client.get(item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.data
        self.assertIn('id', response_dict)
        self.assertIn('src', response_dict)
        self.assertIn('dst', response_dict)
        self.assertIn('path', response_dict)
        self.assertIn('upload_dt', response_dict)
        self.assertIn('status', response_dict)

    def test_update_product(self):
        """
        测试更新产品字段
        """
        product = self.product
        dep_1, dep_2 = self.deps
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        url = reverse('biddingdocument-list')
        data = {
            'product': product.pk,
            'src': dep_1.pk,
            'dst': dep_2.pk,
            'path': upload_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = BiddingDocument.objects.get()
        item_url = reverse('biddingdocument-detail', kwargs={'pk': doc.pk})

        data = {'status': REVIEW_STATUS_PASS}
        response = self.client.patch(item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        doc = BiddingDocument.objects.get()
        self.assertEqual(response.data['status'], doc.status)

    def test_delete_product(self):
        """
        测试删除产品, 应返回 `HTTP_405_METHOD_NOT_ALLOWED`
        """
        product = self.product
        dep_1, dep_2 = self.deps
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        url = reverse('biddingdocument-list')
        data = {
            'product': product.pk,
            'src': dep_1.pk,
            'dst': dep_2.pk,
            'path': upload_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = BiddingDocument.objects.get()
        item_url = reverse('biddingdocument-detail', kwargs={'pk': doc.pk})
        response = self.client.delete(item_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
