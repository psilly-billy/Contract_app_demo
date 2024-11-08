import sqlite3

DB_PATH = 'contracts_app.db'

# Connect to the database and drop existing tables
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.executescript('''
        DROP TABLE IF EXISTS placeholders;
        DROP TABLE IF EXISTS contract_details;
        DROP TABLE IF EXISTS contracts;
        DROP TABLE IF EXISTS users;
    ''')

    # Recreate the users table
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            full_name TEXT NOT NULL,
            address TEXT,
            cnp TEXT UNIQUE,
            id_series TEXT,
            id_number TEXT,
            issuing_authority TEXT,
            issue_date TEXT,
            marital_status TEXT,
            type TEXT CHECK (type IN ('landlord', 'tenant', 'seller', 'buyer'))
        );
    ''')

    # Recreate the contracts table
    cursor.execute('''
        CREATE TABLE contracts (
            contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_type TEXT CHECK (contract_type IN ('rental', 'sale')),
            contract_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            landlord_id INTEGER,
            tenant_id INTEGER,
            seller_id INTEGER,
            buyer_id INTEGER,
            FOREIGN KEY (landlord_id) REFERENCES users(user_id),
            FOREIGN KEY (tenant_id) REFERENCES users(user_id),
            FOREIGN KEY (seller_id) REFERENCES users(user_id),
            FOREIGN KEY (buyer_id) REFERENCES users(user_id)
        );
    ''')

    # Recreate the contract_details table
    cursor.execute('''
        CREATE TABLE contract_details (
            detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            detail_key TEXT,
            detail_value TEXT,
            FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
        );
    ''')

    # Recreate the placeholders table
    cursor.execute('''
        CREATE TABLE placeholders (
            placeholder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            placeholder_key TEXT,
            placeholder_value TEXT,
            FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
        );
    ''')

    # Commit changes
    conn.commit()

print("Database schema recreated successfully.")
