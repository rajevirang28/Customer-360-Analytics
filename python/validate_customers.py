import pandas as pd
from pathlib import Path

# Project path
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "customers.csv"

# Load dataset
df = pd.read_csv(INPUT_FILE)

print("=" * 50)
print("CUSTOMER DATA QUALITY REPORT")
print("=" * 50)

# 1. Shape
print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 3. Duplicate customer IDs
duplicate_ids = df["customer_id"].duplicated().sum()

print(f"\nDuplicate Customer IDs: {duplicate_ids}")

# 4. Unique customers
unique_customers = df["customer_id"].nunique()

print(f"Unique Customer IDs: {unique_customers}")

# 5. Age validation
invalid_age = ((df["age"] < 18) | (df["age"] > 65)).sum()

print(f"Invalid Ages: {invalid_age}")

# 6. Gender values
print("\nGender Distribution:")
print(df["gender"].value_counts())

# 7. Acquisition channels
print("\nAcquisition Channels:")
print(df["acquisition_channel"].value_counts())

# 8. States
print("\nTop States:")
print(df["state"].value_counts().head(10))

# 9. Final status
if (
    df.isnull().sum().sum() == 0
    and duplicate_ids == 0
    and invalid_age == 0
):
    print("\nSTATUS: PASS")
    print("Customer dataset passed basic validation.")
else:
    print("\nSTATUS: REVIEW")
    print("Data quality issues were detected.")