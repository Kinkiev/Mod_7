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

# students_m2m_groups = Table(
#     "students_m2m_groups",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("students", Integer, ForeignKey("students.id", ondelete="CASCADE")),
#     Column("groups", Integer, ForeignKey("groups.id", ondelete="CASCADE")),
# )


class StudentsGroups(Base):
    __tablename__ = "students_to_groups"
    id = Column(Integer, primary_key=True)
    students_id = Column("students_id", ForeignKey("students.id", ondelete="CASCADE"))
    groups_id = Column("groups_id", ForeignKey("groups.id", ondelete="CASCADE"))


class TeachersPredmets(Base):
    __tablename__ = "teachers_to_predmets"
    id = Column(Integer, primary_key=True)
    teachers_id = Column("teachers_id", ForeignKey("teachers.id", ondelete="CASCADE"))
    predmets_id = Column("predmets_id", ForeignKey("predmets.id", ondelete="CASCADE"))


# teachers_m2m_predmets = Table(
#     "teachers_m2m_predmets",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("teachers", Integer, ForeignKey("teachers.id", ondelete="CASCADE")),
#     Column("predmets", Integer, ForeignKey("predmets.id", ondelete="CASCADE")),
# )


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)
    students = relationship(
        "Students", secondary=students_to_groups, back_populates="groups"
    )


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_name = Column(String(50), nullable=False)
    groups = relationship(
        "Groups", secondary=students_to_groups, back_populates="students"
    )


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(100), nullable=False)
    predmets = relationship(
        "Predmets", secondary=teachers_to_predmets, back_populates="teachers"
    )


class Predmets(Base):
    __tablename__ = "predmets"
    id = Column(Integer, primary_key=True)
    predmet_name = Column(String(50), nullable=False)
    # teacher_id = Column(Integer, ForeignKey(Teachers.id, ondelete="CASCADE"))
    teachers = relationship(
        "Predmets", secondary=teachers_to_predmets, back_populates="predmets"
    )


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Students.id, ondelete="CASCADE"))
    predmet_id = Column(Integer, ForeignKey(Predmets.id, ondelete="CASCADE"))
    created = Column(DateTime, default=datetime.now())
    grade = Column(Integer, nullable=False)
