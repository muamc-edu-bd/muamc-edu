"""
Database Models for HSC Academic Management System
Uses PostgreSQL with SQLAlchemy ORM
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import deferred

db = SQLAlchemy()


class Student(db.Model):
    """Active student information."""
    __tablename__ = 'students'

    id       = db.Column(db.String(50),  primary_key=True)
    name     = db.Column(db.String(255), nullable=False)
    roll     = db.Column(db.String(50),  nullable=False)
    reg      = db.Column(db.String(50),  default='')
    cls      = db.Column(db.String(50),  nullable=False)   # Class-XI / Class-XII
    group    = db.Column(db.String(50),  nullable=False)   # Science / Humanities / Business
    section  = db.Column(db.String(50),  default='')
    father   = db.Column(db.String(255), default='')
    mother   = db.Column(db.String(255), default='')
    dob      = db.Column(db.String(50),  default='')
    phone    = db.Column(db.String(20),  default='')
    religion = db.Column(db.String(50),  default='')
    year     = db.Column(db.String(10),  default='')
    session  = db.Column(db.String(50),  default='')
    photo    = db.Column(db.Text, default='')             # Stored as base64 data URL or filepath
    photo_base64 = deferred(db.Column(db.Text, default=''))
    optional_subjects = db.Column(db.String(50), default='')  # e.g. '178/179'
    humanities_main_subjects = db.Column(db.String(100), default='')  # Humanities only: e.g. '269/109/116'
    student_submitted = db.Column(db.Boolean, default=False)  # True once student self-submits via portal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Cascade-delete marks when student is deleted
    marks = db.relationship('Mark', backref='student', lazy=True,
                            cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'roll':      self.roll,
            'reg':       self.reg,
            'cls':       self.cls,
            'group':     self.group,
            'section':   self.section,
            'father':    self.father,
            'mother':    self.mother,
            'dob':       self.dob,
            'phone':     self.phone,
            'religion':  self.religion,
            'year':      self.year,
            'session':   self.session,
            'photo':            self.photo,
            'optionalSubjects':  self.optional_subjects,
            'humanitiesMainSubjects': self.humanities_main_subjects or '',
            'studentSubmitted':  self.student_submitted or False,
            'createdAt':         self.created_at.strftime('%d/%m/%Y') if self.created_at else '',
        }


class Mark(db.Model):
    """Student marks for a specific exam and subject.

    Hierarchical key structure (mirrored in app helpers):
        marks[student_id][exam_type][subject_code] = {cq, mcq, prac, ey, examType, year}
    The selectedOptional field is stored redundantly on every Mark row for that exam.
    """
    __tablename__ = 'marks'
    __table_args__ = (
        db.Index('ix_marks_student_exam',    'student_id', 'exam_type'),
        db.Index('ix_marks_student_subject', 'student_id', 'subject_code'),
        db.Index('ix_marks_exam_subject',    'exam_type',  'subject_code'),
    )

    id                = db.Column(db.Integer,     primary_key=True)
    student_id        = db.Column(db.String(50),  db.ForeignKey('students.id'), nullable=False)
    exam_type         = db.Column(db.String(100), nullable=False)   # e.g. "First Terminal"
    year              = db.Column(db.String(10),  nullable=False)
    subject_code      = db.Column(db.String(50),  nullable=False)   # e.g. "101"
    cq                = db.Column(db.Integer,     default=0)
    mcq               = db.Column(db.Integer,     default=0)
    prac              = db.Column(db.Integer,     default=0)
    absent            = db.Column(db.Boolean,     default=False)  # True when teacher marks student as absent
    selected_optional = db.Column(db.String(50),  default='')
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'cq':       self.cq,
            'mcq':      self.mcq,
            'prac':     self.prac,
            'absent':   self.absent or False,
            'ey':       self.year,
            'examType': self.exam_type,
            'year':     self.year,
        }


class Teacher(db.Model):
    """Teacher / faculty information."""
    __tablename__ = 'teachers'

    id            = db.Column(db.String(50),  primary_key=True)
    name          = db.Column(db.String(255), nullable=False)
    email         = db.Column(db.String(100), nullable=False)
    phone         = db.Column(db.String(20),  nullable=False)
    subject       = db.Column(db.String(100), nullable=False)
    classes       = db.Column(db.String(255), default='—')   # comma-separated
    qualification = db.Column(db.String(255), nullable=False)
    experience    = db.Column(db.Integer,     default=0)     # years
    empid         = db.Column(db.String(50),  default='')
    joining       = db.Column(db.String(50),  default='')
    address       = db.Column(db.Text,        default='')
    added_date    = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':            self.id,
            'name':          self.name,
            'email':         self.email,
            'phone':         self.phone,
            'subject':       self.subject,
            'classes':       self.classes,
            'qualification': self.qualification,
            'experience':    self.experience,
            'empid':         self.empid,
            'joining':       self.joining,
            'address':       self.address,
            'addedDate':     self.added_date.strftime('%d/%m/%Y') if self.added_date else '',
        }


class Setting(db.Model):
    """Application settings stored as key-value pairs."""
    __tablename__ = 'settings'

    id    = db.Column(db.Integer,    primary_key=True)
    key   = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)

    def to_dict(self):
        return {'key': self.key, 'value': self.value}


class Archive(db.Model):
    """Archived (graduated) students."""
    __tablename__ = 'archive'

    id          = db.Column(db.String(50),  primary_key=True)
    name        = db.Column(db.String(255), nullable=False)
    roll        = db.Column(db.String(50),  nullable=False)
    reg         = db.Column(db.String(50),  default='')
    cls         = db.Column(db.String(50),  nullable=False)
    group       = db.Column(db.String(50),  nullable=False)
    section     = db.Column(db.String(50),  default='')
    father      = db.Column(db.String(255), default='')
    mother      = db.Column(db.String(255), default='')
    dob         = db.Column(db.String(50),  default='')
    phone       = db.Column(db.String(20),  default='')
    religion    = db.Column(db.String(50),  default='')
    year        = db.Column(db.String(10),  default='')
    session     = db.Column(db.String(50),  default='')
    photo       = db.Column(db.Text, default='')
    photo_base64 = deferred(db.Column(db.Text, default=''))
    total_marks = db.Column(db.Integer,     default=0)
    gpa         = db.Column(db.Float,       default=0.0)
    archived_at = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'roll':        self.roll,
            'reg':         self.reg,
            'cls':         self.cls,
            'group':       self.group,
            'section':     self.section,
            'father':      self.father,
            'mother':      self.mother,
            'dob':         self.dob,
            'phone':       self.phone,
            'religion':    self.religion,
            'year':        self.year,
            'session':     self.session,
            'photo':       self.photo,
            'total_marks': self.total_marks,
            'gpa':         self.gpa,
            'archived_at': self.archived_at.isoformat() + 'Z' if self.archived_at else '',
        }


class PromotionLog(db.Model):
    """Audit trail for Class-XI → Class-XII promotions."""
    __tablename__ = 'promotion_logs'

    id          = db.Column(db.Integer,     primary_key=True)
    student_id  = db.Column(db.String(50),  nullable=False)
    name        = db.Column(db.String(255), nullable=False)
    old_roll    = db.Column(db.String(50),  default='')
    new_roll    = db.Column(db.String(50),  nullable=False)
    gpa         = db.Column(db.Float,       default=0.0)
    total_marks = db.Column(db.Integer,     default=0)
    promoted_at = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            'student_id':  self.student_id,
            'name':        self.name,
            'old_roll':    self.old_roll,
            'new_roll':    self.new_roll,
            'gpa':         self.gpa,
            'total_marks': self.total_marks,
            'promoted_at': self.promoted_at.isoformat() + 'Z' if self.promoted_at else '',
        }


class AdmissionApplication(db.Model):
    """Student admission applications before approval."""
    __tablename__ = 'admission_applications'

    id                       = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    application_no           = db.Column(db.String(50),  unique=True, nullable=False, index=True)
    
    # Core Student fields (for transfer to Student table upon approval)
    name                     = db.Column(db.String(255), nullable=False)
    roll                     = db.Column(db.String(50),  default='')
    reg                      = db.Column(db.String(50),  default='')
    cls                      = db.Column(db.String(50),  nullable=False)   # Class-XI / Class-XII
    group                    = db.Column(db.String(50),  nullable=False)   # Science / Humanities / Business
    section                  = db.Column(db.String(50),  default='')
    father                   = db.Column(db.String(255), default='')
    mother                   = db.Column(db.String(255), default='')
    dob                      = db.Column(db.String(50),  default='')
    phone                    = db.Column(db.String(20),  default='')
    religion                 = db.Column(db.String(50),  default='')
    year                     = db.Column(db.String(10),  default='')
    session                  = db.Column(db.String(50),  default='')
    photo                    = db.Column(db.Text,        default='')
    photo_base64             = deferred(db.Column(db.Text, default=''))
    optional_subjects        = db.Column(db.String(50),  default='')
    humanities_main_subjects = db.Column(db.String(100), default='')

    # Additional admission details
    gender                   = db.Column(db.String(20),  default='')
    blood_group              = db.Column(db.String(10),  default='')
    nationality              = db.Column(db.String(50),  default='Bangladeshi')
    address                  = db.Column(db.Text,        default='')
    guardian_name            = db.Column(db.String(255), default='')
    guardian_phone           = db.Column(db.String(20),  default='')
    ssc_roll                 = db.Column(db.String(50),  default='')
    ssc_reg                  = db.Column(db.String(50),  default='')
    ssc_board                = db.Column(db.String(50),  default='')
    ssc_gpa                  = db.Column(db.String(10),  default='')
    ssc_passing_year         = db.Column(db.String(10),  default='')
    ssc_group                = db.Column(db.String(50),  default='')

    # Status & workflow
    status                   = db.Column(db.String(20),  default='pending')  # pending / approved / rejected
    admin_remarks            = db.Column(db.Text,        default='')
    approved_student_id      = db.Column(db.String(50),  default='')
    submitted_at             = db.Column(db.DateTime,    default=datetime.utcnow)
    reviewed_at              = db.Column(db.DateTime,    nullable=True)

    def to_dict(self):
        return {
            'id':                     self.id,
            'applicationNo':          self.application_no,
            'name':                   self.name,
            'roll':                   self.roll or '',
            'reg':                    self.reg or '',
            'cls':                    self.cls,
            'group':                  self.group,
            'section':                self.section or '',
            'father':                 self.father or '',
            'mother':                 self.mother or '',
            'dob':                    self.dob or '',
            'phone':                  self.phone or '',
            'religion':               self.religion or '',
            'year':                   self.year or '',
            'session':                self.session or '',
            'photo':                  self.photo or '',
            'optionalSubjects':       self.optional_subjects or '',
            'humanitiesMainSubjects': self.humanities_main_subjects or '',
            'gender':                 self.gender or '',
            'bloodGroup':             self.blood_group or '',
            'nationality':            self.nationality or 'Bangladeshi',
            'address':                self.address or '',
            'guardianName':           self.guardian_name or '',
            'guardianPhone':          self.guardian_phone or '',
            'sscRoll':                self.ssc_roll or '',
            'sscReg':                 self.ssc_reg or '',
            'sscBoard':               self.ssc_board or '',
            'sscGpa':                 self.ssc_gpa or '',
            'sscPassingYear':         self.ssc_passing_year or '',
            'sscGroup':               self.ssc_group or '',
            'status':                 self.status or 'pending',
            'adminRemarks':           self.admin_remarks or '',
            'approvedStudentId':      self.approved_student_id or '',
            'submittedAt':            self.submitted_at.strftime('%d/%m/%Y %I:%M %p') if self.submitted_at else '',
            'reviewedAt':             self.reviewed_at.strftime('%d/%m/%Y %I:%M %p') if self.reviewed_at else '',
        }

