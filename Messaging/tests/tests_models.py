from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from Messaging import (MESSAGE_CATEGORY_NEWS, MESSAGE_CATEGORY_ANNOUNCEMENT,
                       MESSAGE_CATEGORY_PERSONAL)
from Messaging.models import Message, DocumentFile


class MessageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user1', password='user1')
        user2 = User.objects.create_user(username='user2', password='user2')
        Message.objects.create(
            title='news',
            content='123456',
            source=user1,
            category=MESSAGE_CATEGORY_NEWS)
        for _ in range(2):
            Message.objects.create(
                title='announcement',
                content='123456',
                source=user1,
                category=MESSAGE_CATEGORY_ANNOUNCEMENT)
        for _ in range(4):
            Message.objects.create(
                title='personal',
                content='123456',
                source=user1,
                recipient=user2,
                category=MESSAGE_CATEGORY_PERSONAL)

    def test_str(self):
        msg = Message.objects.all()[0]
        self.assertEqual(str(msg), msg.title)

    def test_news_manager_count(self):
        news_count = Message.news.all().count()
        self.assertEqual(news_count, 1)

    def test_announcements_manager_count(self):
        announcements_count = Message.announcements.all().count()
        self.assertEqual(announcements_count, 2)

    def test_personal_message_manager_count(self):
        personal_message_count = Message.personal_messages.all().count()
        self.assertEqual(personal_message_count, 4)


class DocumentFileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user1', password='user1')
        user2 = User.objects.create_user(username='user2', password='user2')
        news = Message.objects.create(
            title='news',
            content='123456',
            source=user1,
            category=MESSAGE_CATEGORY_NEWS)
        pm = Message.objects.create(
            title='personal',
            content='123456',
            source=user1,
            recipient=user2,
            category=MESSAGE_CATEGORY_PERSONAL)
        upload_file = SimpleUploadedFile('UploadFile.txt', b'file content')
        DocumentFile.objects.create(
            path=upload_file,
            name='UploadFile.txt',
            message=news)
        for _ in range(2):
            DocumentFile.objects.create(
                path=upload_file,
                name='UploadFile.txt',
                message=pm)

    def test_str(self):
        document = DocumentFile.objects.all()[0]
        self.assertEqual(str(document), document.name)

    def test_public_files(self):
        documents_count = DocumentFile.public_files.all().count()
        self.assertEqual(documents_count, 1)
