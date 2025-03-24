from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class TickerDataBase(BaseModel):
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    instrument: str

class TickerDataCreate(TickerDataBase):
    pass

class TickerData(TickerDataBase):
    id: int

    class Config:
        # For Pydantic V2, use 'from_attributes' instead of 'orm_mode'
        from_attributes = True
