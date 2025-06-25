# main_fastapi.py (Schema-based version)

from fastapi import FastAPI, Depends, HTTPException
import sqlite3
import crud, schemas, database

# Initialize the database on startup
database.init_db()

app = FastAPI(
    title="Bitespeed Identity Service",
    description="A service to handle identity reconciliation for contacts."
)

# This dependency for getting a DB connection remains the same.
def get_db_connection():
    conn = sqlite3.connect("bitespeed_raw.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# 1. The decorator now includes `response_model` to enforce the output structure.
# 2. The `identify` function is no longer `async`.
# 3. The function now expects a Pydantic model `schemas.IdentifyRequest` as the body.
@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify(
    request: schemas.IdentifyRequest, # FastAPI automatically parses and validates the body into this object
    db: sqlite3.Connection = Depends(get_db_connection)
):
    # No more manual JSON parsing!
    # We access the validated data directly from the request object.
    email = request.email
    phone_number = request.phoneNumber

    if not email and not phone_number:
        raise HTTPException(
            status_code=400,
            detail="Email or phoneNumber must be provided",
        )

    try:
        result = crud.identify_contact(db, email=email, phoneNumber=phone_number)
        
        # FastAPI automatically validates that 'result' matches the 'IdentifyResponse'
        # schema before sending it to the client.
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred: {str(e)}"
        )