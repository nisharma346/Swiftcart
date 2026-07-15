#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()

from swiftcart.models import Category, Product
from django.utils.text import slugify

# Create categories
categories_data = [
    {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
    {'name': 'Clothing', 'description': 'Apparel and fashion items'},
    {'name': 'Home & Garden', 'description': 'Home and garden products'},
    {'name': 'Sports', 'description': 'Sports equipment and accessories'},
    {'name': 'Books', 'description': 'Books and reading materials'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories[cat_data['name']] = cat
    if created:
        print(f"Created category: {cat.name}")

# Create products
products_data = [
    {
        'name': 'Wireless Headphones',
        'description': 'High-quality wireless headphones with noise cancellation',
        'price': 2499,
        'original_price': 3999,
        'stock': 50,
        'category': 'Electronics',
        'is_featured': True,
        'is_best_seller': True,
    },
    {
        'name': 'Smart Watch',
        'description': 'Advanced smartwatch with health monitoring',
        'price': 5999,
        'original_price': 8999,
        'stock': 30,
        'category': 'Electronics',
        'is_featured': True,
    },
    {
        'name': 'USB-C Cable',
        'description': 'Durable USB-C charging cable',
        'price': 299,
        'original_price': 499,
        'stock': 100,
        'category': 'Electronics',
        'is_best_seller': True,
    },
    {
        'name': 'Cotton T-Shirt',
        'description': 'Comfortable cotton t-shirt',
        'price': 499,
        'original_price': 799,
        'stock': 75,
        'category': 'Clothing',
    },
    {
        'name': 'Denim Jeans',
        'description': 'Classic denim jeans',
        'price': 1299,
        'original_price': 1999,
        'stock': 40,
        'category': 'Clothing',
        'is_featured': True,
    },
    {
        'name': 'Yoga Mat',
        'description': 'Non-slip yoga exercise mat',
        'price': 899,
        'original_price': 1299,
        'stock': 25,
        'category': 'Sports',
    },
    {
        'name': 'Dumbbells Set',
        'description': 'Adjustable dumbbells set (2-10kg)',
        'price': 3999,
        'original_price': 5999,
        'stock': 15,
        'category': 'Sports',
        'is_best_seller': True,
    },
    {
        'name': 'Coffee Maker',
        'description': 'Automatic coffee maker',
        'price': 2199,
        'original_price': 3499,
        'stock': 20,
        'category': 'Home & Garden',
    },
    {
        'name': 'LED Lamp',
        'description': 'Modern LED table lamp',
        'price': 799,
        'original_price': 1299,
        'stock': 35,
        'category': 'Home & Garden',
        'is_featured': True,
    },
    {
        'name': 'Python Programming Book',
        'description': 'Learn Python programming from scratch',
        'price': 399,
        'original_price': 699,
        'stock': 50,
        'category': 'Books',
    },
]

for prod_data in products_data:
    category = categories[prod_data['category']]
    prod, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'slug': slugify(prod_data['name']),
            'description': prod_data['description'],
            'price': prod_data['price'],
            'original_price': prod_data['original_price'],
            'stock': prod_data['stock'],
            'category': category,
            'is_featured': prod_data.get('is_featured', False),
            'is_best_seller': prod_data.get('is_best_seller', False),
            'rating': 4.5,
            'discount': 0,
        }
    )
    if created:
        print(f"Created product: {prod.name}")

print("\nAll products added successfully!")
