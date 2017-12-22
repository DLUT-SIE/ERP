from django.db import models
from django.contrib.auth.models import User

from Procurement import COMMENT_USER_CHOICES


class BaseComment(models.Model):
    user = models.ForeignKey(User, verbose_name='用户',
                             on_delete=models.CASCADE)
    comment = models.CharField(verbose_name='意见内容', max_length=200)
    submit_dt = models.DateTimeField(verbose_name='提交时间',
                                     auto_now_add=True)

    class Meta:
        abstract = True


class BiddingComment(BaseComment):
    """
    标单评审意见
    """
    bidding_sheet = models.ForeignKey('BiddingSheet', verbose_name='标单',
                                      on_delete=models.CASCADE)
    # TODO: Auto relate to UserInfo?
    user_title = models.IntegerField(verbose_name='审批人头衔',
                                     choices=COMMENT_USER_CHOICES)

    class Meta:
        verbose_name = '标单评审意见'
        verbose_name_plural = '标单评审意见'

    def __str__(self):
        return '{}:{}'.format(self.bidding_sheet, self.user)


class SubApplyComment(BaseComment):
    """
    材料代用评审意见
    """
    sub_apply = models.ForeignKey('MaterialSubApply',
                                  verbose_name='材料代用申请单',
                                  related_name='sub_spply_comments',
                                  on_delete=models.CASCADE)
    user_title = models.IntegerField(verbose_name='审批人属性',
                                     choices=COMMENT_USER_CHOICES)

    class Meta:
        verbose_name = '材料代用评审意见'
        verbose_name_plural = '材料代用评审意见'

    def __str__(self):
        return '{}:{}'.format(self.sub_apply, self.user)
