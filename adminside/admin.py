from django.contrib import admin
from .models import *

@admin.register(Batch)
class BatchfoAdmin(admin.ModelAdmin):
    list_display = ('batch_id','ship_from_name','type','weight','cost','ship_date','status','created_at')



@admin.register(Cron)
class CronAdmin(admin.ModelAdmin):
    list_display = ('label', 'register_at')



@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
      list_display = ('id', 'label', 'type_name', 'unit', 'value', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
      list_display = ('payment_number','name','email','gateway','previous_balance','request_balance','new_balance','request_at','status')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
     list_display=('id','email','duration','requested_on')



@admin.register(PaymentConfig)
class PaymentConfigAdmin(admin.ModelAdmin):
    list_display = ('stripe_key', 'coinbase_key', 'venmo_email', 'cashapp_email', 'zelle_email')


@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'smtp_host', 'smtp_port')


@admin.register(LabelAPIConfig)
class LabelAPIConfigAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'host')

# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('title', 'ticket_type', 'data_id', 'status', 'created_at')
  
@admin.register(AdminUser)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'email_address')
        }),
        ('Account Details', {
            'fields': ('verified', 'timezone', 'current_balance', 'total_spent'),
        }),
    )

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
     list_display =('id', 'label', 'from_weight', 'to_weight', 'user_cost', 'reseller_cost', 'created_at')



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
       class Meta:
        model = Notification
        fields = '__all__'

 
@admin.register(newLabel)
class newLabelAdmin(admin.ModelAdmin):
     class Meta:
        model = newLabel
        fields = '__all__' 
admin.site.register(CustomUser) 