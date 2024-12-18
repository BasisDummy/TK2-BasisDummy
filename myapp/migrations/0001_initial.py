# Generated by Django 5.1.3 on 2024-12-08 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Promo Code')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Discount Percentage')),
                ('min_transaction', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Minimum Transaction')),
                ('max_usage', models.PositiveIntegerField(verbose_name='Max Usage')),
                ('usage_quota', models.PositiveIntegerField(default=0, verbose_name='Usage Quota')),
                ('voucher_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Voucher Price')),
                ('expired_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=15)),
                ('url_photo', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('date', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='SubJobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='myapp.jobcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='myapp.subjobcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='myapp.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Pembelian')),
                ('is_used', models.BooleanField(default=False, verbose_name='Telah Digunakan')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_vouchers', to='myapp.discount', verbose_name='Diskon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='myapp.user', verbose_name='Pembeli')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=20)),
                ('npwp', models.CharField(max_length=20)),
                ('photo_url', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=50)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_categories', models.ManyToManyField(related_name='workers', to='myapp.subjobcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Transaction Time')),
                ('category', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Transaction Amount')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='myapp.user', verbose_name='User')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='myapp.worker', verbose_name='Worker')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AWAITING_PAYMENT', 'Menunggu Pembayaran'), ('SEARCHING_WORKER', 'Mencari Pekerja Terdekat'), ('WORKER_FOUND', 'Mendapatkan Pekerja'), ('WAITING_WORKER', 'Menunggu Pekerja Tiba'), ('ARRIVE_WORKER', 'Pekerja Tiba'), ('IN_PROGRESS', 'Dikerjakan'), ('COMPLETED', 'Selesai'), ('CANCELED', 'Dibatalkan')], default='AWAITING_PAYMENT', max_length=20, verbose_name='Order Status')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='myapp.discount', verbose_name='Discount')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myapp.service', verbose_name='Service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myapp.user', verbose_name='Pemesan')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='myapp.worker', verbose_name='Worker')),
            ],
        ),
    ]
