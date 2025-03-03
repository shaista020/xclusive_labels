from rest_framework import serializers
from .models import *
from adminside.models import *
class NotificationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)  
    created_by = serializers.CharField(source="created_by.username", read_only=True)   
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at', 'user', 'username', 'created_by', 'color']  

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields ='__all__'


class SavePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields ='__all__'



class TicketSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Ticket
        fields = '__all__'

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewLabel
        fields = '__all__' 

class OrderSerializer(serializers.ModelSerializer):
    new_label = LabelSerializer()  # Include the NewLabel data in the Order

    class Meta:
        model = Order
        fields = '__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class AddFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFund
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
    
class ShipFromAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipFromAddress
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'




class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class StateShipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateShipmentData
        fields = '__all__'