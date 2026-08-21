import pandas as pd
import psycopg2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "customer_360",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD"
}

DATASETS = {
    "customers.csv": "raw.customers",
    "products.csv": "raw.products",
    "orders.csv": "raw.orders",
    "website_events.csv": "raw.website_events",
    "marketing.csv": "raw.marketing",
    "support_tickets.csv": "raw.support_tickets"
}

print("CUSTOMER 360 - POSTGRESQL INGESTION")

print("\nConnecting to PostgreSQL...")

try:

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    print("PostgreSQL connection successful!")

except Exception as e:

    print("\nPostgreSQL connection failed")
    print("Error:", e)

    raise SystemExit

cursor = connection.cursor()

for filename, table_name in DATASETS.items():

    file_path = RAW_DIR / filename

    print("\n" + "-" * 60)
    print(f"Loading: {filename}")
    print(f"Target: {table_name}")

    try:

        df = pd.read_csv(file_path)

        print(
            f"CSV rows: {len(df):,}"
        )

        cursor.execute(
            f"TRUNCATE TABLE {table_name};"
        )

        columns = list(df.columns)

        column_names = ", ".join(
            columns
        )

        placeholders = ", ".join(
            ["%s"] * len(columns)
        )

        insert_query = f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders})
        """

        for row in df.itertuples(
            index=False,
            name=None
        ):

            # Convert pandas NaN to PostgreSQL NULL
            cleaned_row = [
                None if pd.isna(value)
                else value
                for value in row
            ]

            cursor.execute(
                insert_query,
                cleaned_row
            )

        connection.commit()

        print(
            f"Loaded successfully: {len(df):,} rows"
        )

    except Exception as e:

        connection.rollback()

        print(
            f"Failed to load {filename}"
        )

        print("Error:", e)

        cursor.close()
        connection.close()

        raise SystemExit

cursor.close()
connection.close()
print("POSTGRESQL INGESTION COMPLETE")