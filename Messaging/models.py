from django.db import models
from django.contrib.auth.models import User

from Core.utils import DynamicHashPath
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
            category=MESSAGE_CATEGORY_PERSONAL)


class Message(models.Model):
    """
    消息
    """
    title = models.CharField(verbose_name='标题', blank=True, max_length=200)
    content = models.TextField(verbose_name='内容', blank=True)
    source = models.ForeignKey(User, verbose_name='发送者',
                               related_name='message_source',
                               on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, verbose_name='接收者',
                                  blank=True, null=True,
                                  related_name='message_recipient',
                                  on_delete=models.SET_NULL)
    create_dt = models.DateTimeField(verbose_name='创建时间',
                                     auto_now_add=True)
    category = models.IntegerField(verbose_name='类型',
                                   choices=MESSAGE_CATEGORY_CHOICES)
    read = models.BooleanField(verbose_name='是否阅读', default=False)

    def __str__(self):
        return '{}:{}'.format(self.get_category_display(), self.title)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'


class News(Message):
    # TODO: Create message of this category directly
    objects = NewsManager()

    class Meta:
        proxy = True


class Announcement(Message):
    objects = AnnouncementManager()

    class Meta:
        proxy = True


class PersonalMessage(Message):
    objects = PersonalMessageManger()

    class Meta:
        proxy = True


class PublicFileManager(models.Manager):
    def get_queryset(self):
        return super(PublicFileManager, self).get_queryset().exclude(
            message__category=MESSAGE_CATEGORY_PERSONAL).select_related(
                'message')


class MessageFile(models.Model):
    """
    消息文件
    """
    path = models.FileField(verbose_name='路径',
                            upload_to=DynamicHashPath('MessageFile'))
    message = models.ForeignKey(Message, verbose_name='消息')

    # Custom managers
    objects = models.Manager()
    public_files = PublicFileManager()

    class Meta:
        verbose_name = '消息文件'
        verbose_name_plural = '消息文件'

    def __str__(self):
        return self.path.name
