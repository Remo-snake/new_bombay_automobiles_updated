import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Auto_mobile.settings')
django.setup()

from store.models import Billing, Customer, Product, BillItem,Profile
# from profiles.models import Profile
from django.utils.timezone import make_aware

START_DATE = datetime(2025, 11, 1)
END_DATE = datetime(2025, 11, 30)

STAFF_IDS = list(range(1, 7))      

products = list(Product.objects.all())

if not products:
    raise Exception("❌ No products found. Add products before running script.")

def random_staff():
    return Profile.objects.filter(id=random.choice(STAFF_IDS)).first()

# def random_customer():
#     CUSTOMER_IDS=random.randint(1, 7)
#     # cid = random.choice(CUSTOMER_IDS)
#     return Customer.objects.filter(id=CUSTOMER_IDS).first()

current_date = START_DATE

while current_date <= END_DATE:

    bills_today = random.randint(1, 3)

    for _ in range(bills_today):

        # Payment decision
        payment_roll = random.random()

        if payment_roll < 0.2:
            payment_type = "CREDIT"
        elif payment_roll < 0.8:
            payment_type = "PARTIAL"
        else:
            payment_type = "PAID"

        # Customer logic (IMPORTANT RULE)
        if payment_type in ["PARTIAL", "CREDIT"]:
            CUSTOMER_IDS=random.randint(21, 28)
            customer = Customer.objects.get(id=CUSTOMER_IDS)
            print("customer ",customer)
            customer_name = customer.name if customer else "Known Customer"
        else:
            customer = None
            customer_name = "Walking Customer"

        staff = random_staff()

        labor_amount = Decimal(random.randint(200, 2000))
        discount_amount = Decimal(random.choice([0, 50, 100, 150]))

        bill = Billing.objects.create(
            customer=customer,
            customer_name=customer_name,
            attended_staff=staff,
            labor_description="General service & repair",
            labor_amount=labor_amount,
            discount_amount=discount_amount,
            total_amount=Decimal('0'),
            paid_amount=Decimal('0'),
            date=make_aware(
                datetime(
                    current_date.year,
                    current_date.month,
                    current_date.day,
                    random.randint(9, 19),
                    random.randint(0, 59)
                )
            )
        )

        # Add products (1–5 items per bill)
        total_product_amount = Decimal('0')
        product_count = random.randint(1, 5)

        for product in random.sample(products, min(product_count, len(products))):
            qty = random.randint(1, 3)
            price = product.price

            BillItem.objects.create(
                bill=bill,
                product=product,
                quantity=qty,
                price=price
            )

            total_product_amount += price * qty

        # Final total
        bill.total_amount = total_product_amount + labor_amount - discount_amount
        if bill.total_amount < 0:
            bill.total_amount = Decimal('0')

        # Paid amount logic
        if payment_type == "CREDIT":
            bill.paid_amount = Decimal('0')

        elif payment_type == "PAID":
            bill.paid_amount = bill.total_amount

        else:  # PARTIAL
            bill.paid_amount = (
                bill.total_amount * Decimal(random.uniform(0.3, 0.7))
            ).quantize(Decimal('0.01'))

        bill.save()  # uses your save() logic for due & status

    current_date += timedelta(days=1)

print("✅ November 2025 billing + items created successfully.")
