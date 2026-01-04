from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = (
        ('AD', 'Admin'),
        ('HP', 'Helper'),
        ('MC', 'Mechanic'),
        ('AP', 'Air Pressure Specialist'),
        ('SC', 'Seat Cover Specialist'),
        ('WA', 'Washer'),
        ('DO', 'Data Entry Operator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    profile_picture = models.URLField(
        max_length=500,
        blank=True,
        default="https://ik.imagekit.io/i8rqohdkt/profiles/default.png"
    )

    joining_date = models.DateField(null=True, blank=True)
    is_star_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            role='MC'  # default role, can be changed later
        )



class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return self.name

class Billing(models.Model):
    PAYMENT_STATUS = (
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
        ('CREDIT', 'Credit'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=200)

    attended_staff = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills'
    )
    discount_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
)


    labor_description = models.TextField(blank=True)
    labor_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.discount_amount is None:
            self.discount_amount = 0

        # ensure non-negative
        if self.discount_amount < 0:
            self.discount_amount = 0

        self.due_amount = self.total_amount - self.paid_amount

        if self.due_amount <= 0:
            self.payment_status = 'PAID'
        elif self.paid_amount == 0:
            self.payment_status = 'CREDIT'
        else:
            self.payment_status = 'PARTIAL'

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Bill {self.id} - {self.customer_name}"




class BillItem(models.Model):
    bill = models.ForeignKey(Billing, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill {self.id}"
    


class Payment(models.Model):
    bill = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(
        max_length=20,
        choices=(
            ('CASH', 'Cash'),
            ('UPI', 'UPI'),
            ('CARD', 'Card'),
            ('BANK', 'Bank Transfer'),
        )
    )
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.amount} for Bill {self.bill.id}"


class Dealer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    gst_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=100, blank=True)
    invoice_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(
        max_length=10,
        choices=(
            ('PAID', 'Paid'),
            ('CREDIT', 'Credit'),
        ),
        default='PAID'
    )
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def pending_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"Purchase #{self.id} - {self.dealer.name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.purchase_price
    def __str__(self):
        return f"PurchaseItem {self.id} for Purchase {self.purchase.id}"


from django.db import models
from decimal import Decimal

class StaffSalary(models.Model):
    staff = models.OneToOneField(Profile, on_delete=models.CASCADE)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)

    per_day_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Auto calculated"
    )

    def save(self, *args, **kwargs):
        if self.monthly_salary:
            # Standardized 30 days for stability
            self.per_day_salary = (
                Decimal(self.monthly_salary) / Decimal(30)
            ).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff} - {self.monthly_salary}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('H', 'Half Day'),
        ('L', 'Leave'),
    )

    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    remark = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('staff', 'date')

    def __str__(self):
        return f"{self.staff.user.username} - {self.date}"

class StaffAdvance(models.Model):
    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.staff.user.username} - ₹{self.amount}"

import calendar

class SalaryPayment(models.Model):
    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)
    month = models.DateField(help_text="Use first day of month")
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    advance_deducted = models.DecimalField(max_digits=10, decimal_places=2)
    net_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.user.username} - {self.month}"
    
    def month_name(self):
        return calendar.month_name[self.month]


from django.db import models

class StaffPayment(models.Model):
    PAYMENT_MODES = (
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Bank', 'Bank Transfer'),
    )

    staff = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='salary_payments'
    )

    year = models.IntegerField()
    month = models.IntegerField()  # 1–12

    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    advances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODES
    )

    remark = models.CharField(
        max_length=255,
        blank=True
    )

    paid_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('staff', 'year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.staff.user.username} - {self.month}/{self.year}"


from django.db import models
from django.utils import timezone

class PendingPayment(models.Model):
    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("CARD", "Card"),
    )

    bill = models.ForeignKey(
        "Billing",
        on_delete=models.CASCADE,
        related_name="pending_payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default="CASH"
    )

    paid_on = models.DateTimeField(default=timezone.now)

    recorded_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Bill #{self.bill.id} - ₹{self.amount}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Salary', 'Salary'),
        ('Electricity', 'Electricity Bill'),
        ('Transport', 'Transport / Fuel'),
        ('Tea', 'Tea / Snacks'),
        ('Maintenance', 'Repairs & Maintenance'),
        ('Other', 'Other'),
    ]

    PAYMENT_MODES = (
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('BANK', 'Bank Transfer'),
    )
    
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    
    # New additions for better tracking
    payment_mode = models.CharField(
        max_length=10, 
        choices=PAYMENT_MODES, 
        default='CASH'
    )
    
    recorded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    receipt_image = models.ImageField(upload_to='expenses/', blank=True, null=True)

    class Meta:
        ordering = ['-date']  # Shows latest expenses first

    def __str__(self):
        return f"{self.category} - ₹{self.amount} ({self.date})"