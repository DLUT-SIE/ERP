from unittest.mock import Mock, patch

from django.test import TestCase
from django.contrib.auth.models import User, Group

from Core.models import (WorkOrder, SubWorkOrder,
                         UserInfo, Department)


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


def return_fake_department():
    department = Department()
    group = Mock(spec=Group)
    group._state = Mock()
    group.name = 'group'
    group.id = 5
    department.group = group

    def _wrapper():
        return [department]
    return _wrapper


class DepartmentTest(TestCase):
    def test_str(self):
        department = Department()
        group = Mock(spec=Group)
        group._state = Mock()
        group.name = 'group'
        department.group = group
        expected_str = 'group'
        self.assertEqual(str(department), expected_str)

    @patch('Core.models.auth.Department.objects.all', return_fake_department())
    def test_get_departments_dict(self):
        departments = {d.group.name: d.id for d in Department.objects.all()}
        for key, val in Department.get_departments_dict().items():
            self.assertIn(key, departments)
            self.assertEqual(val, departments[key])

    @patch('django.db.models.Manager.get_queryset')
    def test_special_department(self, mocked_queryset):
        mocked_queryset.return_value = mocked_queryset
        mocked_queryset.filter.return_value = mocked_queryset
        mocked_queryset.get.return_value = None
        self.assertEqual(Department.distribution.get(), None)
        self.assertEqual(Department.process.get(), None)
        self.assertEqual(Department.procurement.get(), None)
        self.assertEqual(Department.production.get(), None)


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
