from unittest.mock import Mock, patch

from django.test import TestCase
from django.contrib.auth.models import User, Group

import Core.serializers.auth as auth_serializers
import Core.serializers.work_order as work_order_serializers
from Core import models


def return_none_instance(model):
    def _wrapper(*args, **kwargs):
        return Mock(spec=model)
    return _wrapper


class UserSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = Mock(spec=User)
        user.id = 1
        user_info = Mock(spec=models.UserInfo)
        user_info.user = user
        user_info.id = 1
        user.info = user_info
        cls.user_info = user_info
        cls.user = user

    def test_user_info_serializer(self):
        data = auth_serializers.UserInfoSerializer(self.user_info).data
        expected_keys = {'id', 'phone', 'mobile', 'gender'}
        self.assertEqual(expected_keys, set(data.keys()))

    def test_user_serializer(self):
        data = auth_serializers.UserSerializer(self.user).data
        expected_keys = {'id', 'first_name', 'last_name', 'email', 'info'}
        self.assertEqual(expected_keys, set(data.keys()))

    def test_user_list_serializer(self):
        data = auth_serializers.UserListSerializer(self.user).data
        expected_keys = {'id', 'first_name', 'email', 'info'}
        self.assertEqual(expected_keys, set(data.keys()))

    @patch('django.contrib.auth.models.User.objects.create',
           return_none_instance(User))
    @patch('Core.models.auth.UserInfo.objects.create',
           return_none_instance(models.UserInfo))
    def test_user_create_serializer(self):
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
        serializer = auth_serializers.UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data = auth_serializers.UserCreateSerializer(self.user).data
        expected_keys = {'username', 'email', 'first_name',
                         'last_name', 'info', 'id'}
        self.assertEqual(expected_keys, set(data.keys()))


class GroupSerializerTest(TestCase):
    def test_group_serializer(self):
        group = Mock(spec=Group)
        data = auth_serializers.GroupSerializer(group).data
        expected_keys = {'name'}
        self.assertEqual(expected_keys, set(data.keys()))


class DepartmentSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group = Mock(spec=Group)
        group.name = 'group'
        department = Mock(spec=models.Department)
        department.id = 1
        department.group = group
        cls.department = department
        cls.group = group

    def test_department_serializer(self):
        data = auth_serializers.DepartmentSerializer(self.department).data
        expected_keys = {'id', 'group', 'superior', 'admin', 'short_name'}
        self.assertEqual(expected_keys, set(data.keys()))

    @patch('django.contrib.auth.models.Group.objects.create',
           return_none_instance(Group))
    @patch('Core.models.auth.Department.objects.create',
           return_none_instance(models.Department))
    def test_department_serializer_create(self):
        data = {
            'short_name': 'dep',
            'group': {
                'name': 'group',
            }
        }
        serializer = auth_serializers.DepartmentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data = auth_serializers.DepartmentSerializer(self.department).data
        expected_keys = {'id', 'group', 'superior', 'admin', 'short_name'}
        self.assertEqual(expected_keys, set(data.keys()))

    def test_department_list_serializer(self):
        data = auth_serializers.DepartmentListSerializer(self.department).data
        expected_keys = {'id', 'superior', 'admin', 'short_name'}
        self.assertEqual(expected_keys, set(data.keys()))


class WorkOrderSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        work_order = Mock(spec=models.WorkOrder)
        work_order.id = 1
        work_order.count = 0
        work_order.sell_type = 0
        cls.work_order = work_order

    def test_work_order_serializer(self):
        data = work_order_serializers.WorkOrderSerializer(self.work_order).data
        expected_keys = {'id', 'uid', 'sell_type', 'client', 'project',
                         'product', 'count', 'finished', 'pretty_sell_type'}
        self.assertEqual(expected_keys, set(data.keys()))


class SubWorkOrderSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sub_order = Mock(spec=models.SubWorkOrder)
        sub_order.id = 1
        sub_order.index = 1
        cls.sub_order = sub_order

    def test_sub_work_order_serializer(self):
        data = work_order_serializers.SubWorkOrderSerializer(
            self.sub_order).data
        expected_keys = {'id', 'work_order', 'index', 'finished'}
        self.assertEqual(expected_keys, set(data.keys()))
