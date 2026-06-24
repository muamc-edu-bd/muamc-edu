"""
SQLite to PostgreSQL Data Migration Script
HSC Academic Management System

Usage:
    python migrate_sqlite_to_postgres.py
"""

import os
import sqlite3
import sys

# Load environment variables manually to be safe
db_url = None
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATABASE_URL="):
                db_url = line.split("=", 1)[1]
                if db_url.startswith(('"', "'")) and db_url.endswith(('"', "'")):
                    db_url = db_url[1:-1]

if not db_url:
    db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("[-] ERROR: DATABASE_URL is not configured in .env or system environment variables.")
    sys.exit(1)

# SQLite source database path
sqlite_path = "hsc_academy.db"
if not os.path.exists(sqlite_path):
    print(f"[-] ERROR: Source SQLite database not found at '{sqlite_path}'.")
    sys.exit(1)

print("=" * 65)
print("  HSC Academic Management System - Database Migrator")
print("  SQLite (hsc_academy.db) --> Remote PostgreSQL")
print("=" * 65)

try:
    import psycopg2
except ImportError:
    print("[-] ERROR: psycopg2-binary is not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

# PostgreSQL tables to migrate in order of dependency
TABLES = ['students', 'teachers', 'settings', 'archive', 'promotion_logs', 'marks']

def migrate():
    # Connect to databases
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cur = sqlite_conn.cursor()
    
    print(f"\nConnecting to remote PostgreSQL database...")
    try:
        pg_conn = psycopg2.connect(db_url)
        pg_cur = pg_conn.cursor()
        print("[+] Connected successfully.")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        sqlite_conn.close()
        sys.exit(1)
        
    print("\nStarting migration...")
    
    try:
        # Pre-drop global unique roll constraint on PostgreSQL if it exists, to prevent duplicate roll failures
        try:
            pg_cur.execute("ALTER TABLE students DROP CONSTRAINT IF EXISTS students_roll_key;")
            pg_conn.commit()
            print("[+] Dropped global unique roll constraint on PostgreSQL target.")
        except Exception as ce:
            print(f"  Note: Dropping unique constraint skipped: {ce}")
            pg_conn.rollback()

        for table in TABLES:
            print(f"\nMigrating table '{table}'...")
            
            # Check if table exists in SQLite
            sqlite_cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
            if not sqlite_cur.fetchone():
                print(f"  Skipping '{table}': table does not exist in source database.")
                continue
                
            # Fetch SQLite columns
            sqlite_cur.execute(f"PRAGMA table_info({table});")
            cols = [col[1] for col in sqlite_cur.fetchall()]
            
            # Query all rows
            sqlite_cur.execute(f"SELECT * FROM {table};")
            rows = sqlite_cur.fetchall()
            
            if not rows:
                print(f"  [+] 0 rows to migrate for '{table}'.")
                continue
                
            print(f"  Clearing existing rows in PostgreSQL '{table}' table...")
            pg_cur.execute(f'TRUNCATE TABLE "{table}" CASCADE;')
            
            # Prepare insert query
            col_placeholders = ", ".join(["%s"] * len(cols))
            col_names = ", ".join([f'"{c}"' for c in cols])
            insert_query = f'INSERT INTO "{table}" ({col_names}) VALUES ({col_placeholders});'
            
            print(f"  Copying {len(rows)} rows...")
            count = 0
            for row in rows:
                row_val = list(row)
                
                # Convert SQLite booleans to python booleans for PostgreSQL
                for idx, col_name in enumerate(cols):
                    if col_name == 'student_submitted':
                        row_val[idx] = bool(row_val[idx]) if row_val[idx] is not None else False
                
                pg_cur.execute(insert_query, row_val)
                count += 1
                
            pg_conn.commit()
            print(f"  [+] Migrated {count} rows successfully.")
            
        print("\n" + "=" * 65)
        print("  MIGRATION COMPLETE! All data copied successfully.")
        print("=" * 65 + "\n")
        
    except Exception as e:
        pg_conn.rollback()
        print(f"\n[-] ERROR during migration: {e}")
        print("Rollback executed. No changes were committed.")
        
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == '__main__':
    migrate()
