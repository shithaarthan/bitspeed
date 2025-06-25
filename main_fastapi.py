# main_fastapi.py (No Schemas Version)

from fastapi import FastAPI, Depends, HTTPException, Request ### CHANGED: Imported Request
import sqlite3
import json ### CHANGED: Imported json for error handling

# We no longer import schemas
import crud, database ### CHANGED

# Initialize the database on startup (this part is unchanged)
database.init_db()

app = FastAPI()

# The dependency for getting a DB connection is unchanged. It's still the best way.
def get_db_connection():
    conn = database.get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


# ### CHANGED: The decorator no longer has 'response_model'
@app.post("/identify")
# ### CHANGED: The function is now 'async' and takes a raw 'Request' object
async def identify(
    request: Request,
    db: sqlite3.Connection = Depends(get_db_connection)
):
    # --- Manual Request Body Handling (replaces Pydantic) ---
    try:
        # We must now manually get the JSON body and handle potential errors.
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")

    # We manually get the values from the dictionary, like in Flask.
    email = data.get("email")
    phone_number = str(data.get("phoneNumber")) if data.get("phoneNumber") is not None else None
    # --- End of Manual Handling ---

    if not email and not phone_number:
        raise HTTPException(
            status_code=400,
            detail="Email or phoneNumber must be provided",
        )

    try:
        # The call to the core logic remains the same.
        result = crud.identify_contact(db, email=email, phoneNumber=phone_number)
        # FastAPI will still automatically convert our dictionary to a JSON response.
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred: {str(e)}"
        )