from connect_db import session
from models import Students, Teachers, Groups, Grades, Predmets

if __name__ == "__main__":
    st1 = Students(student_name="John Dow")
    st2 = Students(student_name="John Wayne")
    st3 = Students(student_name="Indiana Jones")
    st4 = Students(student_name="Dandy Crocodile")

    gr1 = Groups(group_name="Lions")
    gr2 = Groups(group_name="Tigers")

    te1 = Teachers(teacher_name="Sergey Ivanovich")
    te2 = Teachers(teacher_name="Maria Petrovna")

    pr1 = Predmets(predmet_name="math")
    pr2 = Predmets(predmet_name="eng")
    pr3 = Predmets(predmet_name="chem")

    session.add(st1)
    session.add(st2)
    session.add(st3)
    session.add(st4)

    session.add(gr1)
    session.add(gr2)

    session.add(te1)
    session.add(te2)

    session.add(pr1)
    session.add(pr2)
    session.add(pr3)

    session.commit()
