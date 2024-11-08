import sqlite3
from datetime import datetime

DB_PATH = 'contracts_app.db'

# Function to insert user details and return user ID
def insert_user_details(user_data):
    """
    Insert user details into the database and return the user ID.
    Args:
    - user_data: Dictionary containing user details.
    """
    full_name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
    
    if not full_name:
        raise ValueError("User name cannot be empty.")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, full_name, address, cnp, id_series, id_number, issuing_authority, issue_date, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data.get('first_name'),
            user_data.get('last_name'),
            full_name,
            user_data.get('address'),
            user_data.get('cnp'),
            user_data.get('id_series'),
            user_data.get('id_number'),
            user_data.get('issuing_authority'),
            user_data.get('issue_date'),
            user_data.get('type')
        ))
        conn.commit()
        return cursor.lastrowid  # Return the generated user ID

# Function to insert contract metadata and return contract ID
def insert_contract(contract_data):
    """
    Insert contract metadata into the database and return the contract ID.
    Args:
    - contract_data: Dictionary containing contract details.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contracts (contract_type, contract_date, landlord_id, tenant_id, seller_id, buyer_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            contract_data.get('contract_type'),
            datetime.now(),  # Use current timestamp for contract_date
            contract_data.get('landlord_id'),
            contract_data.get('tenant_id'),
            contract_data.get('seller_id'),
            contract_data.get('buyer_id')
        ))
        conn.commit()
        return cursor.lastrowid  # Return the generated contract ID

# Function to insert contract-specific details
def insert_contract_details(contract_id, details):
    """
    Insert contract-specific details into the database.
    Args:
    - contract_id: ID of the contract.
    - details: Dictionary containing key-value pairs of contract details.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for key, value in details.items():
            cursor.execute('''
                INSERT INTO contract_details (contract_id, detail_key, detail_value)
                VALUES (?, ?, ?)
            ''', (contract_id, key, value))
        conn.commit()

# Function to insert contract content as a BLOB
def insert_contract_content(contract_id, content):
    """
    Insert a copy of the contract content as a BLOB into the database.
    Args:
    - contract_id: ID of the contract.
    - content: Binary content of the contract document.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contract_content (contract_id, content)
            VALUES (?, ?)
        ''', (contract_id, content))
        conn.commit()

# Function to retrieve user details by user ID and type
def get_user_details(user_id, user_type):
    """
    Retrieve user details for a specific user and type.
    Args:
    - user_id: The ID of the user.
    - user_type: 'landlord', 'tenant', 'seller', or 'buyer'.
    
    Returns:
    - Dictionary of user details.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT first_name, last_name, full_name, address, cnp, id_series, id_number, issuing_authority, issue_date
            FROM users
            WHERE user_id = ? AND type = ?
        ''', (user_id, user_type))
        row = cursor.fetchone()
        if row:
            return {
                "first_name": row[0],
                "last_name": row[1],
                "full_name": row[2],
                "address": row[3],
                "cnp": row[4],
                "id_series": row[5],
                "id_number": row[6],
                "issuing_authority": row[7],
                "issue_date": row[8]
            }
        return None

# Function to check if a user already exists based on CNP
def user_exists(cnp):
    """
    Check if a user already exists in the 'users' table based on CNP.
    Args:
    - cnp: The CNP of the user.
    
    Returns:
    - Boolean indicating if the user exists.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM users WHERE cnp = ?
        ''', (cnp,))
        return cursor.fetchone() is not None

# Function to retrieve contract details by contract ID
def get_contract_details(contract_id):
    """
    Retrieve contract details for a specific contract ID.
    Args:
    - contract_id: The ID of the contract.
    
    Returns:
    - Dictionary of contract details.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT detail_key, detail_value
            FROM contract_details
            WHERE contract_id = ?
        ''', (contract_id,))
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows} if rows else None

# Function to retrieve contract content
def get_contract_content(contract_id):
    """
    Retrieve contract content as a BLOB for a specific contract ID.
    Args:
    - contract_id: The ID of the contract.
    
    Returns:
    - Binary content of the contract document.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT content
            FROM contract_content
            WHERE contract_id = ?
        ''', (contract_id,))
        row = cursor.fetchone()
        return row[0] if row else None
