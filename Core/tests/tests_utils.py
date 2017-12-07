import uuid
import os.path as osp
import hashlib

from django.test import TestCase
from django.core import exceptions
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth.models import User

from Core.utils import gen_uuid, DynamicHashPath, Transition


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

        class Object:
            pass

        instance = Object()
        instance.path = SimpleUploadedFile('UploadFile.txt', b'file content')
        path = hash_pather(instance, 'UploadFile.txt')

        hasher = hashlib.md5()
        hasher.update(b'file content')
        fingerprint = hasher.hexdigest()
        fname, ext = osp.splitext('UploadFile.txt')
        prefix = hash_pather.base + timezone.now().strftime('/%Y/%m/%d')
        target_path = '{0}/{1}_{2}{3}'.format(prefix, fname, fingerprint, ext)
        self.assertEqual(path, target_path)


class RequestUserObject(object):
    def __init__(self):
        self.user = User.objects.get()


class TransitionTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='user', password='123456')
        self.request = RequestUserObject()

    def test_has_perm(self):
        # default
        trans = Transition(None, None, None)
        self.assertIs(trans._has_perm(None, self.request), True)
        # bool
        trans = Transition(None, None, None, permission=False)
        self.assertIs(trans._has_perm(None, self.request), False)
        # str
        trans = Transition(None, None, None,
                           permission='Core.add_userinfo')
        self.assertIs(trans._has_perm(None, self.request), False)

        # callable
        def fake_perm_func(inst, request):
            return False

        trans = Transition(None, None, None, permission=fake_perm_func)
        self.assertIs(trans._has_perm(None, self.request), False)
        # others
        trans = Transition(None, None, None, permission=1)
        self.assertIs(trans._has_perm(None, self.request), False)

    def test_can_trans(self):
        # match
        self.assertIs(Transition(0, 0, None)._can_trans(self.request), True)

        # all
        self.assertIs(Transition(0, '*', None)._can_trans(self.request), True)

        # iterable
        self.assertIs(Transition(0, [1, 2], None)._can_trans(self.request),
                      False)

        # fail
        self.assertIs(Transition(0, 5, None)._can_trans(self.request), False)

    def test_match_conds(self):
        # default
        trans = Transition(None, None, None)
        self.assertIs(trans._match_conds(None, self.request), True)

        # bool
        trans = Transition(None, None, None, conditions=False)
        self.assertIs(trans._match_conds(None, self.request), False)

        # callable
        def fake_cond_func(inst, request):
            return False

        trans = Transition(None, None, None, conditions=fake_cond_func)
        self.assertIs(trans._match_conds(None, self.request), False)

        # others
        trans = Transition(None, None, None, conditions=5)
        self.assertIs(trans._match_conds(None, self.request), False)

    def test_call_raise_exception(self):
        trans = Transition(None, None, None, permission=False)(None)
        with self.assertRaises(exceptions.PermissionDenied):
            trans(None, self.request)

        trans = Transition('field', 'source', 'target')(None)
        with self.assertRaises(exceptions.ValidationError):
            trans(None, self.request)

        trans = Transition('source', 'source', 'target',
                           conditions=False)(None)
        with self.assertRaises(exceptions.ValidationError):
            trans(None, self.request)
