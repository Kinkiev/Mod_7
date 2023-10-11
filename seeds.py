from connect_db import session
from models import Students, Teachers, Groups, Grades, Predmets
import faker
from datetime import datetime
from random import randint

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 15
NUMBER_PREDMETS = 5
NUMBER_TEACHERS = 5


def generate_fake_data(
    number_groups, number_students, number_predmets, number_teachers
) -> tuple():
    fake_groups = []  # тут зберігатимемо групи
    fake_students = []  # тут зберігатимемо студентів
    fake_predmets = []  # тут зберігатимемо предмети
    fake_teachers = []  # тут зберігатимемо вчителів

    fake_data = faker.Faker()

    for _ in range(number_groups):
        fake_groups.append(fake_data.country())

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_predmets):
        fake_predmets.append(fake_data.city())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    return fake_groups, fake_students, fake_predmets, fake_teachers


def prepare_data(groups, students, predmets, teachers) -> tuple():
    for_groups = []

    for group in groups:
        for_groups.append((group,))

    for_students = []

    for stud in students:
        for_students.append((stud, randint(1, NUMBER_GROUPS)))

    for_teachers = []

    for teach in teachers:
        for_teachers.append((teach, randint(1, NUMBER_PREDMETS)))

    for_predmets = []

    for pred in predmets:
        for_predmets.append((pred, randint(1, NUMBER_TEACHERS)))

    for_grades = []

    for stud in range(1, NUMBER_STUDENTS + 1):
        grade_date = datetime(2023, randint(1, 12), randint(1, 28)).date()

        for_grades.append(
            (stud, randint(1, NUMBER_PREDMETS), grade_date, randint(1, 10))
        )

    return for_groups, for_students, for_teachers, for_predmets, for_grades


if __name__ == "__main__":
    groups, students, predmets, teachers, grades = prepare_data(
        *generate_fake_data(
            NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_PREDMETS, NUMBER_TEACHERS
        )
    )

    fake_groups = [group[0] for group in groups]
    fake_students = [student[0] for student in students]
    fake_predmets = [predmet[0] for predmet in predmets]
    fake_teachers = [teacher[0] for teacher in teachers]

    for group_name in fake_groups:
        new_group = Groups(group_name=group_name)
        session.add(new_group)

    for student_name, group_id in zip(fake_students, range(1, len(groups) + 1)):
        new_student = Students(student_name=student_name, group_id=group_id)
        session.add(new_student)

    for predmet_name, teacher_id in zip(fake_predmets, range(1, len(teachers) + 1)):
        new_predmet = Predmets(predmet_name=predmet_name, teacher_id=teacher_id)
        session.add(new_predmet)

    for teacher_name, predmet_id in zip(fake_teachers, range(1, len(predmets) + 1)):
        new_teacher = Teachers(teacher_name=teacher_name, predmet_id=predmet_id)
        session.add(new_teacher)

    for student_id, predmet_id, created, grade in grades:
        new_grade = Grades(
            student_id=student_id, predmet_id=predmet_id, created=created, grade=grade
        )
        session.add(new_grade)

    session.commit()
