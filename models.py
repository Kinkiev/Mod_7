from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


grades_m2m_students = Table(
    "grades_m2m_students",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("students", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("grades", Integer, ForeignKey("grades.id", ondelete="CASCADE")),
)

students_m2m_groups = Table(
    "students_m2m_groups",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("students", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("groups", Integer, ForeignKey("groups.id", ondelete="CASCADE")),
)

teachers_m2m_predmets = Table(
    "teachers_m2m_predmets",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("teachers", Integer, ForeignKey("teachers.id", ondelete="CASCADE")),
    Column("predmets", Integer, ForeignKey("predmets.id", ondelete="CASCADE")),
)


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_name = Column(String(50), nullable=False)
    group_id = relationship(
        "Groups",
        secondary=students_m2m_groups,
        backref="students",
        passive_deletes=True,
    )


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(50), nullable=False)
    # predmet_id = Column(Integer, ForeignKey(Predmets.id, ondelete="CASCADE"))
    predmet_id = relationship(
        "Predmets",
        secondary=teachers_m2m_predmets,
        backref="teachers",
        passive_deletes=True,
    )


class Predmets(Base):
    __tablename__ = "predmets"
    id = Column(Integer, primary_key=True)
    predmet_name = Column(String(50), nullable=False)
    # teacher_id = Column(Integer, ForeignKey(Teachers.id, ondelete="CASCADE"))
    teacher_id = relationship(
        "Teachers",
        secondary=teachers_m2m_predmets,
        backref="predmets",
        passive_deletes=True,
        overlaps="predmet_id,teachers",
    )


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Students.id, ondelete="CASCADE"))
    predmet_id = Column(Integer, ForeignKey(Predmets.id, ondelete="CASCADE"))
    created = Column(DateTime, default=datetime.now())
    grade = Column(Integer, nullable=False)
