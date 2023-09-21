from sqlalchemy import *
from datetime import datetime
from sqlalchemy.orm import relationship
from core.db_connection import Base


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    token = Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, index=True)
    no = Column(Integer, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    student = relationship('Student', back_populates='group')
    
    
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    name = Column(String)
    surname = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    token = Column(String)
    group_id = Column(Integer, ForeignKey('group.id', ondelete='CASCADE'))
    in_exam = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    group = relationship("Group", cascade='all, delete', back_populates='student')
    passedExams = relationship("PassedExams", back_populates='student')
    
    
    
    
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    question = relationship("Question", back_populates='subject')
    exam_details = relationship('ExamDetails', back_populates='subject')
    
    
class Exam(Base):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    time = Column(Time)
    status = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    question = relationship("Question", back_populates='exam')
    passedExams = relationship("PassedExams", back_populates='exam')
    exam_details = relationship("ExamDetails", back_populates='exam')
    
    
class ExamDetails(Base):
    __tablename__ = 'examDetails'
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subject.id', ondelete='CASCADE'))
    question_count = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    exam = relationship("Exam", back_populates='exam_details')
    subject = relationship("Subject", back_populates='exam_details')
    
    
    
class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    correct_answer = Column(Integer)
    subject_id = Column(Integer, ForeignKey('subject.id', ondelete='CASCADE'))
    exam_id = Column(Integer, ForeignKey('exam.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    
    subject = relationship('Subject', cascade='all, delete', back_populates='question')
    exam = relationship('Exam', back_populates='question')
    
    

class PassedExams(Base):
    __tablename__ = 'passed_exams'
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey('exam.id'))
    student_id = Column(Integer, ForeignKey('student.id'))
    mark = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
    exam = relationship('Exam', back_populates='passedExams')
    student = relationship('Student', back_populates='passedExams')
    