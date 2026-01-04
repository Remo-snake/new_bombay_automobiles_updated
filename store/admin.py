from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Profile,
    Customer,
    Category,
    Product,
    Billing,
    BillItem,
    Dealer,
    Purchase,
    PurchaseItem,SalaryPayment, StaffAdvance,  Attendance,StaffSalary
)

# -------------------------
# Profile Admin
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
    ordering = ('user',)


# -------------------------
# Customer Admin
# -------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# -------------------------
# Category Admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -------------------------
# Product Admin
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('price', 'stock')
    ordering = ('name',)


# -------------------------
# Bill Item Inline
# -------------------------
class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


# -------------------------
# Billing Admin
# -------------------------
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'date')
    list_filter = ('date','payment_status')
    search_fields = ('customer__name',)
    ordering = ('-date',)
    inlines = [BillItemInline]


# -------------------------
# BillItem Admin (optional)
# -------------------------
@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'product', 'quantity', 'price')
    search_fields = ('bill__id', 'product__name')

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'gst_number', 'created_at')
    search_fields = ('name', 'phone', 'gst_number')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('dealer', 'total_amount',)
    search_fields = ('dealer__name',)

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product', 'quantity',)
    search_fields = ('purchase__id', 'product__name')

# @admin.register(SalaryPayment)
# class SalaryPaymentAdmin(admin.ModelAdmin):
#     list_display = ('staff', )
#     search_fields = ('staff__name',)

@admin.register(StaffAdvance)
class StaffAdvanceAdmin(admin.ModelAdmin):
    list_display = ('id','staff',  'date')
    search_fields = ('staff__name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status')
    search_fields = ('staff__name',)
    list_filter = ('staff','date', 'status')
@admin.register(StaffSalary)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = ('id','staff')
    search_fields = ('staff__name',)


from .models import StaffPayment

@admin.register(StaffPayment)
class StaffPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'staff', 'month', 'year',
        'net_pay', 'paid_amount',
        'payment_mode', 'paid_on'
    )
    list_filter = ('year', 'month', 'payment_mode')

