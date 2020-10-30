from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'inn', 'balance', 'first_name', 'last_name']


class TransferMoneySerializer(serializers.Serializer):
    user_from = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    inn_to = serializers.CharField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
