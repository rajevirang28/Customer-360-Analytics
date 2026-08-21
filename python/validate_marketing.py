import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
MARKETING_FILE = RAW_DIR / "marketing.csv"

customers = pd.read_csv(CUSTOMERS_FILE)
marketing = pd.read_csv(MARKETING_FILE)

print("MARKETING DATA QUALITY REPORT")

print("\nDataset Size")
print("-" * 30)

print(f"Rows: {marketing.shape[0]}")
print(f"Columns: {marketing.shape[1]}")

print("\nMissing Values")
print("-" * 30)

print(marketing.isnull().sum())

duplicate_ids = (
    marketing["campaign_id"].duplicated().sum()
)

print(
    "\nDuplicate Campaign IDs:",
    duplicate_ids
)

valid_customer_ids = set(
    customers["customer_id"]
)

marketing_customer_ids = set(
    marketing["customer_id"]
)

invalid_customer_ids = (
    marketing_customer_ids - valid_customer_ids
)

print("\nCustomer ID Validation")
print("-" * 30)

print(
    f"Customers in master data: "
    f"{len(valid_customer_ids)}"
)

print(
    f"Customers in marketing data: "
    f"{len(marketing_customer_ids)}"
)

print(
    f"Invalid customer IDs: "
    f"{len(invalid_customer_ids)}"
)

invalid_clicks = (
    (marketing["clicked"] == 1)
    & (marketing["opened"] == 0)
).sum()

invalid_conversions = (
    (marketing["converted"] == 1)
    & (marketing["clicked"] == 0)
).sum()

invalid_conversion_values = (
    (marketing["converted"] == 0)
    & (marketing["conversion_value"] > 0)
).sum()


print("\nBusiness Logic Validation")
print("-" * 30)

print(
    "Clicked without opening:",
    invalid_clicks
)

print(
    "Converted without clicking:",
    invalid_conversions
)

print(
    "Value without conversion:",
    invalid_conversion_values
)

if (
    marketing.isnull().sum().sum() == 0
    and duplicate_ids == 0
    and len(invalid_customer_ids) == 0
    and invalid_clicks == 0
    and invalid_conversions == 0
    and invalid_conversion_values == 0
):
    print("STATUS: PASS ")
    print("Marketing dataset passed validation.")
else:
    print("STATUS: REVIEW ")
    print("Data quality issues were detected.")