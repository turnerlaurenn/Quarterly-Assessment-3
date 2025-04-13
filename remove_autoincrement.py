import sqlite3
import shutil
import os

# Backup first
original_db = "questions.db"
backup_db = "questions_backup.db"
shutil.copyfile(original_db, backup_db)
print(f"✅ Backup created at {backup_db}")

# Connect to the original database
conn = sqlite3.connect(original_db)
cursor = conn.cursor()

# Get user-defined tables only (excluding internal ones)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    try:
        # Get original schema
        cursor.execute(f"PRAGMA table_info('{table}')")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info if col[1] != 'id']
        
        # Create a temporary table without AUTOINCREMENT
        temp_table = f"{table}_temp"
        cursor.execute(f"""
            CREATE TABLE '{temp_table}' (
                id INTEGER PRIMARY KEY,
                {', '.join([f"{col[1]} {col[2]}" for col in columns_info if col[1] != 'id'])}
            )
        """)
        
        # Copy data to the new table
        cursor.execute(f"""
            INSERT INTO '{temp_table}' (id, {', '.join(columns)})
            SELECT id, {', '.join(columns)} FROM '{table}'
        """)
        
        # Drop the old table and rename the new one
        cursor.execute(f"DROP TABLE '{table}'")
        cursor.execute(f"ALTER TABLE '{temp_table}' RENAME TO '{table}'")
        
        print(f"✅ Table '{table}' converted.")
    except Exception as e:
        print(f"❌ Error converting table '{table}': {e}")

conn.commit()
conn.close()
print("🎉 Done!")
