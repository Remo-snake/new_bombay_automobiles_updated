from django import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from store.views import (
    attendance_mark,
    attendance_monthly_mark,
    audit_export_excel,
    audit_export_pdf,
    audit_report,
    credit_bills,
    dashboard,
    customer_list,
    customer_create,
    customer_update,
    customer_delete,
    category_list,
    category_create,
    category_update,
    category_delete,
    dealer_create,
    dealer_delete,
    dealer_list,
    dealer_update,
    maintenance,
    mark_bill_paid,
    pay_salary,
    pay_salary_from_expectation,
    product_list,
    product_create,
    product_update,
    product_delete,
    billing_list,
    billing_create,
    billing_print,
    purchase_create,
    purchase_list,
    salary_calculate,
    salary_dashboard,
    salary_expectation,
    salary_history,
    sales_simulator_api,
    set_staff_salary,
    staff_advance_create,
    staff_create,
    staff_delete,
    staff_details,
    staff_login,
    staff_logout,
    staff_monthly_attendance,
    staff_update,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    # Customer
    path("customers/", customer_list, name="customer_list"),
    path("customers/add/", customer_create, name="customer_create"),
    path("customers/<int:pk>/edit/", customer_update, name="customer_update"),
    path("customers/<int:pk>/delete/", customer_delete, name="customer_delete"),
    # Category
    path("categories/", category_list, name="category_list"),
    path("categories/add/", category_create, name="category_create"),
    path("categories/<int:pk>/edit/", category_update, name="category_update"),
    path("categories/<int:pk>/delete/", category_delete, name="category_delete"),
    # Product
    path("products/", product_list, name="product_list"),
    path("products/add/", product_create, name="product_create"),
    path("products/<int:pk>/edit/", product_update, name="product_update"),
    path("products/<int:pk>/delete/", product_delete, name="product_delete"),
    # Billing
    path("billing/", billing_list, name="billing_list"),
    path("billing/create/", billing_create, name="billing_create"),
    path("billing/<int:pk>/print/", billing_print, name="billing_print"),
    # purchase
    path("purchase/create/", purchase_create, name="purchase_create"),
    path("purchase/", purchase_list, name="purchase_list"),
    # Attendance
    path("attendance/", attendance_mark, name="attendance_mark"),
    path("attendance/staff/", staff_monthly_attendance, name="staff_monthly_attendance"
    ),
    path("attendance/mark/", attendance_monthly_mark, name="attendance_monthly_mark"),
    # Staff Advance
    path("staff/advance/", staff_advance_create, name="staff_advance_create"),
    # Salary Calculation
    path('salary/expectation/', salary_expectation, name='salary_expectation'),
    path('salary/pay/<int:staff_id>/<int:year>/<int:month>/', pay_salary, name='pay_salary'),
    path('salary/history/', salary_history, name='salary_history'),

    path("dashboard/sales-simulator/", sales_simulator_api, name="sales_simulator_api"),

    #login/logout can be added here
    path("login/", staff_login, name="staff_login"),
    path("logout/", staff_logout, name="staff_logout"),


    # Audit Reports
    path('audit/',audit_report,name='audit_report'),
    path('audit/export/excel/',audit_export_excel,name='audit_export_excel'),
    path('audit/export/pdf/',audit_export_pdf,name='audit_export_pdf'),

    # Maintenance
    path("maintenance/", maintenance, name="maintenance"),

    # Credit Bills 
    path("billing/pending/", credit_bills, name="credit_bills"),
    path("billing/mark-paid/<int:bill_id>/", mark_bill_paid, name="mark_bill_paid"),

    # store/urls.py
    path("staff/details/", staff_details, name="staff_details"),
    path("staff/salary/set/<int:staff_id>/", set_staff_salary, name="set_staff_salary"),
    path("staff/<int:pk>/edit/", staff_update, name="staff_update"),
    path("staff/<int:pk>/delete/", staff_delete, name="staff_delete"),
    path("staff/create/", staff_create, name="staff_create"),


    # Dealer
    path("dealers/", dealer_list, name="dealer_list"),
    path("dealers/add/", dealer_create, name="dealer_create"),
    path("dealers/<int:pk>/edit/", dealer_update, name="dealer_update"),
    path("dealers/<int:pk>/delete/", dealer_delete, name="dealer_delete"),


    ]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
handler403 = "django.views.defaults.permission_denied"
