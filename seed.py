import pandas as pd
from datetime import datetime
from decimal import Decimal
from app.models import TickerDataCreate
from app import crud

# Convert the Google Sheet link to a CSV export URL
CSV_URL = "https://docs.google.com/spreadsheets/d/1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8/export?format=csv"

def seed_data():
    try:
        df = pd.read_csv(CSV_URL)
    except Exception as e:
        print(f"Error reading CSV data: {e}")
        return

    # Iterate over DataFrame rows and insert each row into the database
    for index, row in df.iterrows():
        try:
            data = {
                "datetime": pd.to_datetime(row["datetime"]),
                "open": Decimal(str(row["open"])),
                "high": Decimal(str(row["high"])),
                "low": Decimal(str(row["low"])),
                "close": Decimal(str(row["close"])),
                "volume": int(row["volume"]),
                "instrument": row["instrument"]  # Ensure the column name matches your CSV header
            }
            ticker_data = TickerDataCreate(**data)
            created_item = crud.create_data(ticker_data)
            print(f"Inserted row with id: {created_item['id']}")
        except Exception as e:
            print(f"Error inserting row {data}: {e}")

if __name__ == "__main__":
    seed_data()
