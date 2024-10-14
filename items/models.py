from datetime import date
from pydantic import BaseModel, EmailStr


# Pydantic model for input data
class ItemInput(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date


def item_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"].strftime('%Y-%m-%d'),
        "insert_date": item["insert_date"].isoformat()
    }

