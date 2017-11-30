import uuid
import os.path as osp
import hashlib

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Core.utils import gen_uuid, DynamicHashPath


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
        prefix = hash_pather.base + '/%Y/%m/%d'
        target_path = '{0}/{1}_{2}{3}'.format(prefix, fname, fingerprint, ext)
        self.assertEqual(path, target_path)
