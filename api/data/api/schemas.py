import datetime
from pathlib import Path
from ninja import Schema
from pydantic import BaseModel, ConfigDict, field_validator

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


class CSVFileSchema(BaseModel):
    id: int
    file: str
    presigned_url: str | None = None
    processed: bool
    processed_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("file", mode="before")
    def file_to_basename(cls, v):
        return Path(str(v)).name if v is not None else None
