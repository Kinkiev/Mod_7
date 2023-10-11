from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(100), nullable=False)


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey(Groups.id, ondelete="CASCADE"))


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(100), nullable=False)
    predmet_id = Column(Integer, ForeignKey(Groups.id, ondelete="CASCADE"))


class Predmets(Base):
    __tablename__ = "predmets"
    id = Column(Integer, primary_key=True)
    predmet_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teachers.id, ondelete="CASCADE"))


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Students.id, ondelete="CASCADE"))
    predmet_id = Column(Integer, ForeignKey(Predmets.id, ondelete="CASCADE"))
    created = Column(Date, nullable=False)
    grade = Column(Integer, nullable=False)
