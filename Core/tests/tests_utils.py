import uuid
import os.path as osp
import hashlib

from unittest.mock import Mock, MagicMock

from django.test import TestCase
from django.core import exceptions
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth.models import User

from Core.utils import gen_uuid, DynamicHashPath
from Core.utils.fsm import Transition


class GenUUIDTest(TestCase):
    def test_uuid(self):
        uid = gen_uuid()
        self.assertIsInstance(uid, uuid.UUID)


class DynamicHashPathTest(TestCase):
    def test_eq(self):
        hash_pather1 = DynamicHashPath('dynamic')
        hash_pather2 = DynamicHashPath('dynamic')
        self.assertEqual(hash_pather1, hash_pather2)

    def test_call(self):
        hash_pather = DynamicHashPath('dynamic')

        instance = Mock()
        instance.path = SimpleUploadedFile('UploadFile.txt', b'file content')
        path = hash_pather(instance, 'UploadFile.txt')

        hasher = hashlib.md5()
        hasher.update(b'file content')
        fingerprint = hasher.hexdigest()
        fname, ext = osp.splitext('UploadFile.txt')
        prefix = hash_pather.base + timezone.now().strftime('/%Y/%m/%d')
        target_path = '{0}/{1}/{2}{3}'.format(prefix, fingerprint, fname, ext)
        self.assertEqual(path, target_path)

    def test_call_without_date(self):
        hash_pather = DynamicHashPath('dynamic', False)

        instance = Mock()
        instance.path = SimpleUploadedFile('UploadFile.txt', b'file content')
        path = hash_pather(instance, 'UploadFile.txt')

        hasher = hashlib.md5()
        hasher.update(b'file content')
        fingerprint = hasher.hexdigest()
        fname, ext = osp.splitext('UploadFile.txt')
        prefix = hash_pather.base
        target_path = '{0}/{1}/{2}{3}'.format(prefix, fingerprint, fname, ext)
        self.assertEqual(path, target_path)


class TransitionTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='user', password='123456')
        self.request = Mock()
        self.request.user = Mock(spec=User)
        self.request.user.has_perm.return_value = False
        self.inst = MagicMock()
        self.inst.field = 0

    def test_has_perm(self):
        # default
        trans = Transition(None, 'field', None, None)
        self.assertIs(trans._has_perm(None, self.request), True)
        # bool
        trans = Transition(None, 'field', None, None, permission=False)
        self.assertIs(trans._has_perm(None, self.request), False)
        # str
        trans = Transition(None, 'field', None, None,
                           permission='Core.add_userinfo')
        self.assertIs(trans._has_perm(self.inst, self.request), False)

        # callable
        fake_perm_func = Mock()
        fake_perm_func.return_value = False
        trans = Transition(None, 'field', None, None,
                           permission=fake_perm_func)
        self.assertIs(trans._has_perm(self.inst, self.request), False)
        # others
        trans = Transition(None, 'field', None, None, permission=1)
        self.assertIs(trans._has_perm(self.inst, self.request), False)

    def test_can_trans(self):
        # match
        trans = Transition(None, 'field', 0, None)
        self.assertIs(trans._can_trans(self.inst, self.request), True)

        # all
        trans = Transition(None, 'field', '*', None)
        self.assertIs(trans._can_trans(self.inst, self.request), True)

        # iterable
        trans = Transition(None, 'field', [1, 2], None)
        self.assertIs(trans._can_trans(self.inst, self.request), False)

        # fail
        trans = Transition(None, 'field', 5, None)
        self.assertIs(trans._can_trans(self.inst, self.request), False)

    def test_match_conds(self):
        # default
        trans = Transition(None, 'field', None, None)
        self.assertIs(trans._match_conds(self.inst, self.request), True)

        # bool
        trans = Transition(None, 'field', None, None, conditions=False)
        self.assertIs(trans._match_conds(self.inst, self.request), False)

        # callable
        fake_cond_func = Mock()
        fake_cond_func.return_value = False
        trans = Transition(None, 'field', None, None,
                           conditions=fake_cond_func)
        self.assertIs(trans._match_conds(self.inst, self.request), False)

        # others
        trans = Transition(None, 'field', None, None, conditions=5)
        self.assertIs(trans._match_conds(self.inst, self.request), False)

    def test_call_raise_exception(self):
        trans = Transition(None, 'field', None, None, permission=False)
        trans.inst = self.inst
        with self.assertRaises(exceptions.PermissionDenied):
            trans(self.request)

        trans = Transition(None, 'field', 'source', 'target')
        trans.inst = self.inst
        with self.assertRaises(exceptions.ValidationError):
            trans(self.request)

        trans = Transition(None, 'field', 'source', 'target', conditions=False)
        trans.inst = self.inst
        with self.assertRaises(exceptions.ValidationError):
            trans(self.request)

    def test_check_validity(self):
        trans = Transition(None, 'field', None, None, permission=False)
        self.assertIs(trans.check_validity(self.inst, self.request, False),
                      False)

        trans = Transition(None, 'field', '*', None, conditions=False)
        self.assertIs(trans.check_validity(self.inst, self.request, False),
                      False)
        trans = Transition(None, 'field', '*', None, conditions=False)
        with self.assertRaises(exceptions.ValidationError):
            trans.check_validity(self.inst, self.request)
