from app.database import get_connection
from app.models import TickerDataCreate
import psycopg2.extras
from typing import List, Dict, Any

def get_all_data() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM ticker_data;")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def create_data(item: TickerDataCreate) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO ticker_data (datetime, open, high, low, close, volume, instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    values = (
        item.datetime, item.open, item.high, item.low,
        item.close, item.volume, item.instrument
    )
    cursor.execute(query, values)
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {**item.dict(), "id": new_id}
