from database import init_db, drop_db, Base, engine
from models import VoterAddress

# Drop all tables
Base.metadata.drop_all(engine)
print("Dropped all tables")

# Create all tables
Base.metadata.create_all(engine)
print("Created all tables")

# Check the voter_address table structure
import sqlite3
conn = sqlite3.connect('voter_registration.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(voter_address)")
print("VoterAddress table structure:")
for column in cursor.fetchall():
    print(column)
conn.close()
