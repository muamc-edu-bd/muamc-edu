"""
Database Initialization and Migration Script
HSC Academic Management System

Usage:
    python db_init.py

This script:
1. Creates all database tables in PostgreSQL
2. (Optional) Migrates data from legacy JSON files if they exist
"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text
from app import app, db
from models import Student, Mark, Teacher, Setting, Archive, PromotionLog, AdmissionApplication


def load_json_file(file_path):
    """Load data from a JSON file. Returns None if missing or invalid."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  Error reading {file_path}: {e}")
        return None


def migrate_students_from_json(data_dir):
    students_data = load_json_file(os.path.join(data_dir, 'students.json'))
    if not students_data:
        print("  No students.json found. Skipping.")
        return 0

    print(f"  Migrating {len(students_data)} students...")
    count = 0
    for d in students_data:
        try:
            db.session.add(Student(
                id=d.get('id'),
                name=d.get('name', ''),
                roll=d.get('roll', ''),
                reg=d.get('reg', ''),
                cls=d.get('cls', ''),
                group=d.get('group', ''),
                section=d.get('section', ''),
                father=d.get('father', ''),
                mother=d.get('mother', ''),
                dob=d.get('dob', ''),
                phone=d.get('phone', ''),
                religion=d.get('religion', ''),
                year=d.get('year', ''),
                session=d.get('session', ''),
                photo=d.get('photo', ''),
                optional_subjects=d.get('optionalSubjects', ''),
            ))
            count += 1
        except Exception as e:
            print(f"  Skipping student {d.get('id')}: {e}")
            db.session.rollback()

    db.session.commit()
    print(f"  ✓ {count} students migrated")
    return count


def migrate_teachers_from_json(data_dir):
    teachers_data = load_json_file(os.path.join(data_dir, 'teachers.json'))
    if not teachers_data:
        print("  No teachers.json found. Skipping.")
        return 0

    print(f"  Migrating {len(teachers_data)} teachers...")
    count = 0
    for d in teachers_data:
        try:
            db.session.add(Teacher(
                id=d.get('id'),
                name=d.get('name', ''),
                email=d.get('email', ''),
                phone=d.get('phone', ''),
                subject=d.get('subject', ''),
                classes=d.get('classes', '—'),
                qualification=d.get('qualification', ''),
                experience=int(d.get('experience', 0) or 0),
                empid=d.get('empid', ''),
                joining=d.get('joining', ''),
                address=d.get('address', ''),
            ))
            count += 1
        except Exception as e:
            print(f"  Skipping teacher {d.get('id')}: {e}")
            db.session.rollback()

    db.session.commit()
    print(f"  ✓ {count} teachers migrated")
    return count


def migrate_marks_from_json(data_dir):
    """Migrate marks.json → Mark rows.

    JSON format: {student_id: {exam_type: {subject_code: {cq,mcq,prac,...},
                                            selectedOptional: str}}}
    """
    marks_data = load_json_file(os.path.join(data_dir, 'marks.json'))
    if not marks_data:
        print("  No marks.json found. Skipping.")
        return 0

    print("  Migrating marks...")
    count = 0

    for student_id, exams in marks_data.items():
        for exam_type, subjects in exams.items():
            # selectedOptional is stored at the exam level, not per subject
            selected_optional = subjects.get('selectedOptional', '')

            for subject_code, mark_dict in subjects.items():
                # FIX: skip the selectedOptional key — it is not a subject entry
                if subject_code == 'selectedOptional':
                    continue

                if not isinstance(mark_dict, dict):
                    continue

                try:
                    db.session.add(Mark(
                        student_id=student_id,
                        exam_type=exam_type,
                        year=mark_dict.get('year', ''),
                        subject_code=subject_code,
                        cq=int(mark_dict.get('cq', 0) or 0),
                        mcq=int(mark_dict.get('mcq', 0) or 0),
                        prac=int(mark_dict.get('prac', 0) or 0),
                        selected_optional=selected_optional,
                    ))
                    count += 1
                except Exception as e:
                    print(f"  Skipping mark {student_id}/{exam_type}/{subject_code}: {e}")
                    db.session.rollback()

    db.session.commit()
    print(f"  ✓ {count} mark records migrated")
    return count


def migrate_settings_from_json(data_dir):
    settings_data = load_json_file(os.path.join(data_dir, 'settings.json'))
    if not settings_data:
        print("  No settings.json found. Skipping.")
        return 0

    print("  Migrating settings...")
    count = 0
    for key, value in settings_data.items():
        try:
            db.session.add(Setting(key=key, value=str(value)))
            count += 1
        except Exception as e:
            print(f"  Skipping setting {key}: {e}")
            db.session.rollback()

    db.session.commit()
    print(f"  ✓ {count} settings migrated")
    return count


def migrate_archive_from_json(data_dir):
    archive_data = load_json_file(os.path.join(data_dir, 'archive.json'))
    if not archive_data:
        print("  No archive.json found. Skipping.")
        return 0

    print(f"  Migrating {len(archive_data)} archived students...")
    count = 0
    for d in archive_data:
        try:
            db.session.add(Archive(
                id=d.get('id'),
                name=d.get('name', ''),
                roll=d.get('roll', ''),
                reg=d.get('reg', ''),
                cls=d.get('cls', ''),
                group=d.get('group', ''),
                section=d.get('section', ''),
                father=d.get('father', ''),
                mother=d.get('mother', ''),
                dob=d.get('dob', ''),
                phone=d.get('phone', ''),
                religion=d.get('religion', ''),
                year=d.get('year', ''),
                session=d.get('session', ''),
                photo=d.get('photo', ''),
                total_marks=int(d.get('total_marks', 0) or 0),
                gpa=float(d.get('gpa', 0.0) or 0.0),
            ))
            count += 1
        except Exception as e:
            print(f"  Skipping archived student {d.get('id')}: {e}")
            db.session.rollback()

    db.session.commit()
    print(f"  ✓ {count} archived students migrated")
    return count


def main():
    print("\n" + "=" * 60)
    print("  HSC Academic Management System")
    print("  Database Initialization & Migration")
    print("=" * 60 + "\n")

    with app.app_context():
        print("Creating database tables...")
        try:
            db.create_all()
            print("Tables created\n")
        except Exception as e:
            print(f"Error creating tables: {e}\n")
            return False

        inspector = inspect(db.engine)
        if 'students' in inspector.get_table_names():
            student_cols = [c['name'] for c in inspector.get_columns('students')]
            if 'optional_subjects' not in student_cols:
                print("Adding missing column optional_subjects to students table...")
                try:
                    with db.engine.begin() as conn:
                        conn.execute(text("ALTER TABLE students ADD COLUMN optional_subjects VARCHAR(50) DEFAULT ''"))
                    print("optional_subjects column added\n")
                except Exception as e:
                    print(f"Failed to add optional_subjects column: {e}\n")
                    return False

        response = input("Migrate data from JSON files (data/ folder)? (y/n): ").strip().lower()

        if response == 'y':
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            if not os.path.isdir(data_dir):
                print(f"\n  ⚠ data/ directory not found at: {data_dir}")
                print("  Skipping migration.")
            else:
                print("\nStarting migration...\n")
                migrate_students_from_json(data_dir)
                migrate_teachers_from_json(data_dir)
                migrate_marks_from_json(data_dir)
                migrate_settings_from_json(data_dir)
                migrate_archive_from_json(data_dir)
                print("\n✓ Migration complete!")
        else:
            print("\nSkipped. Database ready with empty tables.")

    print("\n" + "=" * 60)
    print("  Setup complete!  Next: python app.py")
    print("=" * 60 + "\n")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
