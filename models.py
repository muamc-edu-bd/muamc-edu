"""
Database Models for HSC Academic Management System
Uses PostgreSQL with SQLAlchemy ORM
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):
    """Active student information."""
    __tablename__ = 'students'

    id       = db.Column(db.String(50),  primary_key=True)
    name     = db.Column(db.String(255), nullable=False)
    roll     = db.Column(db.String(50),  nullable=False, unique=True)
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
    photo    = db.Column(db.String(500), default='')       # e.g. /photos/abc.jpg
    optional_subjects = db.Column(db.String(50), default='')  # e.g. '178/179'
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

    id                = db.Column(db.Integer,     primary_key=True)
    student_id        = db.Column(db.String(50),  db.ForeignKey('students.id'), nullable=False)
    exam_type         = db.Column(db.String(100), nullable=False)   # e.g. "First Terminal"
    year              = db.Column(db.String(10),  nullable=False)
    subject_code      = db.Column(db.String(50),  nullable=False)   # e.g. "101"
    cq                = db.Column(db.Integer,     default=0)
    mcq               = db.Column(db.Integer,     default=0)
    prac              = db.Column(db.Integer,     default=0)
    selected_optional = db.Column(db.String(50),  default='')
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'cq':       self.cq,
            'mcq':      self.mcq,
            'prac':     self.prac,
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
    photo       = db.Column(db.String(500), default='')
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
