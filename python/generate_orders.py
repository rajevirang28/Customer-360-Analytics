import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
PRODUCTS_FILE = RAW_DIR / "products.csv"
OUTPUT_FILE = RAW_DIR / "orders.csv"

NUM_ORDERS = 75_000

np.random.seed(42)

customers = pd.read_csv(CUSTOMERS_FILE)
products = pd.read_csv(PRODUCTS_FILE)

print("Customers loaded:", len(customers))
print("Products loaded:", len(products))

# Some customers purchase more frequently
customer_weights = np.random.exponential(
    scale=1.0,
    size=len(customers)
)

customer_weights = customer_weights / customer_weights.sum()

orders = []

customer_ids = customers["customer_id"].values
product_ids = products["product_id"].values

product_price_map = dict(
    zip(
        products["product_id"],
        products["unit_price"]
    )
)


for i in range(1, NUM_ORDERS + 1):

    # Select customer based on purchase probability
    customer_id = np.random.choice(
        customer_ids,
        p=customer_weights
    )

    # Select product
    product_id = np.random.choice(product_ids)

    # Get product price
    unit_price = product_price_map[product_id]

    # Quantity
    quantity = np.random.choice(
        [1, 2, 3, 4, 5],
        p=[0.45, 0.25, 0.15, 0.10, 0.05]
    )

    # Discount
    discount = np.random.choice(
        [0, 5, 10, 15, 20, 25],
        p=[0.20, 0.25, 0.25, 0.15, 0.10, 0.05]
    )

    # Order date
    order_date = pd.Timestamp(
        np.random.choice(
            pd.date_range(
                start="2024-01-01",
                end="2026-08-20"
            )
        )
    )

    # Payment method
    payment_method = np.random.choice(
        [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Cash on Delivery",
            "Wallet"
        ],
        p=[
            0.35,
            0.20,
            0.15,
            0.10,
            0.12,
            0.08
        ]
    )

    # Order status
    order_status = np.random.choice(
        [
            "Delivered",
            "Shipped",
            "Processing",
            "Cancelled",
            "Returned"
        ],
        p=[
            0.70,
            0.12,
            0.08,
            0.06,
            0.04
        ]
    )

    orders.append(
        {
            "order_id": f"O{i:06d}",
            "customer_id": customer_id,
            "order_date": order_date,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "discount": discount,
            "payment_method": payment_method,
            "order_status": order_status
        }
    )

df = pd.DataFrame(orders)

df["revenue"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount"] / 100)
)

df["revenue"] = df["revenue"].round(2)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 50)
print("ORDER DATASET GENERATED")
print("=" * 50)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate Order IDs:",
    df["order_id"].duplicated().sum()
)

print(
    "\nUnique Customers in Orders:",
    df["customer_id"].nunique()
)

print(
    "\nUnique Products in Orders:",
    df["product_id"].nunique()
)

print("\nOrder Status:")
print(df["order_status"].value_counts())

print("\nPayment Methods:")
print(df["payment_method"].value_counts())

print("\nRevenue Statistics:")
print(df["revenue"].describe())

print(
    "\nTotal Revenue:",
    round(df["revenue"].sum(), 2)
)

print(f"\nFile saved at:\n{OUTPUT_FILE}")