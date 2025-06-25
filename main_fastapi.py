# main_fastapi.py

from fastapi import FastAPI, Depends, HTTPException
import sqlite3

# Make sure all imports are correct
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

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bitespeed Identity Service is running."}

# The decorator now correctly uses 'IdentifyResponse' as the response_model
@app.post("/identify", response_model=schemas.IdentifyResponse) ### THIS IS THE FIX ###
def identify(
    request: schemas.IdentifyRequest, # The request body is validated against this model
    db: sqlite3.Connection = Depends(get_db_connection)
):
    email = request.email
    phone_number = request.phoneNumber

    if not email and not phone_number:
        raise HTTPException(
            status_code=400,
            detail="Email or phoneNumber must be provided",
        )

    try:
        # The result from this function matches the IdentifyResponse schema
        result = crud.identify_contact(db, email=email, phoneNumber=phone_number)
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred: {str(e)}"
        )