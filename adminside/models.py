from django.db import models
from django.contrib.auth.models import  BaseUserManager
from django.db import models
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from contact_form.models import NewLabel 
from django.conf import settings 


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
    available_for_withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    def __str__(self):
        return self.username
    @property
    def verified_status(self):       
        return "Yes" if self.is_active and self.is_2fa_enabled else "No"

    def generate_referral_code(self):
        while True:
            code = get_random_string(length=10)
            if not CustomUser.objects.filter(referral_code=code).exists():
                return code

    @staticmethod
    def calculate_commission(referrer, amount):
        commission = amount * 0.10
        referrer.available_for_withdraw += commission
        referrer.save()
        return commission

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super(CustomUser, self).save(*args, **kwargs)
  

class AdminUser(models.Model):
    email_address = models.EmailField(unique=True)
    
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
    color_CHOICES = [
         ('select', 'Select'),
        ('Red', 'Red'),
        ('Yellow', 'Yellow'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        
    ]
    message = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  
    is_read = models.BooleanField(default=False)  
    is_global = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_notifications" , null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100, choices=color_CHOICES, default='select')
