# Generated by Django 5.1.3 on 2024-12-25 06:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('timezone', models.CharField(choices=[('GMT-05:00', 'Eastern Time (US & Canada)'), ('GMT-06:00', 'Central Time (US & Canada)'), ('GMT+10:00', 'Guam'), ('GMT+10:00', 'Yakutsk'), ('GMT+09:00', 'Tokyo'), ('GMT+09:00', 'Seoul'), ('GMT+12:00', 'Auckland')], default='GMT-05:00', max_length=20)),
                ('two_fa_enabled', models.BooleanField(default=False, verbose_name='2FA Authentication')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('available_for_withdraw', models.DecimalField(decimal_places=2, max_digits=10)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipFromAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('company_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('apt_unit_suite', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StateShipmentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('shipments_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('select', 'Select'), ('credit_debit_card', 'Credit/Debit Card (instantly)'), ('crypto_currency', 'Crypto Currency (instantly)'), ('venmo', 'Venmo (2-3 hours)'), ('cashapp', 'CashApp (2-3 hours)'), ('zelle', 'Zelle (2-3 hours)')], default='Select', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company_reference', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('apt_unit_suite', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(max_length=255)),
                ('apt_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('ship_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact_form.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(max_length=255)),
                ('batch_number', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('select', 'Select'), ('in_queue', 'In Queue'), ('processing', 'Processing'), ('awaiting', 'Awaiting'), ('in_progress', 'In Progress'), ('delivered', 'Delivered'), ('complete', 'Complete'), ('cancelled', 'Cancelled'), ('none', 'None')], default='Select', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('new_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact_form.newlabel')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='newlabel',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact_form.package'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_number', models.CharField(max_length=255)),
                ('gateway', models.CharField(max_length=255)),
                ('previous_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('request_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('select', 'Select'), ('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('completed', 'Completed')], default='Select', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('url', models.URLField(null=True)),
                ('description', models.TextField(null=True)),
                ('store_type', models.CharField(choices=[('select', 'Select'), ('Retail', 'Retail'), ('Online', 'Online'), ('Wholesale', 'Wholesale'), ('Others', 'Others')], default='select', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], default='Open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
