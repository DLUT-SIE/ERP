from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from Messaging import (MESSAGE_CATEGORY_NEWS, MESSAGE_CATEGORY_ANNOUNCEMENT,
                       MESSAGE_CATEGORY_PERSONAL)
from Messaging.models import (Message, News, Announcement, PersonalMessage,
                              MessageFile)


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
        expected_str = '{}:{}'.format(msg.get_category_display(), msg.title)
        self.assertEqual(str(msg), expected_str)

    def test_news_manager_count(self):
        news_count = News.objects.all().count()
        self.assertEqual(news_count, 1)

    def test_announcements_manager_count(self):
        announcements_count = Announcement.objects.all().count()
        self.assertEqual(announcements_count, 2)

    def test_personal_message_manager_count(self):
        personal_message_count = PersonalMessage.objects.all().count()
        self.assertEqual(personal_message_count, 4)


class MessageFileTest(TestCase):
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
        MessageFile.objects.create(
            path=upload_file,
            message=news)
        for _ in range(2):
            MessageFile.objects.create(
                path=upload_file,
                message=pm)

    def test_str(self):
        message_file = MessageFile.objects.all()[0]
        self.assertIn('UploadFile', str(message_file))

    def test_public_files(self):
        files_count = MessageFile.public_files.all().count()
        self.assertEqual(files_count, 1)
