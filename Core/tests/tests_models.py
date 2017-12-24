from unittest.mock import Mock

from django.test import TestCase
from django.contrib.auth.models import User, Group

from Core.models import (WorkOrder, SubWorkOrder,
                         UserInfo, Department)


class WorkOrderTest(TestCase):
    def test_str(self):
        uid = '123456'
        work_order = WorkOrder(uid=uid)
        self.assertEqual(str(work_order), uid)


class SubWorkOrderTest(TestCase):
    def test_str(self):
        sub_order = SubWorkOrder()
        work_order = Mock(spec=WorkOrder)
        work_order._state = Mock()
        work_order.__str__ = Mock()
        work_order.__str__.return_value = '1'
        sub_order.work_order = work_order
        sub_order.index = 1
        expected_str = '1-1'
        self.assertEqual(str(sub_order), expected_str)


class UserInfoTest(TestCase):
    def test_str(self):
        user_info = UserInfo()
        user = Mock(spec=User)
        user._state = Mock()
        user.username = 'username'
        user.first_name = 'first_name'
        user_info.user = user
        expected_str = '{}(用户名:{})'.format(
            user.first_name, user.username)
        self.assertEqual(str(user_info), expected_str)


class DepartmentTest(TestCase):
    def test_str(self):
        department = Department()
        group = Mock(spec=Group)
        group._state = Mock()
        group.name = 'group'
        department.group = group
        expected_str = 'group'
        self.assertEqual(str(department), expected_str)
