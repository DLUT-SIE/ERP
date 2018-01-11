from unittest.mock import patch

from django.test import TestCase
from model_mommy import mommy

from Core.models import Department


class UserInfoTest(TestCase):
    def test_str(self):
        username = 'username'
        name = 'name'
        user_info = mommy.prepare(
            'UserInfo', user__username=username, user__first_name=name)
        expected_str = '{}(用户名:{})'.format(
            name, username)
        self.assertEqual(str(user_info), expected_str)


class DepartmentTest(TestCase):
    def test_str(self):
        name = 'group'
        department = mommy.prepare('Department', group__name=name)
        self.assertEqual(str(department), name)

    @patch('Core.models.auth.Department.objects')
    def test_get_departments_dict(self, mocked_objects):
        objects = mommy.prepare('Department', _quantity=4)
        mocked_objects.all.return_value = mocked_objects
        mocked_objects.select_related.return_value = objects
        departments = {
            d.group.name: d.id
            for d in Department.objects.all().select_related('group')}
        for key, val in Department.get_departments_dict().items():
            self.assertIn(key, departments)
            self.assertEqual(val, departments[key])

    @patch('django.db.models.Manager.get_queryset')
    def test_special_department(self, mocked_queryset):
        mocked_queryset.return_value = mocked_queryset
        mocked_queryset.filter.return_value = mocked_queryset
        mocked_queryset.select_related.return_value = mocked_queryset
        dep = mommy.prepare('Department')
        mocked_queryset.get.return_value = dep
        self.assertEqual(Department.distribution.get(), dep)
        self.assertEqual(Department.process.get(), dep)
        self.assertEqual(Department.procurement.get(), dep)
        self.assertEqual(Department.production.get(), dep)


class WorkOrderTest(TestCase):
    def test_str(self):
        uid = '1'
        work_order = mommy.prepare('WorkOrder', uid=uid)
        self.assertEqual(str(work_order), uid)


class SubWorkOrderTest(TestCase):
    def test_str(self):
        sub_order = mommy.prepare('SubWorkOrder', work_order_id='1', index=1)
        expected_str = '1-1'
        self.assertEqual(str(sub_order), expected_str)

    def test_uid(self):
        sub_order = mommy.prepare('SubWorkOrder', work_order__uid='5', index=1)
        expected_str = '5-1'
        self.assertEqual(sub_order.uid, expected_str)
