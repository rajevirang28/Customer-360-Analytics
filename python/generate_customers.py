import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

# Initialize Faker
fake = Faker("en_IN")

# Make results reproducible
Faker.seed(42)
np.random.seed(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "customers.csv"

# Configuration
NUM_CUSTOMERS = 10_000

# Indian locations
locations = [
    ("Pune", "Maharashtra"),
    ("Mumbai", "Maharashtra"),
    ("Nagpur", "Maharashtra"),
    ("Nashik", "Maharashtra"),
    ("Bengaluru", "Karnataka"),
    ("Mysuru", "Karnataka"),
    ("Delhi", "Delhi"),
    ("Gurgaon", "Haryana"),
    ("Noida", "Uttar Pradesh"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Ahmedabad", "Gujarat"),
    ("Surat", "Gujarat"),
    ("Kolkata", "West Bengal"),
    ("Jaipur", "Rajasthan"),
]

# Acquisition channels
acquisition_channels = [
    "Google",
    "Facebook",
    "Instagram",
    "Referral",
    "Organic Search",
    "Email",
    "Direct",
]

# Generate customers
customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    city, state = locations[
        np.random.randint(0, len(locations))
    ]

    gender = np.random.choice(
        ["Male", "Female"],
        p=[0.55, 0.45]
    )

    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()

    customer = {
        "customer_id": f"C{i:05d}",
        "name": name,
        "email": fake.email(),
        "phone": fake.numerify("##########"),
        "age": np.random.randint(18, 65),
        "gender": gender,
        "city": city,
        "state": state,
        "registration_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "acquisition_channel": np.random.choice(
            acquisition_channels
        ),
    }

    customers.append(customer)

# Convert to DataFrame
df = pd.DataFrame(customers)

# Save CSV
df.to_csv(
    OUTPUT_FILE,
    index=False
)

# Basic validation
print("\nCustomer dataset generated successfully!")

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate customer IDs:")
print(df["customer_id"].duplicated().sum())

print(f"\nFile saved at:")
print(OUTPUT_FILE)