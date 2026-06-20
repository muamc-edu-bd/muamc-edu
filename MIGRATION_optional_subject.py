"""
MIGRATION: Add optional_subject column to students table
=========================================================
Run this once against your PostgreSQL database.

Usage:
    python MIGRATION_optional_subject.py
    
Or via psql:
    psql $DATABASE_URL -c "ALTER TABLE students ADD COLUMN IF NOT EXISTS optional_subject VARCHAR(20) DEFAULT '';"
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://hsc_academy_db_obhw_user:<password>@dpg-d8pu0r3eo5us73ai1glg-a:5432/hsc_academy_db_obhw')

# ── Option A: run via psql shell ────────────────────────────────────────
SQL = """
ALTER TABLE students ADD COLUMN IF NOT EXISTS optional_subject VARCHAR(20) DEFAULT '';
"""

# ── Option B: run via SQLAlchemy / psycopg2 ─────────────────────────────
if __name__ == '__main__':
    try:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cur  = conn.cursor()
        cur.execute(SQL)
        conn.commit()
        cur.close()
        conn.close()
        print("✅  Migration successful: 'optional_subject' column added to students table.")
    except Exception as e:
        print(f"❌  Migration failed: {e}")
        print("Run manually via psql:")
        print(f"    psql $DATABASE_URL -c \"{SQL.strip()}\"")


# ── models.py — ADD this field to the Student class ─────────────────────
# In your models.py, inside the Student model, add:
#
#   optional_subject = db.Column(db.String(20), default='')
#
# And inside to_dict(), add:
#
#   'optional_subject': self.optional_subject or '',
#
# FULL EXAMPLE (add alongside existing fields like 'session'):
#
#   class Student(db.Model):
#       __tablename__ = 'students'
#       id               = db.Column(db.String(32), primary_key=True)
#       name             = db.Column(db.String(200), nullable=False)
#       roll             = db.Column(db.String(50), unique=True, nullable=False)
#       reg              = db.Column(db.String(50), default='')
#       cls              = db.Column(db.String(20), default='')
#       group            = db.Column(db.String(30), default='')
#       section          = db.Column(db.String(10), default='')
#       father           = db.Column(db.String(200), default='')
#       mother           = db.Column(db.String(200), default='')
#       dob              = db.Column(db.String(20), default='')
#       phone            = db.Column(db.String(20), default='')
#       religion         = db.Column(db.String(50), default='')
#       year             = db.Column(db.String(20), default='')
#       session          = db.Column(db.String(20), default='')
#       photo            = db.Column(db.Text, default='')
#       optional_subject = db.Column(db.String(20), default='')   # <── ADD THIS
#
#       def to_dict(self):
#           return {
#               'id':               self.id,
#               'name':             self.name,
#               'roll':             self.roll,
#               'reg':              self.reg or '',
#               'cls':              self.cls,
#               'group':            self.group,
#               'section':          self.section or '',
#               'father':           self.father or '',
#               'mother':           self.mother or '',
#               'dob':              self.dob or '',
#               'phone':            self.phone or '',
#               'religion':         self.religion or '',
#               'year':             self.year or '',
#               'session':          self.session or '',
#               'photo':            self.photo or '',
#               'optional_subject': self.optional_subject or '',  # <── ADD THIS
#           }
