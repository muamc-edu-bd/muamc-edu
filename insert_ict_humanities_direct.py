import os
import sys
from dotenv import load_dotenv

sys.path.append(r'C:\Users\FC\OneDrive\Desktop\1234')
load_dotenv(r'C:\Users\FC\OneDrive\Desktop\1234\.env')

from app import app, db
from models import Student, Mark
from submit_ict_humanities_marks import MARKS, SUBJECT, EXAM_TYPE, YEAR

def main():
    with app.app_context():
        # Get all Humanities students
        students = Student.query.filter_by(group='Humanities').all()
        roll_to_student = {s.roll: s for s in students}
        
        print(f"Loaded {len(students)} Humanities students.")
        
        updated_count = 0
        for roll_num, (cq, mcq, absent) in MARKS.items():
            roll_str = str(roll_num)
            student = roll_to_student.get(roll_str)
            if not student:
                print(f"Skipping roll {roll_str} - student not found in Humanities group.")
                continue
            
            # Delete existing ICT mark for this student
            Mark.query.filter_by(
                student_id=student.id,
                exam_type=EXAM_TYPE,
                subject_code=SUBJECT
            ).delete()
            
            # Convert marks
            cq_val = 0 if absent else (int(cq) if cq != '' else 0)
            mcq_val = 0 if absent else (int(mcq) if mcq != '' else 0)
            prac_val = 0
            
            # Check for existing optional subject preference
            existing = Mark.query.filter_by(
                student_id=student.id,
                exam_type=EXAM_TYPE
            ).first()
            selected_optional = existing.selected_optional if existing else ''
            
            # Create and add mark row
            mark = Mark(
                student_id=student.id,
                exam_type=EXAM_TYPE,
                year=YEAR,
                subject_code=SUBJECT,
                cq=cq_val,
                mcq=mcq_val,
                prac=prac_val,
                absent=absent,
                selected_optional=selected_optional or ''
            )
            db.session.add(mark)
            updated_count += 1
            
        db.session.commit()
        print(f"Successfully inserted/updated {updated_count} marks in database.")

if __name__ == '__main__':
    main()
