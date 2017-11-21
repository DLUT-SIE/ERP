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
            category=MESSAGE_CATEGORY_PERSONAL)


class Message(models.Model):
    """
    消息

    Attributes
    ----------
    title : CharField
        标题
    content : TextField
        内容
    source : ForeignKey
        外键User, 发送者
    recipient : ForeignKey
        外键User, 接收者, 为空代表广播消息
    create_dt : DateTimeField
        创建时间
    category : IntegerField
        类型
    read : BooleanField
        是否阅读, 对recipient为空无效
    news : Manager
        Manager对象, 查询范围为公司新闻
    announcements : Manager
        Manager对象, 查询范围为重要通知
    personal_messages : Manager
        Manager对象, 查询范围为个人消息
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

    # Custom managers
    objects = models.Manager()
    news = NewsManager()
    announcements = AnnouncementManager()
    personal_messages = PersonalMessageManger()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'


class PublicFileManager(models.Manager):
    def get_queryset(self):
        return super(PublicFileManager, self).get_queryset().exclude(
            message__category=MESSAGE_CATEGORY_PERSONAL).select_related(
                'message')


class DocumentFile(models.Model):
    """
    消息文件

    Attributes
    ----------
    path : FileField
        路径
    name : CharField
        文件名
    message : ForeignKey
        外键Message, 消息
    public_files : Manager
        Manager对象, 查询范围为非个人消息文件
    """
    path = models.FileField(verbose_name='路径', upload_to='%Y/%m/%d')
    name = models.CharField(verbose_name='文件名', max_length=40)
    message = models.ForeignKey(Message, verbose_name='消息')

    # Custom managers
    objects = models.Manager()
    public_files = PublicFileManager()

    class Meta:
        verbose_name = '消息文件'
        verbose_name_plural = '消息文件'

    def document_name(self):
        """
        获取文件名

        note
        ----
        不赞成使用: 该函数将很快被移除，使用 `.name` 代替

        Returns
        -------
        str
            文件名
        """
        raise Warning('Deprecated: This will be removed soon, '
                      'use .name instead')
        return os.path.basename(self.path.name)

    def __str__(self):
        return self.name
