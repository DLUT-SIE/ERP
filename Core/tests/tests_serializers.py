from unittest.mock import Mock, patch

from django.test import TestCase
from model_mommy import mommy

import Core.serializers.auth as auth_serializers
import Core.serializers.work_order as work_order_serializers
from Core import models


class UserSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_info = mommy.prepare('UserInfo')
        cls.user = mommy.prepare('User')

    def test_user_info_serializer_fields(self):
        data = auth_serializers.UserInfoSerializer(self.user_info).data
        expected_keys = {'id', 'phone', 'mobile', 'gender'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_user_serializer_fields(self):
        data = auth_serializers.UserSerializer(self.user).data
        expected_keys = {'id', 'first_name', 'last_name', 'email', 'info'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_user_list_serializer_fields(self):
        data = auth_serializers.UserListSerializer(self.user).data
        expected_keys = {'id', 'first_name', 'email', 'info'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('django.contrib.auth.models.User.objects.create')
    @patch('Core.models.auth.UserInfo.objects.create')
    def test_user_create_serializer_fields(self, mocked_userinfo_create,
                                           mocked_user_create):
        data = {
            'username': '123',
            'password': '123',
            'email': 'test@test.com',
            'first_name': 'david',
            'last_name': 'david',
            'info': {
                'phone': 123,
                'mobile': 456,
                'gender': 0,
            }
        }
        mocked_user_create.return_value = mommy.prepare('User')
        mocked_userinfo_create.return_value = mommy.prepare('UserInfo')
        serializer = auth_serializers.UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data = auth_serializers.UserCreateSerializer(self.user).data
        expected_keys = {'username', 'email', 'first_name',
                         'last_name', 'info', 'id'}
        self.assertEqual(set(data.keys()), expected_keys)
        mocked_user_create.assert_called()
        mocked_userinfo_create.assert_called()


class GroupSerializerTest(TestCase):
    def test_group_serializer_fields(self):
        group = mommy.prepare('Group')
        data = auth_serializers.GroupSerializer(group).data
        expected_keys = {'name'}
        self.assertEqual(set(data.keys()), expected_keys)


class DepartmentSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = mommy.prepare('Department')

    def test_department_serializer_fields(self):
        data = auth_serializers.DepartmentSerializer(self.department).data
        expected_keys = {'id', 'group', 'superior', 'admin', 'short_name'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('django.contrib.auth.models.Group.objects.create')
    @patch('Core.models.auth.Department.objects.create')
    def test_department_serializer_create_fields(
            self, mocked_department_create, mocked_group_create):
        data = {
            'short_name': 'dep',
            'group': {
                'name': 'group',
            }
        }
        mocked_group_create.return_value = mommy.prepare('Group')
        mocked_department_create.return_value = mommy.prepare('Department')
        serializer = auth_serializers.DepartmentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data = auth_serializers.DepartmentSerializer(self.department).data
        expected_keys = {'id', 'group', 'superior', 'admin', 'short_name'}
        self.assertEqual(set(data.keys()), expected_keys)
        mocked_group_create.assert_called()
        mocked_department_create.assert_called()

    def test_department_list_serializer_fields(self):
        data = auth_serializers.DepartmentListSerializer(self.department).data
        expected_keys = {'id', 'superior', 'admin', 'short_name'}
        self.assertEqual(set(data.keys()), expected_keys)


class WorkOrderSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        work_order = Mock(spec=models.WorkOrder)
        work_order.id = 1
        work_order.count = 0
        work_order.sell_type = 0
        cls.work_order = work_order

    def test_work_order_serializer_fields(self):
        data = work_order_serializers.WorkOrderSerializer(self.work_order).data
        expected_keys = {'id', 'uid', 'sell_type', 'client', 'project',
                         'product', 'count', 'finished', 'pretty_sell_type'}
        self.assertEqual(set(data.keys()), expected_keys)


class SubWorkOrderSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        sub_order = Mock(spec=models.SubWorkOrder)
        sub_order.id = 1
        sub_order.index = 1
        cls.sub_order = sub_order

    def test_sub_work_order_serializer_fields(self):
        data = work_order_serializers.SubWorkOrderSerializer(
            self.sub_order).data
        expected_keys = {'id', 'work_order', 'index', 'finished', 'uid'}
        self.assertEqual(set(data.keys()), expected_keys)
