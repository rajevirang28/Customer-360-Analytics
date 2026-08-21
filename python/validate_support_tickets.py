import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
SUPPORT_FILE = RAW_DIR / "support_tickets.csv"

customers = pd.read_csv(CUSTOMERS_FILE)
support = pd.read_csv(SUPPORT_FILE)


print("=" * 60)
print("SUPPORT TICKET DATA QUALITY REPORT")
print("=" * 60)

print("\nDataset Size")
print("-" * 30)

print(f"Rows: {support.shape[0]}")
print(f"Columns: {support.shape[1]}")

print("\nMissing Values")
print("-" * 30)

print(support.isnull().sum())

duplicate_ids = (
    support["ticket_id"].duplicated().sum()
)

print(
    "\nDuplicate Ticket IDs:",
    duplicate_ids
)

valid_customer_ids = set(
    customers["customer_id"]
)

support_customer_ids = set(
    support["customer_id"]
)

invalid_customer_ids = (
    support_customer_ids - valid_customer_ids
)

print("\nCustomer ID Validation")
print("-" * 30)

print(
    f"Customers in master data: "
    f"{len(valid_customer_ids)}"
)

print(
    f"Customers in support data: "
    f"{len(support_customer_ids)}"
)

print(
    f"Invalid customer IDs: "
    f"{len(invalid_customer_ids)}"
)

# Unresolved tickets should not have resolution time
invalid_unresolved_resolution = (
    support["status"].isin(
        ["Open", "In Progress"]
    )
    & support["resolution_time_hours"].notna()
).sum()


# Unresolved tickets should not have satisfaction score
invalid_unresolved_satisfaction = (
    support["status"].isin(
        ["Open", "In Progress"]
    )
    & support["satisfaction_score"].notna()
).sum()


# Resolved tickets should have resolution time
invalid_resolved_resolution = (
    support["status"].isin(
        ["Resolved", "Closed"]
    )
    & support["resolution_time_hours"].isna()
).sum()


# Resolved tickets should have satisfaction score
invalid_resolved_satisfaction = (
    support["status"].isin(
        ["Resolved", "Closed"]
    )
    & support["satisfaction_score"].isna()
).sum()


print("\nBusiness Logic Validation")
print("-" * 30)

print(
    "Unresolved tickets with resolution time:",
    invalid_unresolved_resolution
)

print(
    "Unresolved tickets with satisfaction score:",
    invalid_unresolved_satisfaction
)

print(
    "Resolved tickets without resolution time:",
    invalid_resolved_resolution
)

print(
    "Resolved tickets without satisfaction score:",
    invalid_resolved_satisfaction
)

invalid_satisfaction = (
    support["satisfaction_score"].notna()
    & (
        (support["satisfaction_score"] < 1)
        | (support["satisfaction_score"] > 5)
    )
).sum()

print(
    "\nInvalid Satisfaction Scores:",
    invalid_satisfaction
)

if (
    duplicate_ids == 0
    and len(invalid_customer_ids) == 0
    and invalid_unresolved_resolution == 0
    and invalid_unresolved_satisfaction == 0
    and invalid_resolved_resolution == 0
    and invalid_resolved_satisfaction == 0
    and invalid_satisfaction == 0
):
    print("STATUS: PASS")
    print("Support ticket dataset passed validation.")
else:
    print("STATUS: REVIEW")
    print("Data quality issues were detected.")