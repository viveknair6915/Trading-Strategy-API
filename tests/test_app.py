import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pandas as pd

from app.models import TickerDataCreate
from app import crud, strategy, database

class TestTickerDataValidation(unittest.TestCase):
    def test_valid_ticker_data(self):
        data = {
            "datetime": datetime.now(),
            "open": Decimal("100.50"),
            "high": Decimal("101.00"),
            "low": Decimal("100.00"),
            "close": Decimal("100.75"),
            "volume": 1500,
            "instrument": "TestInstrument"
        }
        ticker = TickerDataCreate(**data)
        self.assertEqual(ticker.volume, 1500)
        self.assertEqual(ticker.instrument, "TestInstrument")

    def test_invalid_data_type(self):
        data = {
            "datetime": "not-a-datetime",
            "open": "not-a-decimal",
            "high": Decimal("101.00"),
            "low": Decimal("100.00"),
            "close": Decimal("100.75"),
            "volume": "not-an-int",
            "instrument": "TestInstrument"
        }
        with self.assertRaises(Exception):
            TickerDataCreate(**data)

class TestCRUD(unittest.TestCase):
    @patch('app.crud.get_connection')
    def test_get_all_data(self, mock_get_connection):
        # Setup a dummy connection and cursor
        dummy_cursor = MagicMock()
        dummy_cursor.fetchall.return_value = [
            {
                "id": 1,
                "datetime": "2025-03-20 09:30:00",
                "open": 100.50,
                "high": 101.00,
                "low": 100.00,
                "close": 100.75,
                "volume": 1500,
                "instrument": "TestInstrument"
            }
        ]
        dummy_conn = MagicMock()
        dummy_conn.cursor.return_value = dummy_cursor
        mock_get_connection.return_value = dummy_conn
        
        result = crud.get_all_data()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["id"], 1)

    @patch('app.crud.get_connection')
    def test_create_data(self, mock_get_connection):
        # Setup dummy connection and cursor for create_data
        dummy_cursor = MagicMock()
        dummy_cursor.fetchone.return_value = [2]
        dummy_conn = MagicMock()
        dummy_conn.cursor.return_value = dummy_cursor
        mock_get_connection.return_value = dummy_conn
        
        data = {
            "datetime": datetime(2025, 3, 20, 9, 30),
            "open": Decimal("100.50"),
            "high": Decimal("101.00"),
            "low": Decimal("100.00"),
            "close": Decimal("100.75"),
            "volume": 1500,
            "instrument": "TestInstrument"
        }
        ticker = TickerDataCreate(**data)
        result = crud.create_data(ticker)
        self.assertEqual(result["id"], 2)
        self.assertEqual(result["volume"], 1500)
        self.assertEqual(result["instrument"], "TestInstrument")

class TestStrategy(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset with 25 entries
        self.sample_data = [
            {
                "id": i,
                "datetime": f"2025-03-{(i//2)+1:02d} 09:30:00",
                "open": 100 + i,
                "high": 101 + i,
                "low": 99 + i,
                "close": 100 + i,
                "volume": 1500,
                "instrument": "TestInstrument"
            }
            for i in range(25)
        ]
    
    def test_empty_data(self):
        with patch('app.strategy.crud.get_all_data', return_value=[]):
            result = strategy.evaluate_strategy()
            self.assertIn("error", result)
    
    def test_moving_average_calculation(self):
        with patch('app.strategy.crud.get_all_data', return_value=self.sample_data):
            result = strategy.evaluate_strategy()
            self.assertIn("cumulative_return", result)
            self.assertIsInstance(result["cumulative_return"], float)

class TestDatabaseConnection(unittest.TestCase):
    @patch("app.database.psycopg2.connect")
    def test_get_connection(self, mock_connect):
        dummy_conn = MagicMock()
        mock_connect.return_value = dummy_conn
        conn = database.get_connection()
        self.assertEqual(conn, dummy_conn)
        mock_connect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
