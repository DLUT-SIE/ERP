from Procurement import models
from Procurement.serializers import (BaseDynamicFieldSerializer,)


class BaseBiddingCommentSerializer(BaseDynamicFieldSerializer):
    class Meta:
        model = models.BiddingComment
        fields = ('id', 'user', 'comment', 'submit_dt', 'bidding_sheet',
                  'user_title')
