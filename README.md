# FastAPI CRUD Application

This project is a CRUD (Create, Read, Update, Delete) application built with FastAPI and MongoDB. It provides endpoints for managing items and clock-in records.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Setup and Running the Project](#setup-and-running-the-project)
- [Endpoints](#endpoints)
  - [Items Endpoints](#items-endpoints)
  - [Clock-In Endpoints](#clock-in-endpoints)

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **MongoDB**: A NoSQL database that uses a document-oriented data model.
- **Pydantic**: Data validation and settings management using Python type annotations.

## Setup and Running the Project

To set up and run the project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd <repo-name>
   
2. **Create a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
   
4. **Start the MongoDB Server: Make sure you have MongoDB installed and running on your local machine or connect to your MongoDB Atlas instance.**

5. **Run the Application**:
6. ```bash
    uvicorn app:app --reload --host 0.0.0.0 --port 8423
7. **Access the API Documentation**: Open your web browser and go to http://127.0.0.1:8423/docs to view the automatically generated API documentation.

# Endpoints
## Items Endpoints
- **Create Item**:

  - **POST** /create_item/
  - Request body: { "name": "string", "email": "string", "item_name": "string", "quantity": integer, "expiry_date": "YYYY-MM-DD" }
  - Response: { "Message": "Successfully created new item", "data": { ... } }


- **Get Item**:
  - **GET** /get_item/{item_id}
  - Response: { "Message": "Successfully shared data.", "data": { ... } }


- **Update Item**:

  - **PUT**  /update_item/{item_id}
  - Request body: { "name": "string", "email": "string", "item_name": "string", "quantity": integer, "expiry_date": "YYYY-MM-DD" }
  - Response: { "Message": "Successfully updated item", "data": { ... } }


- **Delete Item**:

  - **DELETE** /delete_item/{item_id}
  - Response: { "Message": "Successfully deleted item" }


- **Filter Items**:

  - **GET** /items/filter/
  - Query Parameters: email, expiry_date, insert_date, quantity
  - Response: { "Message": "Filtered items retrieved successfully", "data": { "filtered_items": [...], "email_counts": [...] } }


## Clock-In Endpoints


- **Create Clock-In**:

  - **POST** /clock-in/
  - Request body: { "email": "string", "location": "string" }
  - Response: { "Message": "Clock-in successful", "data": { ... } }


- **Get Clock-In Record**:
  - **GET** /clock-in/{clock_in_id}
  - Response: { "Message": "Clock-in record retrieved successfully.", "data": { ... } }


- **Filter Clock-Ins**:
  - **GET** /clock-in/filter/
  - Query Parameters: email, location, clock_in_time
  - Response: { "Message": "Filtered clock-in record retrieved successfully.", "data": [...] }


- **Update Clock-In**:
  - **PUT** /click-in/{clock_in_id}
  - Request body: { "email": "string", "location": "string" }
  - Response: { "Message": "Clock in record updated successfully.", "data": { ... } }


- **Delete Clock-In**:
  - **DELETE** /clock-in/{clock_in_id}
  - Response: { "Message": "Clock-in record deleted successfully" }