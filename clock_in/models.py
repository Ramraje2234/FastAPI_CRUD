from pydantic import BaseModel, EmailStr


class ClockInInput(BaseModel):
    email: EmailStr
    location: str


def clock_in_serializer(record) -> dict:
    return {
        "id": str(record["_id"]),
        "email": record["email"],
        "location": record["location"],
        "clock_in_time": record["clock_in_time"].isoformat()
    }

