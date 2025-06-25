# crud.py

import sqlite3
from datetime import datetime, timezone ### CHANGED ###

def identify_contact(conn: sqlite3.Connection, email: str | None, phoneNumber: str | None):
    cursor = conn.cursor()

    # Step 1: Find all contacts that match the given email or phone number.
    query_parts = []
    params = []
    if email:
        query_parts.append("email = ?")
        params.append(email)
    if phoneNumber:
        query_parts.append("phoneNumber = ?")
        params.append(phoneNumber)
    
    where_clause = " OR ".join(query_parts)
    
    sql_query = f"SELECT * FROM contact WHERE {where_clause} ORDER BY createdAt ASC"
    cursor.execute(sql_query, params)
    matching_contacts = cursor.fetchall()

    # Case 1: No existing contacts. Create a new primary contact.
    if not matching_contacts:
        sql_insert = """
            INSERT INTO contact (email, phoneNumber, linkPrecedence, createdAt, updatedAt)
            VALUES (?, ?, 'primary', ?, ?)
        """
        now = datetime.now(timezone.utc) ### CHANGED ###
        cursor.execute(sql_insert, (email, phoneNumber, now, now))
        new_contact_id = cursor.lastrowid
        conn.commit()
        
        return {
            "contact": {
                "primaryContatctId": new_contact_id,
                "emails": [e for e in [email] if e],
                "phoneNumbers": [p for p in [phoneNumber] if p],
                "secondaryContactIds": []
            }
        }

    # Identify the primary contact and see if we need to merge identities
    primary_contact = matching_contacts[0]
    all_primary_contacts = [c for c in matching_contacts if c['linkPrecedence'] == 'primary']

    # Case 2: We found multiple primary contacts that now need to be linked. Merge them.
    if len(all_primary_contacts) > 1:
        newest_primary = max(all_primary_contacts, key=lambda c: c['createdAt'])
        
        sql_update = """
            UPDATE contact 
            SET linkedId = ?, linkPrecedence = 'secondary', updatedAt = ?
            WHERE id = ?
        """
        cursor.execute(sql_update, (primary_contact['id'], datetime.now(timezone.utc), newest_primary['id'])) ### CHANGED ###
        conn.commit()

    # Check if the incoming request has new information
    all_emails = {c['email'] for c in matching_contacts if c['email']}
    all_phone_numbers = {c['phoneNumber'] for c in matching_contacts if c['phoneNumber']}

    new_info_found = (email and email not in all_emails) or \
                     (phoneNumber and phoneNumber not in all_phone_numbers)

    # Case 3: New information is found. Create a new secondary contact.
    if new_info_found:
        sql_insert_secondary = """
            INSERT INTO contact (email, phoneNumber, linkedId, linkPrecedence, createdAt, updatedAt)
            VALUES (?, ?, ?, 'secondary', ?, ?)
        """
        now = datetime.now(timezone.utc) ### CHANGED ###
        cursor.execute(sql_insert_secondary, (email, phoneNumber, primary_contact['id'], now, now))
        conn.commit()

    # Step 4: Consolidate all information for the response.
    primary_id = primary_contact['id']
    sql_get_all = "SELECT * FROM contact WHERE id = ? OR linkedId = ?"
    cursor.execute(sql_get_all, (primary_id, primary_id))
    all_linked_contacts = cursor.fetchall()
    
    emails = list(dict.fromkeys([c['email'] for c in all_linked_contacts if c['email']]))
    phone_numbers = list(dict.fromkeys([c['phoneNumber'] for c in all_linked_contacts if c['phoneNumber']]))
    secondary_ids = [c['id'] for c in all_linked_contacts if c['linkPrecedence'] == 'secondary']

    return {
        "contact": {
            "primaryContatctId": primary_id,
            "emails": emails,
            "phoneNumbers": phone_numbers,
            "secondaryContactIds": secondary_ids
        }
    }