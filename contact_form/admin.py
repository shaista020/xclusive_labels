from django.contrib import admin
from .models import *

# Registering models with custom admin classes
admin.site.register(ContactInfo)
admin.site.register(Package)
# admin.site.register(Chat)
admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(AddFund)
admin.site.register(Store)
admin.site.register(Address)
admin.site.register(ShipFromAddress)
admin.site.register(Profile)
admin.site.register(Coupon)
admin.site.register(Referral)
admin.site.register(NewLabel)
admin.site.register(StateShipmentData)
admin.site.register(Transaction)