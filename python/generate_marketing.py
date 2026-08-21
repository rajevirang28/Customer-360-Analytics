import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
OUTPUT_FILE = RAW_DIR / "marketing.csv"

NUM_INTERACTIONS = 50_000

np.random.seed(42)

customers = pd.read_csv(CUSTOMERS_FILE)

customer_ids = customers["customer_id"].values

print("Customers loaded:", len(customer_ids))

campaigns = [
    "Summer Sale",
    "Winter Sale",
    "New Year Sale",
    "Diwali Sale",
    "Republic Day Sale",
    "Independence Day Sale",
    "Mega Electronics Sale",
    "Fashion Week",
    "Weekend Offer",
    "Flash Sale"
]

channels = [
    "Email",
    "SMS",
    "Push Notification",
    "Google Ads",
    "Facebook Ads",
    "Instagram"
]

channel_probabilities = [
    0.25,
    0.15,
    0.15,
    0.18,
    0.15,
    0.12
]

marketing_data = []

for i in range(1, NUM_INTERACTIONS + 1):

    customer_id = np.random.choice(
        customer_ids
    )

    campaign_name = np.random.choice(
        campaigns
    )

    channel = np.random.choice(
        channels,
        p=channel_probabilities
    )

    sent_date = pd.Timestamp(
        np.random.choice(
            pd.date_range(
                start="2024-01-01",
                end="2026-08-20"
            )
        )
    )

    # Whether message was opened
    opened = np.random.choice(
        [0, 1],
        p=[0.35, 0.65]
    )

    # Click is possible mostly when opened
    if opened == 1:
        clicked = np.random.choice(
            [0, 1],
            p=[0.60, 0.40]
        )
    else:
        clicked = 0

    # Conversion is more likely after click
    if clicked == 1:
        converted = np.random.choice(
            [0, 1],
            p=[0.70, 0.30]
        )
    else:
        converted = 0

    # Conversion value
    if converted == 1:
        conversion_value = round(
            np.random.uniform(500, 25000),
            2
        )
    else:
        conversion_value = 0.0

    marketing_data.append(
        {
            "campaign_id": f"CMP{i:05d}",
            "customer_id": customer_id,
            "campaign_name": campaign_name,
            "channel": channel,
            "sent_date": sent_date,
            "opened": opened,
            "clicked": clicked,
            "converted": converted,
            "conversion_value": conversion_value
        }
    )

df = pd.DataFrame(marketing_data)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 50)
print("MARKETING DATASET GENERATED")
print("=" * 50)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate Campaign IDs:",
    df["campaign_id"].duplicated().sum()
)

print(
    "\nUnique Customers:",
    df["customer_id"].nunique()
)

print("\nChannels:")
print(df["channel"].value_counts())

print("\nCampaigns:")
print(df["campaign_name"].value_counts())

print("\nOpened:")
print(df["opened"].value_counts())

print("\nClicked:")
print(df["clicked"].value_counts())

print("\nConverted:")
print(df["converted"].value_counts())

print(
    "\nTotal Conversion Value:",
    round(df["conversion_value"].sum(), 2)
)

print(f"\nFile saved at:\n{OUTPUT_FILE}")