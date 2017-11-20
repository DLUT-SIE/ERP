import os

from django.db import models
from django.core.checks import Warning
from django.contrib.auth.models import User

from Messaging import (
    MESSAGE_CATEGORY_CHOICES, MESSAGE_CATEGORY_NEWS,
    MESSAGE_CATEGORY_ANNOUNCEMENT, MESSAGE_CATEGORY_PERSONAL)


class NewsManager(models.Manager):
    def get_queryset(self):
        return super(NewsManager, self).get_queryset().filter(
            category=MESSAGE_CATEGORY_NEWS)


class AnnouncementManager(models.Manager):
    def get_queryset(self):
        return super(AnnouncementManager, self).get_queryset().filter(
            category=MESSAGE_CATEGORY_ANNOUNCEMENT)


class PersonalMessageManger(models.Manager):
    def get_queryset(self):
        return super(PersonalMessageManger, self).get_queryset().filter(
            category=PersonalMessageManger)


class Message(models.Model):
    title = models.CharField(verbose_name='标题', blank=True, max_length=200)
    content = models.TextField(verbose_name='内容', blank=True)
    source = models.ForeignKey(User, verbose_name='发送者',
                               related_name='message_source',
                               on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, verbose_name='接收者',
                                  blank=True, null=True,
                                  related_name='message_recipient',
                                  on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name='创建时间',
                                       auto_now_add=True)
    category = models.IntegerField(verbose_name='类型',
                                   choices=MESSAGE_CATEGORY_CHOICES)
    read = models.BooleanField(verbose_name='是否阅读', default=False)

    # Custom managers
    news = NewsManager()
    announcements = AnnouncementManager()
    personal_messages = PersonalMessageManger()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'


class PublicFileManager(models.Manager):
    def get_queryset(self):
        return super(PublicFileManager, self).get_queryset().exclude(
            message__category=MESSAGE_CATEGORY_PERSONAL).select_related(
                'message')


class DocumentFile(models.Model):
    path = models.FileField(verbose_name='文件', upload_to='%Y/%m/%d')
    name = models.CharField(verbose_name='文件名', max_length=40)
    message = models.ForeignKey(Message, verbose_name='消息')

    # Custom managers
    public_files = PublicFileManager()

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = '文件'

    def document_name(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use .name instead')
        return os.path.basename(self.news_document.name)

    def __str__(self):
        return str(self.name)
