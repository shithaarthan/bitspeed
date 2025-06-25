# main_flask.py

from flask import Flask, request, jsonify, g
import sqlite3
import database
import crud

app = Flask(__name__)

# This function gets a db connection for the current request.
# It stores it in 'g', a special object that is unique for each request.
def get_db():
    if 'db' not in g:
        g.db = database.get_db_connection()
    return g.db

# This function is called after each request, to close the connection.
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the database when the app starts
with app.app_context():
    database.init_db()

@app.route('/identify', methods=['POST'])
def identify():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    phone_number = str(data.get("phoneNumber")) if data.get("phoneNumber") is not None else None

    if not email and not phone_number:
        return jsonify({"error": "Email or phoneNumber must be provided"}), 400
    
    # Get the database connection for this request
    conn = get_db()
    
    try:
        # Call the core logic function
        result = crud.identify_contact(conn, email=email, phoneNumber=phone_number)
        return jsonify(result)
    except Exception as e:
        # It's good practice to rollback changes if an error occurs
        conn.rollback()
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)