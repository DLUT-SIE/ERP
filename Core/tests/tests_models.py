from django.test import TestCase
from django.contrib.auth.models import User, Group

from Core import SELL_TYPE_DOMESTIC, GENDER_MALE
from Core.models import (WorkOrder, SubWorkOrder,
                         UserInfo, Department)
from Distribution.models import Product


class WorkOrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name='product')
        WorkOrder.objects.create(
            uid='123456',
            sell_type=SELL_TYPE_DOMESTIC,
            client='client',
            project='project',
            product=product,
            count=10)

    def test_str(self):
        work_order = WorkOrder.objects.all()[0]
        expected_str = str(work_order.uid)
        self.assertEqual(str(work_order), expected_str)

    def test_sub_orders(self):
        work_order = WorkOrder.objects.all()[0]
        sub_orders = work_order.subworkorder_set.all()
        self.assertEqual(sub_orders.count(), 10)


class SubWorkOrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name='product')
        # SubWorkOrder will be created automatically when WorkOrder created
        WorkOrder.objects.create(
            uid='123456',
            sell_type=SELL_TYPE_DOMESTIC,
            client='client',
            project='project',
            product=product,
            count=10)

    def test_work_order(self):
        work_order = WorkOrder.objects.all()[0]
        sub_order = work_order.subworkorder_set.all()[0]
        self.assertIs(sub_order.work_order, work_order)

    def test_index(self):
        sub_order = SubWorkOrder.objects.all()[0]
        self.assertEqual(sub_order.index, 1)

    def test_str(self):
        sub_order = SubWorkOrder.objects.all()[0]
        expected_str = '{}-{}'.format(sub_order.work_order, sub_order.index)
        self.assertEqual(str(sub_order), expected_str)


class UserInfoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='user',
            password='password',
            first_name='first name',
            last_name='last name')
        UserInfo.objects.create(
            user=user,
            phone='1234567890',
            mobile='0987654321',
            gender=GENDER_MALE)

    def test_str(self):
        user_info = UserInfo.objects.all()[0]
        expected_str = '{}(用户名:{})'.format(
            user_info.user.first_name, user_info.user.username)
        self.assertEqual(str(user_info), expected_str)


class DepartmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='user',
            password='password',
            first_name='first name',
            last_name='last name')
        group = Group.objects.create(name='group')
        Department.objects.create(
            group=group,
            admin=user,
            short_name='dep')

    def test_str(self):
        department = Department.objects.all()[0]
        expected_str = department.group.name
        self.assertEqual(str(department), expected_str)
