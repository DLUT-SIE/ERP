from rest_framework import serializers
from Procurement import models


class BaseBiddingCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BiddingComment
        fields = ('id', 'user', 'comment', 'submit_dt', 'bidding_sheet',
                  'user_title')
