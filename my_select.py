from sqlalchemy import func, desc, and_
from connect_db import session
from models import Students, Teachers, Groups, Grades, Predmets


def select_1():
    return (
        session.query(
            Students.student_name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .group_by(Students.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(subj):
    result = (
        session.query(
            Students.student_name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .join(Predmets)
        .filter(Predmets.predmet_name == subj)
        .group_by(Students.id)
        .order_by(desc("avg_grade"))
        .limit(1)
        .first()
    )
    if result:
        print(
            f"Top student for {subj}: {result.student_name}, Average Grade: {result.avg_grade}"
        )
    else:
        print(f"No data found for {subj}")


def select_3(subj):
    result = (
        session.query(
            Groups.group_name, func.round(func.avg(Grades.grade), 2).label("avg_grade")
        )
        .select_from(Grades)
        .join(Students)
        .join(Predmets)
        .join(Groups)
        .filter(Predmets.predmet_name == subj)
        .group_by(Groups.group_name)
        .all()
    )
    if result:
        for row in result:
            print(f"Group: {row.group_name}, Average Grade for {subj}: {row.avg_grade}")
    else:
        print(f"No data found for {subj}")


def select_4():
    avg_grade = session.query(func.avg(Grades.grade)).scalar()
    print(f"Середній бал на потоці: {avg_grade:.2f}")


def select_5(teacher_name):
    courses = (
        session.query(Predmets.predmet_name)
        .join(Teachers)
        .filter(Teachers.teacher_name == teacher_name)
        .all()
    )

    if not courses:
        print(f"{teacher_name} не викладає жодного курсу.")
    else:
        print(f"{teacher_name} викладає наступні курси:")
        for course in courses:
            print(course[0])


def select_6(group_name):
    students = (
        session.query(Students.student_name)
        .join(Groups)
        .filter(Groups.group_name == group_name)
        .all()
    )

    if not students:
        print(f"У групі {group_name} немає студентів.")
    else:
        print(f"Студенти у групі {group_name}:")
        for student in students:
            print(student[0])


def select_7(group_name, teacher_name):  # не по предмету а по викладачу
    query = (
        session.query(Students.student_name, Grades.grade)
        .join(Groups)
        .join(Teachers)
        .filter(Groups.group_name == group_name, Teachers.teacher_name == teacher_name)
        .all()
    )

    if not query:
        print(f"В групі {group_name} не знайдено оцінок у викладача {teacher_name}.")
    else:
        print(f"Оцінки студентів у групі {group_name} у викладача {teacher_name}:")
        for student_name, grade in query:
            print(f"{student_name}: {grade}")


def select_8(teacher_name):
    query = (
        session.query(
            Predmets.predmet_name,
            func.round(func.avg(Grades.grade), 2).label("average_grade"),
        )
        .join(Teachers)
        .join(Grades)
        .filter(Teachers.teacher_name == teacher_name)
        .group_by(Predmets.predmet_name)
        .all()
    )

    if not query:
        print(
            f"Викладача {teacher_name} не знайдено або він не має оцінок з жодного предмету."
        )
    else:
        print(
            f"Середній бал, який ставить викладач {teacher_name}, зі своїх предметів:"
        )
        for predmet_name, average_grade in query:
            print(f"Предмет: {predmet_name}, Середній бал: {average_grade}")


def select_9(student_name):
    query = (
        session.query(Students.student_name, Predmets.predmet_name)
        .join(Grades, Students.id == Grades.student_id)
        .join(Predmets, Grades.predmet_id == Predmets.id)
        .filter(Students.student_name == student_name)
        .all()
    )

    if not query:
        print(
            f"Студента {student_name} не знайдено або він не має оцінок з жодного предмету."
        )
    else:
        print(f"Список курсів, які відвідує студент {student_name}:")
        for course in query:
            print(course[1])


def select_10(student_name, teacher_name):
    query = (
        session.query(Students.student_name, Predmets.predmet_name)
        .join(Grades, Students.id == Grades.student_id)
        .join(Predmets, Grades.predmet_id == Predmets.id)
        .join(Teachers, Predmets.teacher_id == Teachers.id)
        .filter(
            and_(
                Students.student_name == student_name,
                Teachers.teacher_name == teacher_name,
            )
        )
        .all()
    )

    if not query:
        print(f"Студент {student_name} не відвідує курси від викладача {teacher_name}.")
    else:
        print(
            f"Список курсів, які студент {student_name} відвідує у викладача {teacher_name}:"
        )
        for course in query:
            print(course[1])


if __name__ == "__main__":
    sel1 = select_1()
    for row in sel1:
        print(f"Student: {row.student_name}, Average Grade: {row.avg_grade}")
    print()
    select_2("Richard Newman")
    print()
    select_3("Richard Newman")
    print()
    select_4()
    print()
    select_5("Richardsbury")
    print()
    select_6("Oman")
    print()
    select_7("Oman", "Ramirezville")
    print()
    select_8("Warrentown")
    print()
    select_9("David Perkins")
    print()
    select_10("David Perkins", "Richardsbury")
