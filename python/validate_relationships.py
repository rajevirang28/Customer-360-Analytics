import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
PRODUCTS_FILE = RAW_DIR / "products.csv"
ORDERS_FILE = RAW_DIR / "orders.csv"

customers = pd.read_csv(CUSTOMERS_FILE)
products = pd.read_csv(PRODUCTS_FILE)
orders = pd.read_csv(ORDERS_FILE)

print("CUSTOMER 360 RELATIONSHIP VALIDATION")

valid_customer_ids = set(
    customers["customer_id"]
)

order_customer_ids = set(
    orders["customer_id"]
)

invalid_customer_ids = (
    order_customer_ids - valid_customer_ids
)

print("\nCustomer ID Validation")
print("-" * 30)

print(
    f"Customers in master data: "
    f"{len(valid_customer_ids)}"
)

print(
    f"Customers appearing in orders: "
    f"{len(order_customer_ids)}"
)

print(
    f"Invalid customer IDs in orders: "
    f"{len(invalid_customer_ids)}"
)

valid_product_ids = set(
    products["product_id"]
)

order_product_ids = set(
    orders["product_id"]
)

invalid_product_ids = (
    order_product_ids - valid_product_ids
)

print("\nProduct ID Validation")
print("-" * 30)

print(
    f"Products in master data: "
    f"{len(valid_product_ids)}"
)

print(
    f"Products appearing in orders: "
    f"{len(order_product_ids)}"
)

print(
    f"Invalid product IDs in orders: "
    f"{len(invalid_product_ids)}"
)

customers_with_orders = set(
    orders["customer_id"]
)

customers_without_orders = (
    valid_customer_ids - customers_with_orders
)

print("\nCustomer Purchase Coverage")
print("-" * 30)

print(
    f"Customers with orders: "
    f"{len(customers_with_orders)}"
)

print(
    f"Customers without orders: "
    f"{len(customers_without_orders)}"
)

duplicate_orders = (
    orders["order_id"].duplicated().sum()
)

print("\nOrder ID Validation")
print("-" * 30)

print(
    f"Duplicate order IDs: "
    f"{duplicate_orders}"
)

if (
    len(invalid_customer_ids) == 0
    and len(invalid_product_ids) == 0
    and duplicate_orders == 0
):
    print("STATUS: PASS")
    print("Customer and product relationships are valid.")
else:
    print("STATUS: FAIL")
    print("Relationship problems were detected.")