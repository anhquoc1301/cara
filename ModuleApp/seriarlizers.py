from rest_framework import serializers
from .models import User, PhaseUSDT, TradeUSDT


class ResultSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            user = User.objects.get(id=instance.user.id)
            user_code = user.code
            user_name = user.username
        except:
            user_code = ''
            user_name = ''
            
        representation['user_code'] = user_code
        representation['user_name'] = user_name

        return representation

    class Meta:
        model = TradeUSDT
        fields = ['trade_value', 'trade_value_win', 'trade_type']