import sqlite3

DB_PATH = 'contracts_app.db'

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add columns to the `contracts` table if they don't exist
try:
    cursor.execute('''
        ALTER TABLE contracts ADD COLUMN landlord_id INTEGER
    ''')
    print("`landlord_id` column added to `contracts` table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("`landlord_id` column already exists.")
    else:
        raise e

try:
    cursor.execute('''
        ALTER TABLE contracts ADD COLUMN tenant_id INTEGER
    ''')
    print("`tenant_id` column added to `contracts` table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("`tenant_id` column already exists.")
    else:
        raise e

try:
    cursor.execute('''
        ALTER TABLE contracts ADD COLUMN seller_id INTEGER
    ''')
    print("`seller_id` column added to `contracts` table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("`seller_id` column already exists.")
    else:
        raise e

try:
    cursor.execute('''
        ALTER TABLE contracts ADD COLUMN buyer_id INTEGER
    ''')
    print("`buyer_id` column added to `contracts` table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("`buyer_id` column already exists.")
    else:
        raise e

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database schema updated.")
