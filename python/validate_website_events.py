import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
EVENTS_FILE = RAW_DIR / "website_events.csv"

customers = pd.read_csv(CUSTOMERS_FILE)
events = pd.read_csv(EVENTS_FILE)

print("WEBSITE EVENT DATA QUALITY REPORT")

print("\nDataset Size")
print("-" * 30)

print(f"Rows: {events.shape[0]}")
print(f"Columns: {events.shape[1]}")

print("\nMissing Values")
print("-" * 30)

print(events.isnull().sum())

duplicate_events = events["event_id"].duplicated().sum()

print("\nDuplicate Event IDs:", duplicate_events)

valid_customer_ids = set(
    customers["customer_id"]
)

event_customer_ids = set(
    events["customer_id"]
)

invalid_customer_ids = (
    event_customer_ids - valid_customer_ids
)

print("\nCustomer ID Validation")
print("-" * 30)

print(
    f"Customers in master data: "
    f"{len(valid_customer_ids)}"
)

print(
    f"Customers in website events: "
    f"{len(event_customer_ids)}"
)

print(
    f"Invalid customer IDs: "
    f"{len(invalid_customer_ids)}"
)

print("\nEvent Types")
print("-" * 30)

print(events["event_type"].value_counts())

print("\nDevices")
print("-" * 30)

print(events["device"].value_counts())

if (
    events.isnull().sum().sum() == 0
    and duplicate_events == 0
    and len(invalid_customer_ids) == 0
):
    print("STATUS: PASS")
    print("Website event dataset passed validation.")
else:
    print("STATUS: REVIEW")
    print("Data quality issues were detected.")