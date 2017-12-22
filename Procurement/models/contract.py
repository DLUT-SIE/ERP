from django.db import models
from django.contrib.auth.models import User


class ContractDetail(models.Model):
    """
    合同金额明细
    """
    bidding_sheet = models.ForeignKey('BiddingSheet', verbose_name='标单',
                                      on_delete=models.CASCADE)
    submitter = models.ForeignKey(User, verbose_name='提交用户',
                                  on_delete=models.CASCADE)
    submit_dt = models.DateTimeField(verbose_name='提交时间',
                                     auto_now_add=True)
    amount = models.FloatField(verbose_name='金额')

    class Meta:
        verbose_name = '合同金额明细'
        verbose_name_plural = '合同金额明细'

    def __str__(self):
        return '{}:{}'.format(self.bidding_sheet, self.amount)
