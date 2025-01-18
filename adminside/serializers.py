from rest_framework import serializers
from .models import *
from contact_form.serializers import LabelSerializer

    

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class CronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cron
        fields ='__all__'

class TypeSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=NewLabel.objects.all())

    class Meta:
        model = Type
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'


class PaymentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentConfig
        fields = '__all__'

class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = '__all__'

class LabelAPIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelAPIConfig
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'
    
class WeightSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=NewLabel.objects.all())

    class Meta:
        model = Weight
        fields = '__all__'

class newLableSerializer(serializers.ModelSerializer):
    class Meta:
        model = newLabel
        fields = '__all__'

