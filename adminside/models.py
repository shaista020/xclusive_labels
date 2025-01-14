from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

from contact_form.models import NewLabel, Package, Address 

from django.conf import settings 



class Signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rememberme= models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Signin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rememberme= models.BooleanField(default=False)
    recaptcha=models.BooleanField(default=False)
    

    def __str__(self):
        return self.email

class Batch(models.Model):
    batch_id = models.CharField(max_length=100)
    ship_from_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    ship_date = models.DateField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.batch_id
    


class Cron(models.Model):
    label = models.CharField(max_length=100)
    register_at = models.DateField()

    def __str__(self):
        return self.label
class Type(models.Model):
    VALUE_CHOICES = [
        ('Priority', 'Priority'),
        ('Express', 'Express'),
        ('First Class', 'First Class'),
        ('Signature', 'Signature'),
    ]
    label = models.ForeignKey(NewLabel, on_delete=models.CASCADE, related_name='types')
    type_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    value = models.CharField(
        max_length=100,
        choices=VALUE_CHOICES,  
        default='Priority', 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_name} - {self.label.name}"


class Payment(models.Model):
    payment_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gateway = models.CharField(max_length=50)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    request_balance = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    request_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


class Refund(models.Model):
    email = models.EmailField()
    duration = models.CharField(max_length=50)
    requested_on = models.DateTimeField(auto_now_add=True)




class PaymentConfig(models.Model):
    stripe_key = models.CharField(max_length=255)
    stripe_secret = models.CharField(max_length=255)
    stripe_webhook_secret = models.CharField(max_length=255)
    coinbase_key = models.CharField(max_length=255)
    coinbase_webhook_secret = models.CharField(max_length=255)
    venmo_email = models.EmailField()
    cashapp_email = models.EmailField()
    zelle_email = models.EmailField()



class EmailConfig(models.Model):
    from_email = models.EmailField()
    from_name = models.CharField(max_length=255)
    smtp_host = models.CharField(max_length=255)
    smtp_port = models.IntegerField()
    smtp_user = models.EmailField()
    smtp_password = models.CharField(max_length=255)

class LabelAPIConfig(models.Model):
    api_key = models.CharField(max_length=255)
    host = models.CharField(max_length=255)


# class Ticket(models.Model):
#     title = models.CharField(max_length=255)
#     ticket_type = models.CharField(max_length=100)
#     data_id = models.CharField(max_length=100)
#     status = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

 
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, null=True)
    date_of_creation = models.DateField(auto_now_add=True, null=True)
    last_login_date = models.DateField(blank=True, null=True)
    is_super_admin = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='UTC') 
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def verified_status(self):
        # Set the `verified` status based on `is_active`
        return "Yes" if self.is_active else "No"

from django.conf import settings

class AdminUser(models.Model):
    email_address = models.EmailField(unique=True)
   
    # Proper reference to CustomUser
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return self.user.username

class Weight(models.Model):
    label = models.ForeignKey(NewLabel, on_delete=models.CASCADE, related_name='weights')
    from_weight = models.FloatField()
    to_weight = models.FloatField()
    user_cost = models.DecimalField(max_digits=10, decimal_places=2)
    reseller_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label.name




class Notification(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    send_by = models.ForeignKey(CustomUser, related_name='sent_notifications', on_delete=models.CASCADE)
    send_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE)
    is_seen = models.BooleanField()

    def __str__(self):
        return f'Notification from {self.send_by} to {self.send_to}'

class newLabel(models.Model):
    DELIVERY_CHOICES = [
        ('usps_priority', 'USPS Priority'),
    ]
    PACKAGE_CHOICES = [
        ('test', 'Test'), 
    ]
    SHIP_FROM_CHOICES = [
        ('no_saved_address', "Don't use saved Ship From Address"),
        ('address_1', "Test name, Street Address 1, City 1, 424424, NY"),
        ('address_2', "Bob Doe, 1431 Brushed Lane, Lawrenceville, 30045-5507, GA"),
    ]

    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    package = models.CharField(max_length=100, choices=PACKAGE_CHOICES)
    ship_from = models.CharField(max_length=100, choices=SHIP_FROM_CHOICES)
    weight = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    recipient_name = models.CharField(max_length=100)
    recipient_company = models.CharField(max_length=100, blank=True, null=True)
    recipient_address = models.CharField(max_length=200)
    recipient_city = models.CharField(max_length=50)
    recipient_zip_code = models.CharField(max_length=10)
    recipient_state = models.CharField(max_length=50)
    recipient_phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"Label for {self.recipient_name} - {self.delivery_type}"
