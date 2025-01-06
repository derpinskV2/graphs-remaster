import datetime

from ninja import Schema

from core.api.schemas import UserSchema


class CSVDataSchema(Schema):
    user: UserSchema | None = None
    bg: float | None = None
    bg_input: float | None = None
    carb_input: float | None = None
    insulin_delivered: float | None = None
    total_insulin: float | None = None
    bolus: float | None = None
    event: str | None = None
    serial_number: str | None = None
    timestamp: datetime.datetime


class CSVFileSchema(Schema):
    id: int
    file: str
    processed: bool
    processed_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
