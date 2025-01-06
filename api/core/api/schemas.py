import datetime

from ninja import Schema
from pydantic import EmailStr


class UserSchema(Schema):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
