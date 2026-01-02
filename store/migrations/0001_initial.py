# Generated manually – clean MySQL-safe initial migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        # ======================
        # CORE MASTER TABLES
        # ======================

        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),

        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, null=True)),
                ('phone', models.CharField(max_length=15, blank=True)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),

        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=15, blank=True)),
                ('address', models.TextField(blank=True)),
                ('gst_number', models.CharField(max_length=50, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),

        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(
                    max_length=2,
                    choices=[
                        ('AD', 'Admin'),
                        ('HP', 'Helper'),
                        ('MC', 'Mechanic'),
                        ('AP', 'Air Pressure Specialist'),
                        ('SC', 'Seat Cover Specialist'),
                        ('WA', 'Washer'),
                        ('DO', 'Data Entry Operator'),
                    ],
                )),
                ('profile_picture', models.URLField(
                    max_length=500,
                    blank=True,
                    default='https://ik.imagekit.io/i8rqohdkt/profiles/default.png'
                )),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('is_star_staff', models.BooleanField(default=False)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),

        # ======================
        # PRODUCTS & PURCHASE
        # ======================

        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.IntegerField(default=0, blank=True, null=True)),
                ('category', models.ForeignKey(
                    to='store.category',
                    on_delete=django.db.models.deletion.CASCADE,
                    blank=True,
                    null=True
                )),
            ],
        ),

        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(max_length=100, blank=True)),
                ('invoice_date', models.DateField()),
                ('total_amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('payment_type', models.CharField(
                    max_length=10,
                    choices=[('PAID', 'Paid'), ('CREDIT', 'Credit')],
                    default='PAID'
                )),
                ('paid_amount', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dealer', models.ForeignKey(
                    to='store.dealer',
                    on_delete=django.db.models.deletion.PROTECT
                )),
            ],
        ),

        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('product', models.ForeignKey(
                    to='store.product',
                    on_delete=django.db.models.deletion.PROTECT
                )),
                ('purchase', models.ForeignKey(
                    to='store.purchase',
                    on_delete=django.db.models.deletion.CASCADE
                )),
            ],
        ),

        # ======================
        # BILLING
        # ======================

        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=200)),
                ('discount_amount', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('labor_description', models.TextField(blank=True)),
                ('labor_amount', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('total_amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('paid_amount', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('due_amount', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('payment_status', models.CharField(
                    max_length=10,
                    choices=[('PAID', 'Paid'), ('PARTIAL', 'Partial'), ('CREDIT', 'Credit')]
                )),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(
                    to='store.customer',
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True,
                    null=True
                )),
                ('attended_staff', models.ForeignKey(
                    to='store.profile',
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True,
                    null=True,
                    related_name='bills'
                )),
            ],
        ),

        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('bill', models.ForeignKey(
                    to='store.billing',
                    on_delete=django.db.models.deletion.CASCADE
                )),
                ('product', models.ForeignKey(
                    to='store.product',
                    on_delete=django.db.models.deletion.CASCADE
                )),
            ],
        ),

        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('mode', models.CharField(
                    max_length=20,
                    choices=[
                        ('CASH', 'Cash'),
                        ('UPI', 'UPI'),
                        ('CARD', 'Card'),
                        ('BANK', 'Bank Transfer'),
                    ]
                )),
                ('note', models.TextField(blank=True)),
                ('bill', models.ForeignKey(
                    to='store.billing',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payments'
                )),
            ],
        ),

        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('payment_method', models.CharField(
                    max_length=10,
                    choices=[('CASH', 'Cash'), ('UPI', 'UPI'), ('CARD', 'Card')],
                    default='CASH'
                )),
                ('paid_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bill', models.ForeignKey(
                    to='store.billing',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pending_payments'
                )),
                ('recorded_by', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True,
                    null=True
                )),
            ],
        ),
    ]
