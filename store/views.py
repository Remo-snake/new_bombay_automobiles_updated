from urllib import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta


from .models import Customer, PendingPayment, Product, Billing, BillItem




from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import Customer, Product, Billing, BillItem


from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta


from .models import Customer, Product, Billing, BillItem


from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDate
import json

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import (
    Customer, Product, Billing, BillItem, Payment
)
from django.contrib.auth.decorators import login_required


# @login_required
# def dashboard(request):
#     today = timezone.now().date()
#     last_7_days = today - timedelta(days=7)

#     # =========================
#     # BASIC COUNTS
#     # =========================
#     total_customers = Customer.objects.count()
#     total_products = Product.objects.count()
#     total_stock = Product.objects.aggregate(
#         total=Sum('stock')
#     )['total'] or 0

#     total_sales = Billing.objects.aggregate(
#         total=Sum('total_amount')
#     )['total'] or 0

#     recent_bills = Billing.objects.select_related(
#         'customer'
#     ).order_by('-date')[:5]

#     # =========================
#     # SALES LAST 7 DAYS
#     # =========================
#     sales_last_7_days = (
#         Billing.objects
#         .filter(date__date__gte=last_7_days)
#         .values('date__date')
#         .annotate(total=Sum('total_amount'))
#         .order_by('date__date')
#     )

#     sales_labels = [
#         row['date__date'].strftime('%d %b')
#         for row in sales_last_7_days
#     ]
#     sales_values = [
#         float(row['total']) for row in sales_last_7_days
#     ]


#     # =========================
#     # TOP PRODUCTS
#     # =========================
#     top_products = (
#         BillItem.objects
#         .values('product__name')
#         .annotate(quantity=Sum('quantity'))
#         .order_by('-quantity')[:5]
#     )

#     # =========================
#     # PAYMENT MODE PIE (TODAY)
#     # =========================
#     payment_qs = (
#         Payment.objects
#         .filter(payment_date__date=today)
#         .values('mode')
#         .annotate(total=Sum('amount'))
#     )

#     payment_labels = []
#     payment_values = []

#     for row in payment_qs:
#         payment_labels.append(row['mode'])
#         payment_values.append(float(row['total']))

#     # =========================
#     # AVG DAILY SALES (SLIDER)
#     # =========================
#     avg_daily_sales = (
#         Billing.objects
#         .filter(date__date__gte=last_7_days)
#         .aggregate(avg=Sum('total_amount'))['avg'] or 0
#     )

#     avg_daily_sales = float(avg_daily_sales) / 7 if avg_daily_sales else 0

#     context = {
#         'total_customers': total_customers,
#         'total_products': total_products,
#         'total_stock': total_stock,
#         'total_sales': total_sales,
#         'recent_bills': recent_bills,

#         # charts
#         'sales_labels': sales_labels,
#         'sales_values': sales_values,
#         'payment_labels': payment_labels,
#         'payment_values': payment_values,
#         'avg_daily_sales': round(avg_daily_sales, 2),
#         'top_products': list(top_products),
#     }

#     return render(request, 'store/dashboard.html', context)


@login_required
def dashboard(request):
    return render(request, 'store/ticktak.html')

# Customer View


from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.contrib import messages
@login_required
def customer_list(request):
        customers = Customer.objects.all().order_by('-created_at')
        return render(request, 'store/customer/list.html', {'customers': customers})
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def customer_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email') or None
        address = request.POST.get('address')

        if not name or not phone or not address:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return redirect('customer_create')

        Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        messages.success(
            request,
            "Customer added successfully ✅"
        )
        return redirect('customer_list')

    return render(request, 'store/customer/form.html')
