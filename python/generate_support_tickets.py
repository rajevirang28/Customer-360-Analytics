import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DIR / "customers.csv"
OUTPUT_FILE = RAW_DIR / "support_tickets.csv"

NUM_TICKETS = 15_000

np.random.seed(42)

customers = pd.read_csv(CUSTOMERS_FILE)

customer_ids = customers["customer_id"].values

print("Customers loaded:", len(customer_ids))

issue_types = [
    "Payment",
    "Delivery",
    "Product",
    "Refund",
    "Account",
    "Technical",
    "Other"
]

issue_probabilities = [
    0.15,
    0.25,
    0.20,
    0.15,
    0.10,
    0.10,
    0.05
]


priorities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

priority_probabilities = [
    0.25,
    0.50,
    0.20,
    0.05
]


statuses = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

status_probabilities = [
    0.10,
    0.15,
    0.35,
    0.40
]

tickets = []

for i in range(1, NUM_TICKETS + 1):

    customer_id = np.random.choice(
        customer_ids
    )

    issue_type = np.random.choice(
        issue_types,
        p=issue_probabilities
    )

    priority = np.random.choice(
        priorities,
        p=priority_probabilities
    )

    status = np.random.choice(
        statuses,
        p=status_probabilities
    )

    created_date = pd.Timestamp(
        np.random.choice(
            pd.date_range(
                start="2024-01-01",
                end="2026-08-20"
            )
        )
    )

    # Resolution time
    if status in ["Resolved", "Closed"]:

        resolution_time_hours = round(
            np.random.exponential(
                scale=24
            ),
            2
        )

        # Keep within reasonable range
        resolution_time_hours = min(
            resolution_time_hours,
            168
        )

    else:

        resolution_time_hours = np.nan


    # Satisfaction score
    if status in ["Resolved", "Closed"]:

        satisfaction_score = np.random.choice(
            [1, 2, 3, 4, 5],
            p=[
                0.05,
                0.10,
                0.20,
                0.35,
                0.30
            ]
        )

    else:

        satisfaction_score = np.nan


    tickets.append(
        {
            "ticket_id": f"T{i:06d}",
            "customer_id": customer_id,
            "created_date": created_date,
            "issue_type": issue_type,
            "priority": priority,
            "status": status,
            "resolution_time_hours": resolution_time_hours,
            "satisfaction_score": satisfaction_score
        }
    )

df = pd.DataFrame(tickets)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 50)
print("SUPPORT TICKET DATASET GENERATED")
print("=" * 50)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate Ticket IDs:",
    df["ticket_id"].duplicated().sum()
)

print(
    "\nUnique Customers:",
    df["customer_id"].nunique()
)

print("\nIssue Types:")
print(df["issue_type"].value_counts())

print("\nPriorities:")
print(df["priority"].value_counts())

print("\nStatuses:")
print(df["status"].value_counts())

print("\nAverage Resolution Time:")
print(
    round(
        df["resolution_time_hours"].mean(),
        2
    ),
    "hours"
)

print("\nAverage Satisfaction:")
print(
    round(
        df["satisfaction_score"].mean(),
        2
    )
)

print(f"\nFile saved at:\n{OUTPUT_FILE}")