import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

fake = Faker("en_IN")

Faker.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "products.csv"

NUM_PRODUCTS = 500

product_catalog = {
    "Electronics": [
        "Headphones",
        "Earbuds",
        "Smartphone",
        "Smartwatch",
        "Power Bank",
        "Bluetooth Speaker",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Laptop"
    ],

    "Home": [
        "Bedsheet",
        "Curtains",
        "Lamp",
        "Chair",
        "Table",
        "Pillow",
        "Cookware",
        "Storage Box"
    ],

    "Fashion": [
        "T-Shirt",
        "Jeans",
        "Jacket",
        "Shoes",
        "Sneakers",
        "Saree",
        "Shirt",
        "Dress"
    ],

    "Beauty": [
        "Face Wash",
        "Moisturizer",
        "Shampoo",
        "Perfume",
        "Sunscreen",
        "Face Cream"
    ],

    "Grocery": [
        "Rice",
        "Wheat",
        "Tea",
        "Coffee",
        "Snacks",
        "Dry Fruits",
        "Cooking Oil"
    ]
}

brands = [
    "Boat",
    "Samsung",
    "Apple",
    "Nike",
    "Puma",
    "Adidas",
    "Philips",
    "Sony",
    "HP",
    "Dell",
    "Lenovo",
    "Lakme",
    "Maybelline",
    "Nestle",
    "Tata",
    "Fastrack"
]

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = np.random.choice(
        list(product_catalog.keys())
    )

    subcategory = np.random.choice(
        product_catalog[category]
    )

    brand = np.random.choice(brands)

    unit_cost = round(
        np.random.uniform(100, 15000),
        2
    )

    # Selling price is higher than cost
    unit_price = round(
        unit_cost * np.random.uniform(1.15, 1.80),
        2
    )

    product = {
        "product_id": f"P{i:04d}",
        "product_name": f"{brand} {subcategory}",
        "category": category,
        "subcategory": subcategory,
        "brand": brand,
        "unit_cost": unit_cost,
        "unit_price": unit_price
    }

    products.append(product)

df = pd.DataFrame(products)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# 9. Validation
print("\nProduct dataset generated successfully!")

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate Product IDs:",
    df["product_id"].duplicated().sum()
)

print("\nCategories:")
print(df["category"].value_counts())

print("\nProduct price statistics:")
print(df["unit_price"].describe())

print(f"\nFile saved at:")
print(OUTPUT_FILE)