@login_required
def customer_update(request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        if request.method == 'POST':
                customer.name = request.POST['name']
                customer.phone = request.POST['phone']
                customer.email = request.POST['email']
                customer.address = request.POST['address']
                customer.save()
                messages.success(request, 'Customer updated successfully')
                return redirect('customer_list')
        return render(request, 'store/customer/form.html', {'customer': customer})
@login_required
def customer_delete(request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        messages.success(request, 'Customer deleted')
        return redirect('customer_list')




# Category View


from .models import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category/list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, "Category name is required.")
            return redirect('category_create')

        Category.objects.create(
            name=name,
            description=description
        )

        messages.success(
            request,
            "Category created successfully ✅"
        )
        return redirect('category_list')

    return render(request, 'store/category/form.html')


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.description = request.POST['description']
        category.save()
        messages.success(request, 'Category updated successfully')
        return redirect('category_list')
    return render(request, 'store/category/form.html', {'category': category})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted')
    return redirect('category_list')



# Product View


from .models import Product, Category

@login_required
def product_list(request):
    products = Product.objects.select_related('category')
    return render(request, 'store/product/list.html', {'products': products})

@login_required
def product_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        if not name:
            messages.error(request, "Product name is required.")
            return redirect('product_create')

        Product.objects.create(
            name=name,
            category_id=category or None,
            price=price if price else 0,
            stock=stock if stock else 0
        )

        messages.success(
            request,
            "Product added successfully ✅"
        )
        return redirect('product_list')

    return render(request, 'store/product/form.html', {
        'categories': categories
    })


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.price = request.POST['price']
        product.stock = request.POST.get('stock',None)
        product.save()
        messages.success(request, 'Product updated')
        return redirect('product_list')
    return render(request, 'store/product/form.html', {
        'product': product,
        'categories': categories
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect('product_list')



# Billing View

from .models import Billing, Customer
from django.views.decorators.clickjacking import xframe_options_exempt

@login_required
@xframe_options_exempt
def billing_list(request):
    bills = Billing.objects.select_related('customer').order_by('-date')
    return render(request, 'store/billing/list.html', {'bills': bills})
@login_required
def billing_print(request, pk):
    bill = Billing.objects.get(pk=pk)
    items = BillItem.objects.filter(bill=bill)

    # Calculate row totals
    for item in items:
        item.row_total = item.quantity * item.price

    return render(request, 'store/billing/print.html', {
        'bill': bill,
        'items': items
    })



from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .models import Billing, BillItem, Product, Customer




from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .models import Billing, BillItem, Product, Customer

import json
from django.core.serializers.json import DjangoJSONEncoder

import json
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Billing, BillItem, Product, Customer


from .models import Billing, BillItem, Product, Customer, Profile
import json
from django.db import transaction
from django.contrib import messages
@login_required
def billing_create(request):
    products = Product.objects.filter(stock__gt=0)
    customers = Customer.objects.all()
    staff_list = Profile.objects.exclude(role='AD')

    products_data = [
        {'id': p.id, 'name': p.name, 'price': float(p.price)}
        for p in products
    ]

    if request.method == 'POST':
        try:
            with transaction.atomic():
                customer_name = request.POST.get('customer_name')
                customer_id = request.POST.get('customer') or None
                staff_id = request.POST.get('attended_staff') or None

                payment_type = request.POST.get('payment_type')
                paid_amount = float(request.POST.get('paid_amount') or 0)
                labor_amount = float(request.POST.get('labor_amount') or 0)
                discount_amount = float(request.POST.get('discount_amount') or 0)

                bill = Billing.objects.create(
                    customer=customer_id,
                    customer_name=customer_name,
                    attended_staff_id=staff_id,
                    labor_amount=labor_amount,
                    discount_amount=discount_amount,
                    total_amount=0,
                    paid_amount=paid_amount
                )

                total = labor_amount

                for pid, qty, price in zip(
                    request.POST.getlist('product[]'),
                    request.POST.getlist('quantity[]'),
                    request.POST.getlist('price[]')
                ):
                    if not pid:
                        continue

                    product = Product.objects.get(id=int(pid))
                    qty = int(qty)
                    price = float(price)

                    # if product.stock < qty:
                    #     messages.error(
                    #         request,
                    #         f"Insufficient stock for {product.name}"
                    #     )
                    #     raise Exception("Stock error")

                    BillItem.objects.create(
                        bill=bill,
                        product=product,
                        quantity=qty,
                        price=price
                    )

                    product.stock -= qty
                    product.save()

                    total += qty * price

                total -= discount_amount
                bill.total_amount = max(total, 0)

                if payment_type == 'PAID':
                    bill.paid_amount = bill.total_amount

                bill.save()

                messages.success(
                    request,
                    f"Bill #{bill.id} created successfully ✅"
                )

                return redirect('billing_print', bill.id)

        except Exception:
            messages.error(
                request,
                "Billing failed. Please check stock and try again."
            )
            return redirect('billing_create')

    return render(
        request,
        'store/billing/create.html',
        {
            'products_json': json.dumps(products_data),
            'customers': customers,
            'staff_list': staff_list
        }
    )


    return render(
        request,
        'store/billing/create.html',
        {
            'products_json': json.dumps(products_data),
            'customers': customers,
            'staff_list': staff_list
        }
    )


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from store.models import Dealer, Product, Purchase, PurchaseItem
import json
@login_required
def purchase_create(request):
    dealers = Dealer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        dealer_id = request.POST.get('dealer')

        if not dealer_id:
            messages.error(request, "Dealer selection is required.")
            return redirect('purchase_create')

        dealer = Dealer.objects.get(id=dealer_id)

        purchase = Purchase.objects.create(
            dealer=dealer,
            invoice_number=request.POST.get('invoice_number'),
            invoice_date=request.POST.get('invoice_date'),
            payment_type=request.POST.get('payment_type'),
            paid_amount=float(request.POST.get('paid_amount') or 0),
            total_amount=0
        )

        total = 0

        for pid, qty, price in zip(
            request.POST.getlist('product[]'),
            request.POST.getlist('quantity[]'),
            request.POST.getlist('price[]')
        ):
            if not pid:
                continue

            product = Product.objects.get(id=int(pid))
            qty = int(qty)
            price = float(price)

            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=qty,
                purchase_price=price
            )

            product.stock += qty
            product.save()

            total += qty * price

        purchase.total_amount = total
        purchase.save()

        messages.success(
            request,
            "Purchase entry saved successfully ✅"
        )
        return redirect('purchase_list')

    return render(request, 'store/purchase/create.html', {
        'dealers': dealers,
        'products_json': json.dumps(
            list(products.values('id', 'name'))
        )
    })

@login_required
def purchase_list(request):
    purchases = Purchase.objects.select_related('dealer').order_by('-created_at')
    return render(request, 'store/purchase/list.html', {
        'purchases': purchases
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from store.models import Profile, Attendance


# store/views/attendance.py
@login_required
def attendance_mark(request):
    staff_list = Profile.objects.exclude(role='AD')  # exclude admin if needed
    selected_date = request.GET.get('date') or str(date.today())

    if request.method == 'POST':
        selected_date = request.POST.get('date')

        for staff in staff_list:
            status = request.POST.get(f'status_{staff.id}')
            in_time = request.POST.get(f'in_{staff.id}') or None
            out_time = request.POST.get(f'out_{staff.id}') or None
            remark = request.POST.get(f'remark_{staff.id}', '')

            attendance, created = Attendance.objects.get_or_create(
                staff=staff,
                date=selected_date
            )

            attendance.status = status
            attendance.in_time = in_time
            attendance.out_time = out_time
            attendance.remark = remark
            attendance.save()

        messages.success(request, 'Attendance saved successfully')
        return redirect(f'/attendance/?date={selected_date}')

    attendance_qs = Attendance.objects.filter(date=selected_date)
    attendance_lookup = {a.staff_id: a for a in attendance_qs}

    for staff in staff_list:
        staff.attendance = attendance_lookup.get(staff.id)
    
    context = {
    'staff_list': staff_list,
    'selected_date': selected_date
}
    return render(request, 'store/attendance/mark.html', context)


from calendar import monthrange
from django.shortcuts import render
from datetime import date

from .models import Profile, Attendance

@login_required
def staff_monthly_attendance(request):
    staff_list = Profile.objects.exclude(role='AD')

    staff_id = request.GET.get('staff')
    month_str = request.GET.get('month')

    attendance_list = []
    summary = {}

    if staff_id and month_str:
        year, mon = map(int, month_str.split('-'))
        staff = Profile.objects.get(id=staff_id)

        attendance_list = Attendance.objects.filter(
            staff=staff,
            date__year=year,
            date__month=mon
        ).order_by('date')

        present = attendance_list.filter(status='P').count()
        half = attendance_list.filter(status='H').count()
        absent = attendance_list.filter(status='A').count()

        total_days = present + half + absent

        summary = {
            'staff': staff,
            'present': present,
            'half': half,
            'absent': absent,
            'total': total_days,
            'year': year,
            'month': mon
        }

    return render(
        request,
        'store/attendance/staff_monthly.html',
        {
            'staff_list': staff_list,
            'attendance_list': attendance_list,
            'summary': summary,
            'selected_staff': staff_id,
            'selected_month': month_str
        }
    )


from datetime import date
from calendar import monthrange
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile, Attendance

from datetime import date
from calendar import monthrange

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Attendance, Profile

@login_required
def attendance_monthly_mark(request):
    # Only staff profiles (exclude Admin if needed)
    staff_list = Profile.objects.exclude(role='AD')

    staff_id = request.GET.get('staff') or request.POST.get('staff')
    month_str = request.GET.get('month') or request.POST.get('month')

    staff = None
    days = []

    # -----------------------------
    # LOAD ATTENDANCE (GET)
    # -----------------------------
    if staff_id and month_str:
        staff = get_object_or_404(Profile, id=staff_id)

        year, month = map(int, month_str.split('-'))
        total_days = monthrange(year, month)[1]

        for d in range(1, total_days + 1):
            current_date = date(year, month, d)

            attendance = Attendance.objects.filter(
                staff=staff,     # ✅ STRICT STAFF FILTER
                date=current_date
            ).first()

            days.append({
                'date': current_date,
                'status': attendance.status if attendance else 'P',
                'remark': attendance.remark if attendance else '',
                'in_time': attendance.in_time if attendance else '',
                'out_time': attendance.out_time if attendance else '',
            })

    # -----------------------------
    # SAVE ATTENDANCE (POST)
    # -----------------------------
    if request.method == 'POST' and staff_id and month_str:
        staff = get_object_or_404(Profile, id=staff_id)

        year, month = map(int, month_str.split('-'))
        total_days = monthrange(year, month)[1]

        for d in range(1, total_days + 1):
            current_date = date(year, month, d)

            status = request.POST.get(f'status_{d}', 'P')
            remark = request.POST.get(f'remark_{d}', '').strip()

            Attendance.objects.update_or_create(
                staff=staff,          # 🔒 INDIVIDUAL STAFF
                date=current_date,
                defaults={
                    'status': status,
                    'remark': remark
                }
            )

        messages.success(
            request,
            f"Attendance saved for {staff}"
        )

        return redirect(
            f"/attendance/mark/?staff={staff.id}&month={month_str}"
        )

    return render(
        request,
        'store/attendance/mark_monthly.html',
        {
            'staff_list': staff_list,
            'staff': staff,
            'month': month_str,
            'days': days,
            'selected_staff': str(staff_id) if staff_id else None,
        }
    )



from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Profile, StaffAdvance
@login_required
def staff_advance_create(request):
    staff_list = Profile.objects.exclude(role='AD')

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        amount = request.POST.get('amount')
        remark = request.POST.get('remark', '')

        if not staff_id or not amount:
            messages.error(request, 'Staff and amount are required')
            return redirect('staff_advance_create')

        StaffAdvance.objects.create(
            staff_id=staff_id,
            amount=amount,
            remark=remark
        )

        messages.success(request, 'Advance recorded successfully')
        return redirect('staff_advance_create')

    advances = StaffAdvance.objects.select_related('staff__user') \
                                   .order_by('-date')

    context = {
        'staff_list': staff_list,
        'advances': advances
    }
    return render(request, 'store/staff_advance/create.html', context)


from django.shortcuts import render
from datetime import date
from django.db.models import Sum
from store.models import (
    Profile, Attendance,
    StaffSalary, StaffAdvance
)
from decimal import Decimal
from calendar import monthrange
from django.db.models import Sum
from django.shortcuts import render
from datetime import date

from .models import (
    Profile, Attendance, StaffSalary, StaffAdvance
)
@login_required
def salary_calculate(request):
    staff_list = Profile.objects.exclude(role='AD')
    month_str = request.GET.get('month')

    result = None

    if month_str:
        staff_id = request.GET.get('staff')
        year, mon = map(int, month_str.split('-'))

        staff = Profile.objects.get(id=staff_id)

        salary_master = StaffSalary.objects.filter(staff=staff).first()
        if not salary_master:
            result = {'error': 'Salary not configured'}
        else:
            attendances = Attendance.objects.filter(
                staff=staff,
                date__year=year,
                date__month=mon
            )

            present = attendances.filter(status='P').count()
            half = attendances.filter(status='H').count()
            absent = attendances.filter(status='A').count()

            # ✅ Decimal-safe calculation
            total_days = (
                Decimal(present) +
                (Decimal(half) * Decimal('0.5'))
            )

            days_in_month = Decimal(monthrange(year, mon)[1])

            if salary_master.per_day_salary:
                per_day = salary_master.per_day_salary
            else:
                per_day = salary_master.monthly_salary / days_in_month

            gross = total_days * per_day

            advances = StaffAdvance.objects.filter(
                staff=staff,
                date__year=year,
                date__month=mon
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            net = gross - advances

            result = {
                'staff': staff,
                'gross': gross,
                'advances': advances,
                'net': net
            }

    return render(
        request,
        'store/salary/calculate.html',
        {
            'staff_list': staff_list,
            'result': result,
            'month': month_str
        }
    )

from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Sum
from calendar import monthrange

from .models import (
    Profile, Attendance, StaffSalary,
    StaffAdvance, StaffPayment
)

# ===========================
# AJAX SALARY PREVIEW
# ===========================

@login_required
def pay_salary_from_expectation(request, staff_id, year, mon):
    staff = Profile.objects.get(id=staff_id)

    if StaffPayment.objects.filter(
        staff=staff, year=year, month=mon
    ).exists():
        messages.warning(request, 'Salary already paid')
        return redirect('salary_expectation')

    salary_master = StaffSalary.objects.filter(staff=staff).first()
    if not salary_master:
        messages.error(request, 'Salary not configured')
        return redirect('salary_expectation')

    attendances = Attendance.objects.filter(
        staff=staff,
        date__year=year,
        date__month=mon
    )

    present = attendances.filter(status='P').count()
    half = attendances.filter(status='H').count()

    total_days = (
        Decimal(present) +
        (Decimal(half) * Decimal('0.5'))
    )

    if salary_master.per_day_salary:
        per_day = salary_master.per_day_salary
    else:
        per_day = salary_master.monthly_salary / Decimal('30')

    gross = total_days * per_day

    advances = StaffAdvance.objects.filter(
        staff=staff,
        date__year=year,
        date__month=mon
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    net = gross - advances

    StaffPayment.objects.create(
        staff=staff,
        year=year,
        month=mon,
        gross_salary=gross,
        advances=advances,
        net_pay=net,
        paid_amount=net,
        payment_mode='Cash',
        remark='Auto payment from expectation page'
    )

    messages.success(
        request,
        f'Salary paid for {staff.user.username}'
    )

    return redirect(f'/salary/expectation/?month={year}-{str(mon).zfill(2)}')
from calendar import monthrange
from decimal import Decimal
from datetime import date

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import (
    Profile,
    Attendance,
    StaffSalary,
    StaffPayment,
    StaffAdvance
)


from calendar import monthrange
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import (
    Profile, Attendance,
    StaffSalary, StaffPayment,
    StaffAdvance
)

from calendar import monthrange
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum

from .models import (
    Profile,
    Attendance,
    StaffSalary,
    StaffPayment,
    StaffAdvance
)


def get_per_day_salary(staff_salary, year, month):
    """
    Ensure per_day_salary is always available.
    Auto-calculate if missing and save it.
    """
    if staff_salary.per_day_salary:
        return staff_salary.per_day_salary

    days_in_month = monthrange(year, month)[1]
    per_day = staff_salary.monthly_salary / Decimal(days_in_month)

    staff_salary.per_day_salary = per_day
    staff_salary.save(update_fields=['per_day_salary'])

    return per_day

from calendar import monthrange
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum

from .models import (
    Profile,
    Attendance,
    StaffSalary,
    StaffPayment,
    StaffAdvance
)


def get_per_day_salary(salary, year, month):
    if salary.per_day_salary:
        return salary.per_day_salary

    days = monthrange(year, month)[1]
    per_day = salary.monthly_salary / Decimal(days)
    salary.per_day_salary = per_day
    salary.save(update_fields=['per_day_salary'])
    return per_day

from decimal import Decimal
from django.shortcuts import render
from django.db.models import Sum
from datetime import date

from .models import (
    Profile,
    Attendance,
    StaffSalary,
    StaffPayment,
    StaffAdvance
)

@login_required
def salary_expectation(request):
    staff_list = Profile.objects.exclude(role='AD')
    payments = StaffPayment.objects.select_related(
        'staff'
    ).all().order_by('-month')
    rows = []

    # 🔒 LOCAL CONSTANTS (NO ENV)
    MAX_LEAVES = 2
    STAR_INCENTIVE = Decimal('1000')

    selected_month = request.GET.get("month")
    if selected_month:
        year, month = map(int, selected_month.split("-"))
        today = date.today()

        if (year, month) > (today.year, today.month):
            messages.error(request, "Future months are not allowed.")
            return redirect("salary_expectation")


    if selected_month:
        year, month = map(int, selected_month.split('-'))

        for staff in staff_list:

            # Skip already-paid staff
            if StaffPayment.objects.filter(
                staff=staff,
                year=year,
                month=month
            ).exists():
                continue

            salary = StaffSalary.objects.filter(staff=staff).first()
            if not salary or not salary.per_day_salary:
                rows.append({
                    'staff': staff,
                    'error': 'Salary not configured'
                })
                continue

            per_day = salary.per_day_salary

            attendance_qs = Attendance.objects.filter(
                staff=staff,
                date__year=year,
                date__month=month
            )

            payable_days = Decimal('0')
            absent_days = Decimal('0')
            
            for a in attendance_qs:
                if a.status == 'P':
                    payable_days += Decimal('1')
                elif a.status == 'H':
                    payable_days += Decimal('0.5')
                    absent_days += Decimal('0.5')
                elif a.status in ['A', 'L']:
                    absent_days += 1

            # Deduct excess absents
            excess_absent = max(0, absent_days - MAX_LEAVES)
            payable_days -= Decimal(excess_absent)
            if payable_days < 0:
                payable_days = Decimal('0')

            # 💰 Salary calculation
            gross_salary = per_day * payable_days

            # ⭐ Star staff incentive
            incentive = Decimal('0')
            if staff.is_star_staff and absent_days <= MAX_LEAVES:
                incentive = STAR_INCENTIVE

            # ➖ Advances
            advances = StaffAdvance.objects.filter(
                staff=staff,
                date__year=year,
                date__month=month
            ).aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0')

            net_pay = gross_salary + incentive - advances
            if net_pay < 0:
                net_pay = Decimal('0')

            rows.append({
                'staff': staff,
                'per_day': per_day.quantize(Decimal('0.01')),
                'payable_days': payable_days,
                'gross': gross_salary.quantize(Decimal('0.01')),
                'advances': advances.quantize(Decimal('0.01')),
                'incentive': incentive.quantize(Decimal('0.01')),
                'net_pay': net_pay.quantize(Decimal('0.01')),
                'year': year,
                'month': month,
                'error': None       
            })

    return render(
        request,
        'store/salary/expectation_bulk.html',
        {
            'rows': rows,
            'month': selected_month,
            'payments': payments
        }
    )



# ===============================
# PAY SALARY
# ===============================
@login_required
def pay_salary(request, staff_id, year, month):
    staff = get_object_or_404(Profile, id=staff_id)

    if StaffPayment.objects.filter(
        staff=staff, year=year, month=month
    ).exists():
        messages.warning(request, "Salary already paid")
        return redirect('salary_expectation')

    salary = get_object_or_404(StaffSalary, staff=staff)

    attendance = Attendance.objects.filter(
        staff=staff,
        date__year=year,
        date__month=month
    )

    present = Decimal('0')
    leaves = 0

    for a in attendance:
        if a.status == 'P':
            present += Decimal('1')
        elif a.status == 'H':
            present += Decimal('0.5')
        elif a.status in ['A', 'L']:
            leaves += 1

    allowed_leaves = int(
        getattr(settings, 'NORMAL_STAFF_HOLIDAYS', 2)
    )

    extra_leaves = max(0, leaves - allowed_leaves)
    payable_days = present - Decimal(extra_leaves)
    if payable_days < 0:
        payable_days = Decimal('0')

    gross = salary.per_day_salary * Decimal(
        monthrange(year, month)[1]
    )
    net = salary.per_day_salary * payable_days

    advances = StaffAdvance.objects.filter(
        staff=staff,
        date__year=year,
        date__month=month
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    incentive = Decimal('0')
    if staff.is_star_staff and leaves <= allowed_leaves:
        incentive = Decimal(
            getattr(settings, 'STAR_STAFF_BONUS', 1000)
        )

    final_pay = net + incentive - advances

    StaffPayment.objects.create(
        staff=staff,
        year=year,
        month=month,
        gross_salary=gross,
        advances=advances,
        net_pay=final_pay,
        paid_amount=final_pay,
        payment_mode='Cash',
        remark='Auto salary payment'
    )

    messages.success(request, f"Salary paid to {staff}")
    return redirect(
        f"/salary/expectation/?month={year}-{month:02d}"
    )

from calendar import monthrange
from decimal import Decimal
from datetime import date

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    Profile,
    Attendance,
    StaffSalary,
    StaffPayment
)

@login_required
def salary_dashboard(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    total_days = monthrange(year, month)[1]
    allowed_leaves = settings.ALLOWED_LEAVES_PER_MONTH

    rows = []

    staff_list = Profile.objects.exclude(role="AD")

    for staff in staff_list:
        salary = StaffSalary.objects.filter(staff=staff).first()
        if not salary or not salary.per_day_salary:
            continue

        # Skip if already paid
        if StaffPayment.objects.filter(
            staff=staff, year=year, month=month
        ).exists():
            continue

        attendance_qs = Attendance.objects.filter(
            staff=staff,
            date__year=year,
            date__month=month
        )

        working_days = Decimal("0")
        absent_days = 0

        for a in attendance_qs:
            if a.status == "P":
                working_days += Decimal("1")
            elif a.status == "H":
                working_days += Decimal("0.5")
            elif a.status in ["A", "L"]:
                absent_days += 1

        extra_absent = max(0, absent_days - allowed_leaves)
        payable_days = working_days - Decimal(extra_absent)
        if payable_days < 0:
            payable_days = Decimal("0")

        gross_salary = salary.per_day_salary * Decimal(total_days)
        net_pay = salary.per_day_salary * payable_days

        rows.append({
            "staff": staff,
            "working_days": working_days,
            "gross_salary": gross_salary.quantize(Decimal("0.01")),
            "net_pay": net_pay.quantize(Decimal("0.01")),
            "year": year,
            "month": month,
        })

    return render(
        request,
        "store/salary/dashboard.html",
        {
            "rows": rows,
            "year": year,
            "month": month,
        }
    )

@login_required
def salary_history(request):
    payments = StaffPayment.objects.select_related(
        'staff'
    ).all()
    return render(
        request,
        'store/salary/history.html',
        {'payments': payments}
    )



from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Billing
@login_required
def sales_simulator_api(request):
    days = int(request.GET.get("days", 1))

    today = timezone.now().date()
    start_date = today - timedelta(days=days - 1)

    total_sales = (
        Billing.objects
        .filter(date__date__gte=start_date)
        .aggregate(total=Sum("total_amount"))
        ["total"] or 0
    )

    return JsonResponse({
        "days": days,
        "total_sales": float(total_sales)
    })


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


def staff_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Staff ID or Password")

    return render(request, "store/staff_login.html")


def staff_logout(request):
    logout(request)
    return redirect("staff_login")



from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import date

from .models import Billing, Purchase, Profile
from django.http import Http404
from datetime import datetime, date, time
from django.utils import timezone
from django.http import Http404
from django.db.models import Sum

@login_required
def audit_report(request):
    if request.user.profile.role != 'AD':
        raise Http404("Page not found")

    start = request.GET.get('start')
    end = request.GET.get('end')

    # ------------------------
    # PARSE DATES SAFELY
    # ------------------------
    if start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    else:
        today = timezone.localdate()
        start_date = today.replace(day=1)
        end_date = today

    # ------------------------
    # MAKE DATETIME RANGE (FULL DAY)
    # ------------------------
    start_dt = timezone.make_aware(
        datetime.combine(start_date, time.min)
    )

    end_dt = timezone.make_aware(
        datetime.combine(end_date, time.max)
    )

    # ------------------------
    # SALES (INCOME)
    # ------------------------
    billings = Billing.objects.filter(
        date__range=(start_dt, end_dt)
    )

    total_sales = billings.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # ------------------------
    # PURCHASES (EXPENSE)
    # ------------------------
    purchases = Purchase.objects.filter(
        invoice_date__range=(start_date, end_date)
    )

    total_purchases = purchases.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # ------------------------
    # STAFF CONTRIBUTION
    # ------------------------
    staff_sales = (
        Billing.objects
        .filter(
            attended_staff__isnull=False,
            date__range=(start_dt, end_dt)
        )
        .values(
            'attended_staff__user__username',
            'attended_staff__role'
        )
        .annotate(
            total=Sum('total_amount')
        )
        .order_by('-total')
    )

    # ------------------------
    # NET PROFIT
    # ------------------------
    net_profit = total_sales - total_purchases

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'net_profit': net_profit,
        'billings': billings,
        'purchases': purchases,
        'staff_sales': staff_sales,
    }

    return render(request, 'store/audit_report.html', context)



from openpyxl import Workbook
from django.http import HttpResponse
@login_required
def audit_export_excel(request):
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    if start_date:
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))

    if end_date:
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

    wb = Workbook()
    ws = wb.active
    ws.title = "Audit Report"

    ws.append(["Type", "Amount"])

    total_sales = Billing.objects.filter(
        date__date__range=[start, end]
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    total_purchases = Purchase.objects.filter(
        invoice_date__range=[start, end]
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    ws.append(["Total Sales", total_sales])
    ws.append(["Total Purchases", total_purchases])
    ws.append(["Net Profit", total_sales - total_purchases])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="audit_report.xlsx"'

    wb.save(response)
    return response


from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.db.models import Sum
from django.utils.timezone import make_aware

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime


from .models import Billing, Purchase, Profile
@login_required
def audit_export_pdf(request):
    # 🔐 Admin only
    if request.user.profile.role != 'AD':
        return HttpResponse("Unauthorized", status=403)

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    if start_date:
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))

    if end_date:
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

    bills = Billing.objects.all()
    purchases = Purchase.objects.all()

    if start_date and end_date:
        bills = bills.filter(date__range=(start_date, end_date))
        purchases = purchases.filter(created_at__range=(start_date, end_date))

    total_sales = bills.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_purchases = purchases.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    staff_data = (
        bills.values('attended_staff__user__username')
        .annotate(amount=Sum('total_amount'))
        .order_by('-amount')
    )

    net_balance = total_sales - total_purchases

    # ========================
    # PDF RESPONSE
    # ========================
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="audit_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ========================
    # TITLE
    # ========================
    elements.append(Paragraph("<b>NEW BOMBAY AUTOMOBILES</b>", styles['Title']))
    elements.append(Paragraph("Audit Report", styles['h2']))
    elements.append(Spacer(1, 12))

    if start and end:
        elements.append(Paragraph(f"Period: {start} to {end}", styles['Normal']))
        elements.append(Spacer(1, 12))

    # ========================
    # SUMMARY TABLE
    # ========================
    summary_data = [
        ["Metric", "Amount (₹)"],
        ["Total Sales", f"{total_sales:.2f}"],
        ["Total Purchases", f"{total_purchases:.2f}"],
        ["Net Balance", f"{net_balance:.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # ========================
    # STAFF CONTRIBUTION
    # ========================
    elements.append(Paragraph("<b>Staff Contribution</b>", styles['h3']))
    elements.append(Spacer(1, 10))

    staff_table_data = [["Staff", "Amount Generated (₹)"]]

    for row in staff_data:
        staff_table_data.append([
            row['attended_staff__user__username'] or "N/A",
            f"{row['amount']:.2f}"
        ])

    staff_table = Table(staff_table_data, colWidths=[250, 150])
    staff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    elements.append(staff_table)

    # ========================
    # BUILD PDF
    # ========================
    doc.build(elements)
    return response


from django.shortcuts import render

def maintenance(request):
    return render(request, "maintenance.html", status=503)


# store/views.py
from django.shortcuts import render

def custom_404(request, exception=None):
    return render(request, "errors/404.html", status=404)

def custom_403(request, exception=None):
    return render(request, "errors/403.html", status=403)

def custom_500(request):
    return render(request, "errors/500.html", status=500)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def credit_bills(request):
    bills = Billing.objects.filter(
        Q(payment_status="CREDIT") | Q(payment_status="PARTIAL")
    ).select_related("customer").order_by("-date")

    payment_history = PendingPayment.objects.select_related(
    "bill",
    "bill__customer"
).order_by("-paid_on")



    for b in bills:
        b.balance_amount = b.total_amount - b.paid_amount

    return render(request, "store/billing/credit_bills.html", {
        "bills": bills,
        "payment_history": payment_history
    })
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@login_required
def mark_bill_paid(request, bill_id):
    bill = get_object_or_404(Billing, id=bill_id)

    if request.method == "POST":
        pay_amount = Decimal(request.POST.get("pay_amount"))

        # Create payment record
        PendingPayment.objects.create(
            bill=bill,
            amount=pay_amount,
            recorded_by=request.user
        )

        # Update bill
        bill.paid_amount += pay_amount

        if bill.paid_amount >= bill.total_amount:
            bill.paid_amount = bill.total_amount
            bill.payment_status = "PAID"
        else:
            bill.payment_status = "PARTIAL"

        bill.save()

        messages.success(request, "Payment recorded successfully")

    return redirect("credit_bills")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, StaffSalary
@login_required
def staff_details(request):
    staff_list = Profile.objects.select_related("user").all()

    # attach salary dynamically
    for s in staff_list:
        s.salary = StaffSalary.objects.filter(staff=s).first()

    return render(request, "store/staff/details.html", {
        "staff_list": staff_list
    })

from decimal import Decimal

@login_required
def set_staff_salary(request, staff_id):
    staff = get_object_or_404(Profile, id=staff_id)

    if request.method == "POST":
        salary = request.POST.get("monthly_salary")

        if not salary:
            messages.error(request, "Salary is required")
            return redirect("staff_details")

        salary = Decimal(salary)
        per_day = salary / Decimal(30)

        StaffSalary.objects.update_or_create(
            staff=staff,
            defaults={
                "monthly_salary": salary,
                "per_day_salary": per_day
            }
        )

        messages.success(
            request,
            f"Salary configured for {staff.user.username}"
        )
        return redirect("staff_details")



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from store.models import Profile


from store.utils.imagekit import get_imagekit

# try:
#     from store.utils.imagekit import get_imagekit
#     imagekit = get_imagekit()
# except RuntimeError:
#     imagekit = None  # fallback for dev
# from store.utils.imagekit import get_imagekit

@login_required
def staff_update(request, pk):
    staff = get_object_or_404(Profile, pk=pk)
    try:
        imagekit = get_imagekit()
    except RuntimeError:
        imagekit = None  # fallback for local/dev

    if request.method == "POST":
        staff.role = request.POST.get("role")
        staff.joining_date = request.POST.get("joining_date") or None
        staff.is_star_staff = "is_star_staff" in request.POST

        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            if imagekit:
                response = imagekit.files.upload(
                    file=profile_picture.read(),
                    file_name=f"staff_{staff.user.username}.jpg",
                    folder="/profiles"
                )
                staff.profile_picture = response.url
            else:
                # Optional fallback: save locally
                staff.profile_picture.save(profile_picture.name, profile_picture)

        staff.save()
        messages.success(request, "Staff updated successfully")
        return redirect("staff_details")

    return render(request, "store/staff/edit.html", {
        "staff": staff,
        "roles": Profile.ROLE_CHOICES
    })




@login_required
def staff_delete(request, pk):
    staff = get_object_or_404(Profile, pk=pk)

    if request.method == "POST":
        staff.user.delete()  # deletes profile via cascade
        messages.success(request, "Staff deleted successfully")
        return redirect("staff_details")

    return render(request, "store/staff/delete_confirm.html", {
        "staff": staff
    })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from store.models import Profile
from store.utils.uploads import upload_profile_image


@login_required
def staff_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        joining_date = request.POST.get("joining_date")
        is_star_staff = "is_star_staff" in request.POST
        profile_picture = request.FILES.get("profile_picture")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("staff_create")

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Profile created by signal
        profile = user.profile
        profile.role = role
        profile.joining_date = joining_date or None
        profile.is_star_staff = is_star_staff

        # 🔥 ImageKit upload
        if profile_picture:
            image_url = upload_profile_image(
                profile_picture,
                username
            )
            profile.profile_picture = image_url

        profile.save()

        messages.success(request, "Staff created successfully")
        return redirect("staff_details")

    return render(request, "store/staff/create.html", {
        "roles": Profile.ROLE_CHOICES
    })



@login_required
def dealer_create(request):
    if request.method == "POST":    
        Dealer.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone", ""),
            address=request.POST.get("address", ""),
            gst_number=request.POST.get("gst_number", "")
        )
        messages.success(request, "Dealer added successfully")
        return redirect("dealer_list")

    return render(request, "store/dealer/form.html")

@login_required
def dealer_update(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)

    if request.method == "POST":
        dealer.name = request.POST.get("name")
        dealer.phone = request.POST.get("phone", "")
        dealer.address = request.POST.get("address", "")
        dealer.gst_number = request.POST.get("gst_number", "")
        dealer.save()

        messages.success(request, "Dealer updated successfully")
        return redirect("dealer_list")

    return render(request, "store/dealer/form.html", {
        "dealer": dealer
    })

from django.db.models import ProtectedError

@login_required
def dealer_delete(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)

    if request.method == "POST":
        try:
            dealer.delete()
            messages.success(request, "Dealer deleted successfully")
        except ProtectedError:
            messages.error(request, "Cannot delete dealer because there are purchases linked to it.")
        return redirect("dealer_list")

    return render(request, "store/dealer/delete.html", {
        "dealer": dealer
    })


@login_required
def dealer_list(request):
    dealers = Dealer.objects.order_by("-created_at")
    return render(request, "store/dealer/list.html", {
        "dealers": dealers
    })


