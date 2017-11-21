import uuid
from django.test import TestCase

from Core.utils import gen_uuid


class GenUUIDTest(TestCase):
    def test_uuid(self):
        uid = gen_uuid()
        self.assertIsInstance(uid, uuid.UUID)
