import os
import django
import random

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Auto_mobile.settings')
django.setup()

from store.models import Category, Product

def random_price():
    return random.randint(50, 5000)

data = {
    "Tyre": [
        "MRF", "CEAT", "Apollo", "JK", "RALCO", "NUMAX", "Remote", "Other"
    ],
    "Battery": [
        "Amron", "Excide", "Other"
    ],
    "Oil": [
        "Castrol", "Gulf", "Sarvo", "Miles", "Bajaj", "Motul",
        "Vorrac", "Amrron", "Petro", "Numax", "HP laal ghoda Oil"
    ],
    "Coolant": [
        "Castrol", "Bosch", "TVS", "Numax", "Cosmos"
    ],
    "Grease": [
        "Castrol", "Gulf", "SKF", "Miles", "Texpin",
        "SF Soni", "Mark", "Numax", "ABL", "Other"
    ],
    "Seat Cover": [
        "Bike", "Activa", "Tacter"
    ],
    "Halar Belt": [
        "A No. Belt", "B No. Belt", "C No. Belt", "Tacter Belt", "Other"
    ],
    "Washing": [
        "Bike", "Car"
    ],
}

# Standalone products (no category)
standalone_products = [
    "KeyChain",
    "Horn",
    "LED Item",
    "Two Wheeler Bike",
    "Bullet Item",
    "Three Wheeler Auto",
    "Four Wheeler Car",
    "Tata-S Item",
    "Tractor Item",
    "Nangar Item",
    "GCP Item",
    "Chaina Pichkari",
    "Pamchar Fiting",
    "Hawa"
]

def create_data():
    print("Creating categories & products...")

    for category_name, products in data.items():
        category, _ = Category.objects.get_or_create(
            name=category_name
        )

        for product_name in products:
            Product.objects.get_or_create(
                name=product_name,
                category=category,
                defaults={
                    "price": random_price(),
                    "stock": random.randint(5, 100)
                }
            )

    for product_name in standalone_products:
        Product.objects.get_or_create(
            name=product_name,
            category=None,
            defaults={
                "price": random_price(),
                "stock": random.randint(5, 100)
            }
        )

    print("✅ Products created successfully!")

if __name__ == "__main__":
    create_data()
