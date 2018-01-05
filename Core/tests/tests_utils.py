import uuid
import os.path as osp
import hashlib

from unittest.mock import Mock, MagicMock

from django.test import TestCase
from django.core import exceptions
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers

from Core.utils import gen_uuid, DynamicHashPath, DynamicFieldSerializerMixin
from Core.utils.fsm import Transition, TransitionSerializerMixin


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
        self.request = Mock()
        self.request.user = Mock(spec=User)
        self.request.user.has_perm.return_value = False
        self.inst = MagicMock()
        self.inst.valid_method.return_value = True
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

    def test_match_source(self):
        # match
        trans = Transition(None, 'field', 0, None)
        self.assertIs(trans._match_source(self.inst, self.request), True)

        # all
        trans = Transition(None, 'field', '*', None)
        self.assertIs(trans._match_source(self.inst, self.request), True)

        # iterable
        trans = Transition(None, 'field', [1, 2], None)
        self.assertIs(trans._match_source(self.inst, self.request), False)

        # fail
        trans = Transition(None, 'field', 5, None)
        self.assertIs(trans._match_source(self.inst, self.request), False)

    def test_match_conds(self):
        # default
        method = Mock()
        method.__name__ = 'method'
        trans = Transition(method, 'field', None, None)
        self.assertIs(trans._match_conds(self.inst, self.request), True)

        # bool
        trans = Transition(method, 'field', None, None, conditions=False)
        self.assertIs(trans._match_conds(self.inst, self.request), False)

        # str
        trans = Transition(method, 'field', None, None,
                           conditions='valid_method')
        self.assertIs(trans._match_conds(self.inst, self.request), True)

        # callable
        fake_cond_func = Mock()
        fake_cond_func.return_value = False
        trans = Transition(method, 'field', None, None,
                           conditions=fake_cond_func)
        self.assertIs(trans._match_conds(self.inst, self.request), False)

        # others
        trans = Transition(method, 'field', None, None, conditions=5)
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


class TransitionSerializerMixinTest(TestCase):
    def setUp(self):
        obj = Mock()
        obj.actions.return_value = {'action': 1}
        obj.status = 0
        trans = Mock()
        trans._match_source.return_value = False
        trans.check_validity.side_effect = exceptions.ValidationError('error')
        trans.field_name = 'status'
        trans.method.__name__ = 'name'
        obj.transitions.items.return_value = {'_': trans}.items()
        self.obj = obj
        self.trans = trans

    def test_get_actions(self):
        serializer = TransitionSerializerMixin()
        serializer.context['request'] = Mock()
        actions = serializer.get_actions(self.obj)
        self.assertEqual({'action': 1}, actions)

    def test_run_transition_validator_no_valid_trans_error(self):
        serializer = TransitionSerializerMixin()
        serializer.context['request'] = Mock()
        serializer.instance = self.obj
        with self.assertRaises(serializers.ValidationError):
            serializer._run_transitions_validator({'status': 1})

    def test_run_transition_validator_check_validity_error(self):
        self.trans._match_source.return_value = True
        self.trans.target = 1
        serializer = TransitionSerializerMixin()
        serializer.context['request'] = Mock()
        serializer.instance = self.obj
        with self.assertRaises(serializers.ValidationError):
            serializer._run_transitions_validator({'status': 1})


class DynamicFieldSerializerMixinTest(TestCase):
    def setUp(self):
        request = Mock()
        request.query_params = {'fields': 'a,b,c'}
        kwargs = {
            'context': {
                'request': request,
            }
        }
        self.kwargs = kwargs
        self.request = request

    def test_pop_fields(self):
        DynamicFieldSerializerMixin.fields = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        serializer = DynamicFieldSerializerMixin(**self.kwargs)
        self.assertEqual({'a', 'b', 'c'}, set(serializer.fields.keys()))

    def test_invalid_query_params(self):
        self.request.query_params['fields'] = 5  # Not really happens
        DynamicFieldSerializerMixin.fields = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        serializer = DynamicFieldSerializerMixin(**self.kwargs)
        self.assertEqual(set(), set(serializer.fields.keys()))
