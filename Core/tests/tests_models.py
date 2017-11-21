from django.test import TestCase
from django.contrib.auth.models import User

from Core import SELL_TYPE_DOMESTIC, WELD_ROD, GENDER_MALE
from Core.models import (WorkOrder, SubWorkOrder, Material,
                         Materiel, UserInfo, Department)


class WorkOrderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        WorkOrder.objects.create(
            uid='123456',
            sell_type=SELL_TYPE_DOMESTIC,
            client='client',
            project='project',
            product='product',
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
        # SubWorkOrder will be created automatically when WorkOrder created
        WorkOrder.objects.create(
            uid='123456',
            sell_type=SELL_TYPE_DOMESTIC,
            client='client',
            project='project',
            product='product',
            count=10)

    def test_work_order(self):
        work_order = WorkOrder.objects.all()[0]
        sub_order = work_order.subworkorder_set.all()[0]
        self.assertIs(sub_order.work_order, work_order)

    def test_index(self):
        sub_order = SubWorkOrder.objects.all()[0]
        self.assertEqual(sub_order.index, 1)

    def test_name(self):
        sub_order = SubWorkOrder.objects.all()[0]
        expected_name = '{}-{}'.format(sub_order.work_order.uid, 1)
        self.assertEqual(sub_order.name, expected_name)

    def test_str(self):
        sub_order = SubWorkOrder.objects.all()[0]
        self.assertEqual(str(sub_order), sub_order.name)


class MaterialTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Material.objects.create(
            name='material',
            material_id='123456',
            category=WELD_ROD)

    def test_str(self):
        material = Material.objects.all()[0]
        self.assertEqual(str(material), material.name)


class MaterielTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        work_order = WorkOrder.objects.create(
            uid='123456',
            sell_type=SELL_TYPE_DOMESTIC,
            client='client',
            project='project',
            product='product',
            count=10)
        material = Material.objects.create(
            name='material',
            material_id='123456',
            category=WELD_ROD)
        Materiel.objects.create(
            work_order=work_order,
            index='index',
            sub_index='sub_index',
            schematic_index='schematic_index',
            parent_schematic_index='parent_schematic_index',
            parent_name='parent_name',
            material=material,
            name='materiel',
            count='5',
            net_weight=10,
            total_weight=50,
            quota=8,
            quota_coefficient=1.1,
            remark='remark',
            specification='spec',
            standard='standard',
            unit='unit',
            status='status',
            press='press',
            recheck='recheck',
            detection_level='detection_level')

    def test_total_weight_cal(self):
        materiel = Materiel.objects.all()[0]
        total = int(materiel.count) * materiel.net_weight
        self.assertAlmostEqual(materiel.total_weight_cal(), total)

    def test_str(self):
        materiel = Materiel.objects.all()[0]
        self.assertEqual(str(materiel), materiel.name)


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
        self.assertEqual(str(user_info), user_info.user.first_name)


class DepartmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='user',
            password='password',
            first_name='first name',
            last_name='last name')
        Department.objects.create(
            admin=user,
            name='department',
            short_name='dep')

    def test_str(self):
        department = Department.objects.all()[0]
        self.assertEqual(str(department), department.name)
