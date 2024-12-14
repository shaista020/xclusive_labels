from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
# from adminside.models import CustomUser
# User = CustomUser   
# class Notification(models.Model):
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     send_by = models.ForeignKey(User, related_name='seen_notifications', on_delete=models.CASCADE)
#     send_to = models.ForeignKey(User, related_name='review_notifications', on_delete=models.CASCADE)
#     is_seen = models.BooleanField()

#     def __str__(self):
#         return f'Notification from {self.send_by} to {self.send_to}'
    
class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class Package(models.Model):
  
    name = models.CharField(max_length=255)  
    weight = models.DecimalField(max_digits=10, decimal_places=2)  
    length = models.DecimalField(max_digits=5, decimal_places=2)  
    width = models.DecimalField(max_digits=5, decimal_places=2)   
    height = models.DecimalField(max_digits=5, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 

    def __str__(self):
        return self.name



class Ticket(models.Model):
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    message = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 

    def __str__(self):
        return self.title



# class Order(models.Model):
   
#     STATUS_CHOICES = [
#          ('select', 'Select'),
#         ('in_queue', 'In Queue'),
#         ('processing', 'Processing'),
#         ('awaiting', 'Awaiting'),
#         ('in_progress', 'In Progress'),
#         ('delivered', 'Delivered'),
#         ('complete', 'Complete'),
#         ('cancelled', 'Cancelled'),
#         ('none', 'None'),
#     ]
    
#     batch_number = models.CharField(max_length=255)
#     tracking_number = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=100)
#     weight = models.FloatField()
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(
#         max_length=100,
#         choices=STATUS_CHOICES,
#         default='Select'
#     )
    
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.tracking_number
    
class Payment(models.Model):
    payment_number = models.CharField(max_length=255)
    gateway = models.CharField(max_length=255)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    request_balance = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
          ('select', 'Select'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Select')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 

    def __str__(self):
        return f"Payment #{self.payment_number}"
    
class AddFund(models.Model):
    PAYMENT_METHOD_CHOICES = [
          ('select', 'Select'),
        ('credit_debit_card', 'Credit/Debit Card (instantly)'),
        ('crypto_currency', 'Crypto Currency (instantly)'),
        ('venmo', 'Venmo (2-3 hours)'),
        ('cashapp', 'CashApp (2-3 hours)'),
        ('zelle', 'Zelle (2-3 hours)')
    ]

    credit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES,default='Select')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 
  

    def __str__(self):
        return f"${self.credit} via {self.payment_method}"

from django.db import models

class Store(models.Model):
   
    STORE_TYPE_CHOICES = [
         ('select', 'Select'),
        ('Retail', 'Retail'),
        ('Online', 'Online'),
        ('Wholesale', 'Wholesale'),
        ('Others', 'Others'),
    ]
 

    name = models.CharField(max_length=255,null=True)
    url = models.URLField(null=True)
    description = models.TextField(null=True)
    store_type = models.CharField(max_length=100, choices=STORE_TYPE_CHOICES, default='select')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 

    def __str__(self):
        return self.name




class Address(models.Model):
    name = models.CharField(max_length=255)
    company_reference = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    apt_unit_suite = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=100, null= True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 
    def _str_(self):
        return self.name
class ShipFromAddress(models.Model):
    full_name = models.CharField(max_length=255)
    company_reference = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    apt_unit_suite = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.full_name} - {self.address}'
     
TIMEZONE_CHOICES = [
    ('GMT-05:00', 'Eastern Time (US & Canada)'),
    ('GMT-06:00', 'Central Time (US & Canada)'),
    ('GMT+10:00', 'Guam'),
    ('GMT+10:00', 'Yakutsk'),
    ('GMT+09:00', 'Tokyo'),
    ('GMT+09:00', 'Seoul'),
    ('GMT+12:00', 'Auckland'),
]
class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    timezone = models.CharField(max_length=20, choices=TIMEZONE_CHOICES, default='GMT-05:00')
    two_fa_enabled = models.BooleanField(default=False, verbose_name="2FA Authentication")

    def __str__(self):
        return self.user.username 
    
class Coupon(models.Model):
    code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    
class Referral(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    available_for_withdraw = models.DecimalField(max_digits=10, decimal_places=2)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class NewLabel(models.Model):
    # delivery_type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=255)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    ship_from = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    apt_unit = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 

    def __str__(self):
        return f"Label for {self.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('select', 'Select'),
        ('in_queue', 'In Queue'),
        ('processing', 'Processing'),
        ('awaiting', 'Awaiting'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('none', 'None'),
    ]

    # Link Order to NewLabel (ForeignKey)
    new_label = models.ForeignKey(NewLabel, on_delete=models.CASCADE)

    tracking_number = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    weight = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='Select'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)  
    status = models.CharField(max_length=50)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"

class StateShipmentData(models.Model):
    state = models.CharField(max_length=100)
    shipments_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.state