import json
from datetime import datetime
from bson import ObjectId
from typing import Annotated, Optional
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from clock_in.models import ClockInInput, clock_in_serializer
from database import get_database


router = APIRouter(tags=['Clock-In'])


@router.post("/clock-in/")
async def create_clock_in(clock_in: ClockInInput, db=Depends(get_database)):
    resp = {"Message": "Clock-in successful", "data": []}
    try:
        collections = db["clock_in_records"]

        # Create the clock-in entry with the current timestamp
        new_clock_in = {
            "email": clock_in.email,
            "location": clock_in.location,
            "clock_in_time": datetime.utcnow()
        }

        # Insert the new record into the database
        result = await collections.insert_one(new_clock_in)

        # Fetch the newly inserted record
        inserted_record = await collections.find_one({"_id": result.inserted_id})
        if inserted_record:
            resp["data"] = clock_in_serializer(inserted_record)
        status_code = 200
    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


@router.get("/clock-in/{clock_in_id}")
async def get_clock_in(clock_in_id: str, db=Depends(get_database)):
    resp = {"Message": "Clock-in record retrieved successfully.", "data": []}
    try:
        collections = db["clock_in_records"]

        # Fetch the record by its ObjectId
        record = await collections.find_one({"_id": ObjectId(clock_in_id)})

        if record:
            resp["data"] = clock_in_serializer(record)
            status_code = 200
        else:
            resp["Message"] = "Clock-in record not found."
            status_code = 404

    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


@router.get("/clock-in/filter/")
async def filter_clock_in(
        email: Optional[str] = None,
        location: Optional[str] = None,
        clock_in_time: Optional[datetime] = None,
        db=Depends(get_database)):
    try:
        collections = db["clock_in_records"]

        # Build the query based on provided filters
        query = {}
        if email:
            query["email"] = email
        if location:
            query["location"] = location
        if clock_in_time:
            query["clock_in_time"] = {"$gt": clock_in_time}

        # Fetch filtered records from the collection
        records = await collections.find(query)
        filtered_records = [clock_in_serializer(record) for record in records]

        resp = {
            "Message": "Filtered clock-in record retrieved successfully.",
            "data": filtered_records
        }
        return JSONResponse(resp, status_code=200)

    except Exception as e:
        print(e)
        return JSONResponse({"Message": "Database have some issues.", "data": []}, status_code=500)


@router.put("/click-in/{clock_in_id}")
async def update_clock_in(clock_in_id: str, clock_in: ClockInInput, db=Depends(get_database)):
    resp = {"Message": "Clock in record updated successfully.", "data": []}
    try:
        collections = db["clock_in_records"]

        existing_record = await collections.find_one({"_id": ObjectId(clock_in_id)})
        if existing_record:
            update_data = {
                "$set": {
                    "email": clock_in.email,
                    "location": clock_in.location
                }
            }
            result = await collections.update_one({"_id": ObjectId(clock_in_id)}, update_data)

            if result.modified_count:
                updated_record = await collections.find_one({"_id": ObjectId(clock_in_id)})
                resp["data"] = clock_in_serializer(updated_record)
                status_code = 200
            else:
                resp["Message"] = "No changes made."
                status_code = 200

        else:
            resp["Message"] = "Clock-in record not found."
            status_code = 404

    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


@router.delete("/clock-in/{clock_in_id}")
async def delete_clock_in(clock_in_id: str, db=Depends(get_database)):
    resp = {"Message": "Clock-in record deleted successfully"}
    try:
        collections = db["clock_in_records"]

        result = await collections.delete_one({"_id": ObjectId(clock_in_id)})
        if result.deleted_count:
            status_code = 200
        else:
            resp["Message"] = "Clock-in record not found."
            status_code = 404
    except Exception as e:
        print(e)
        resp["Message"] = "Database have some issues."
        status_code = 500

    return JSONResponse(resp, status_code=status_code)


