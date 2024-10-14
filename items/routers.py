import json
from datetime import datetime, date
from bson import ObjectId
from typing import Annotated, Optional
from fastapi import Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from items.models import ItemInput, item_serializer
from database import get_database


router = APIRouter(tags=['Items'])


@router.post("/create_item/")
async def create_item(item: ItemInput, db=Depends(get_database)):
    resp = {"Message": "Successfully created new item", "data": []}
    try:
        collection = db["items"]

        # Check for duplicate items
        existing_item = await collection.find_one({
            "name": item.name,
            "email": item.email,
            "item_name": item.item_name
        })

        if existing_item:
            # Return error response if duplicate item is found
            resp["Message"] = "Item already exists."
            return JSONResponse(resp, status_code=400)

        expiry_datetime = datetime.combine(item.expiry_date, datetime.min.time())

        # Automatically add the current date as insert_date
        new_item = {
            "name": item.name,
            "email": item.email,
            "item_name": item.item_name,
            "quantity": item.quantity,
            "expiry_date": expiry_datetime,
            "insert_date": datetime.utcnow()  # Insert current date and time
        }

        print("Inserting record in database...")
        result = await collection.insert_one(new_item)

        print("Fetching created record from database...")
        # Retrieve the newly inserted item
        inserted_item = await collection.find_one({"_id": result.inserted_id})
        if inserted_item:
            resp["data"] = item_serializer(inserted_item)
        status_code = 200
    except Exception as e:
        print(str(e))
        status_code = 500
        resp["Message"] = "Database have some issues."

    # Return the response as a JSON object
    return JSONResponse(resp, status_code=status_code)


@router.get("/get_item/{item_id}")
async def get_item(item_id: str, db=Depends(get_database)):
    resp = {"Message": "Successfully created new item", "data": []}
    try:
        collection = db["items"]

        # Check for duplicate items
        existing_item = await collection.find_one({"_id": ObjectId(item_id)})

        if existing_item:
            resp["data"] = item_serializer(existing_item)

            resp["Message"] = "Successfully shared data."
            status_code = 200
        else:
            status_code = 404
            resp["Message"] = "Record not found."

    except Exception as e:
        print(str(e))
        status_code = 500
        resp["Message"] = "Database have some issues."

    return JSONResponse(resp, status_code=status_code)


@router.put("/update_item/{item_id}")
async def update_item(item_id: str, item: ItemInput, db=Depends(get_database)):
    resp = {"Message": "Successfully updated item", "data": []}
    try:
        collection = db["items"]

        existing_item = await collection.find_one({"_id": ObjectId(item_id)})

        if not existing_item:
            return JSONResponse({"Message": "Item not found."}, status_code=404)

        expiry_datetime = datetime.combine(item.expiry_date, datetime.min.time())

        updated_item = {
            "$set": {
                "name": item.name,
                "email": item.email,
                "item_name": item.item_name,
                "quantity": item.quantity,
                "expiry_date": expiry_datetime
            }
        }
        result = await collection.update_one({"_id": ObjectId(item_id)}, updated_item)
        if result.modified_count:
            updated = await collection.find_one({"_id": ObjectId(item_id)})
            resp["data"] = item_serializer(updated)
            status_code = 200
        else:
            resp["Message"] = "No Changes made."
            status_code = 200
    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


@router.delete("/delete_item/{item_id}")
async def delete_item(item_id: str, db=Depends(get_database)):
    resp = {"Message": "Successfully deleted item", "data": []}
    try:
        collection = db["items"]
        result = await collection.delete_one({"_id": ObjectId(item_id)})

        if result.deleted_count:
            status_code = 200
        else:
            resp["Message"] = "Item not found."
            status_code = 404

    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


@router.get("/items/filter/")
async def filter_items(
        email: Optional[str] = None,
        expiry_date: Optional[date] = None,
        insert_date: Optional[datetime] = None,
        quantity: Optional[int] = Query(None, ge=0),
        db=Depends(get_database)):
    try:
        collections = db["items"]

        # Building Query
        query = {}
        if email:
            query["email"] = email
        if expiry_date:
            query["expiry_date"] = {"$gt": datetime.combine(expiry_date, datetime.min.time())}
        if insert_date:
            query["insert_date"] = {"$gt": insert_date}
        if quantity is not None:
            query["quantity"] = {"$gte": quantity}

        # Fetch filtered items from the collection
        item_list = await collections.find(query).to_list()
        filtered_items = [item_serializer(item) for item in item_list]

        # Performer aggression: count items grouped by email
        aggregation_pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}}
        ]

        email_counts = await collections.aggregate(aggregation_pipeline).to_list()

        # Prepare response
        response = {
            "Message": "Filtered items retrieved successfully",
            "data": {
                "filtered_items": filtered_items,
                "email_counts": email_counts
            }
        }
        return JSONResponse(response, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({"Message": "Database have some issues."}, status_code=500)
