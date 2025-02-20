from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Abs
from decimal import Decimal
User = settings.AUTH_USER_MODEL
from decimal import Decimal
from django.db import models
# from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, DecimalField, Q
from django.db.models.functions import Abs

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField() 
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.message

class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ShippingClassDiscount(models.Model):
    shipping_class = models.CharField(max_length=100, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20)

    def __str__(self):
        return f"{self.shipping_class} - {self.discount_percentage}% discount"

class CompetitorRate(models.Model):
    weight = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_class = models.CharField(max_length=100, default='Standard')

    def __str__(self):
        return f"{self.length}x{self.width}x{self.height} - {self.rate}"


class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dynamic_pricing_enabled = models.BooleanField(default=False)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_class = models.CharField(max_length=100, default='Standard')

    def get_competitor_rate(self):
       
        weight = self.weight
        length = self.length
        width = self.width
        height = self.height
 
        exact_match = CompetitorRate.objects.filter(
            weight=weight, length=length, width=width, height=height
        ).order_by('rate').first()

        if exact_match:
            return exact_match
 
        closest_match = CompetitorRate.objects.filter(
            Q(weight__gte=weight - Decimal("0.5"), weight__lte=weight + Decimal("0.5")) &
            Q(length__gte=length - Decimal("1"), length__lte=length + Decimal("1")) &
            Q(width__gte=width - Decimal("1"), width__lte=width + Decimal("1")) &
            Q(height__gte=height - Decimal("1"), height__lte=height + Decimal("1"))
        ).order_by('rate').first()

        return closest_match

    def calculate_discounted_price(self):
        discount_percentage = self.discount / Decimal(100)

        if self.dynamic_pricing_enabled:
            competitor_rate = self.get_competitor_rate()

            if competitor_rate:
                self.original_price = competitor_rate.rate
            else:
               
                self.original_price = self.weight * Decimal(2)
 
            self.discounted_price = self.original_price * (Decimal(1) - discount_percentage)
            self.discount_amount = self.original_price - self.discounted_price
            self.total_cost = self.discounted_price
        else:
           
            base_price = Decimal(7) if self.weight <= 4 else self.weight * Decimal(2)
            self.original_price = base_price
            self.discount_amount = base_price * discount_percentage
            self.discounted_price = base_price - self.discount_amount
            self.total_cost = self.discounted_price
 
        self.discounted_price = self.discounted_price or Decimal(0)
        self.discount_amount = self.discount_amount or Decimal(0)
        self.total_cost = self.total_cost or Decimal(0)

    def save(self, *args, **kwargs):
        self.calculate_discounted_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Package: {self.name} - {self.weight} lbs - Dynamic Pricing: {self.dynamic_pricing_enabled}"

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
    created_at = models.DateTimeField(auto_now_add=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Label for {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
 
        if not Batch.objects.filter(new_label=self).exists():
            Batch.objects.create(
                new_label=self,
                batch_id=f"BATCH-{self.id}"
            )
class Batch(models.Model):
    new_label = models.ForeignKey(NewLabel, on_delete=models.CASCADE)  
    batch_id = models.CharField(max_length=100, unique=True)
    ship_from_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ship_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.new_label:
            self.ship_from_name = self.new_label.name
            self.type = self.new_label.delivery_type
            self.weight = self.new_label.package.weight  
            self.cost = self.new_label.package.total_cost   
            self.ship_date = self.new_label.ship_from.created_at   

        super().save(*args, **kwargs)
 
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
    created_by = models.ForeignKey(User, related_name="created_order", on_delete=models.CASCADE, null=True)

    

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
    