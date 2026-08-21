import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
OUTPUT_FILE = RAW_DIR / "website_events.csv"

NUM_EVENTS = 250_000

np.random.seed(42)

customers = pd.read_csv(CUSTOMERS_FILE)

customer_ids = customers["customer_id"].values

print("Customers loaded:", len(customer_ids))

event_types = [
    "login",
    "search",
    "product_view",
    "add_to_cart",
    "remove_from_cart",
    "checkout",
    "purchase",
    "logout"
]

event_probabilities = [
    0.08,
    0.10,
    0.35,
    0.15,
    0.05,
    0.08,
    0.06,
    0.13
]

devices = [
    "Mobile",
    "Desktop",
    "Tablet"
]

device_probabilities = [
    0.60,
    0.32,
    0.08
]

traffic_sources = [
    "Google",
    "Facebook",
    "Instagram",
    "Direct",
    "Email",
    "Referral"
]

traffic_probabilities = [
    0.25,
    0.18,
    0.15,
    0.20,
    0.12,
    0.10
]

pages = [
    "/",
    "/home",
    "/search",
    "/products",
    "/product",
    "/cart",
    "/checkout",
    "/account"
]

print("Generating website events...")


event_ids = [
    f"E{i:07d}"
    for i in range(1, NUM_EVENTS + 1)
]


selected_customers = np.random.choice(
    customer_ids,
    size=NUM_EVENTS
)


selected_event_types = np.random.choice(
    event_types,
    size=NUM_EVENTS,
    p=event_probabilities
)


selected_devices = np.random.choice(
    devices,
    size=NUM_EVENTS,
    p=device_probabilities
)


selected_traffic = np.random.choice(
    traffic_sources,
    size=NUM_EVENTS,
    p=traffic_probabilities
)


selected_pages = np.random.choice(
    pages,
    size=NUM_EVENTS
)

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-08-20")

time_range_seconds = int(
    (end_date - start_date).total_seconds()
)

random_seconds = np.random.randint(
    0,
    time_range_seconds,
    size=NUM_EVENTS
)

event_times = (
    start_date
    + pd.to_timedelta(
        random_seconds,
        unit="s"
    )
)

session_numbers = np.random.randint(
    1,
    100001,
    size=NUM_EVENTS
)

session_ids = [
    f"S{x:06d}"
    for x in session_numbers
]

df = pd.DataFrame(
    {
        "event_id": event_ids,
        "customer_id": selected_customers,
        "event_time": event_times,
        "session_id": session_ids,
        "event_type": selected_event_types,
        "page": selected_pages,
        "device": selected_devices,
        "traffic_source": selected_traffic
    }
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 50)
print("WEBSITE EVENT DATASET GENERATED")
print("=" * 50)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate Event IDs:",
    df["event_id"].duplicated().sum()
)

print(
    "\nUnique Customers:",
    df["customer_id"].nunique()
)

print(
    "\nUnique Sessions:",
    df["session_id"].nunique()
)

print("\nEvent Types:")
print(df["event_type"].value_counts())

print("\nDevice Distribution:")
print(df["device"].value_counts())

print("\nTraffic Sources:")
print(df["traffic_source"].value_counts())

print(f"\nFile saved at:\n{OUTPUT_FILE}")