import pprint


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = float()

    def rate_lr(self, lecturer, course, grade):
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            if course in lecturer.lr_grades:
                lecturer.lr_grades[course] += [grade]
            else:
                lecturer.lr_grades[course] = [grade]
        else:
            return "Ошибка"

    def avg_grade(self):
        sum_grades = 0
        for grades in self.grades.values():
            sum_grades += sum(grades) / len(grades)
            self.average_grade = sum_grades
        return round(self.average_grade, 1)

    def __str__(self):
        courses_in_progress_string = ", ".join(self.courses_in_progress)
        finished_courses_string = ", ".join(self.finished_courses)
        return f"Имя: {self.name} \nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.avg_grade()}\nКурсы в процессе обучения: {courses_in_progress_string}\nЗавершенные курсы: {finished_courses_string}"

    def __lt__(self, other):
        if not isinstance(other, Student):
            print("Кто-то здесь не студент")
            return
        return self.average_grade < other.average_grade


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lr_grades = {}
        self.average_lr_grades = float()

    def avg_grade(self):
        sum_grades = 0
        for grades in self.lr_grades.values():
            sum_grades += sum(grades) / len(grades)
        self.average_lr_grades = sum_grades
        return round(self.average_lr_grades, 1)

    def __str__(self):
        return f"Имя: {self.name} \nФамилия: {self.surname}\nСредняя оценка за лекции: {self.avg_grade()}"

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print("Кто-то здесь не лектор")
            return
        return self.average_lr_grades < other.average_lr_grades


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"

    def __str__(self):
        return f"Имя: {self.name} \nФамилия: {self.surname}"


def avg_students_grades_by_course(students, course):
    grades_list = []
    for student in students:
        if student.courses_in_progress == [course]:
            grades_list += student.grades.get(course)
    return sum(grades_list) / len(grades_list)


def avg_lecturers_grades_by_course(lecturers, course):
    grades_list = []
    for lecturer in lecturers:
        if lecturer.courses_attached == [course]:
            grades_list += lecturer.lr_grades.get(course)
    return sum(grades_list) / len(grades_list)


best_student = Student("Ruoy", "Eman", "your_gender")
best_student.courses_in_progress += ["Python"]
best_student.finished_courses = ["Введение в программирование"]

good_student = Student("R2", "D2", "your_gender")
good_student.courses_in_progress += ["Python"]

cool_mentor = Reviewer("Some", "Buddy")
cool_mentor.courses_attached += ["Python"]

cool_mentor.rate_hw(best_student, "Python", 10)
cool_mentor.rate_hw(best_student, "Python", 10)
cool_mentor.rate_hw(best_student, "Python", 10)
cool_mentor.rate_hw(good_student, "Python", 8)


cool_lecturer = Lecturer("NamLr1", "SurLr1")
cool_lecturer.courses_attached += ["Python"]

lecturer2 = Lecturer("NamLr2", "SurLr2")
lecturer2.courses_attached += ["Python"]

best_student.rate_lr(cool_lecturer, "Python", 10)
best_student.rate_lr(cool_lecturer, "Python", 9)
best_student.rate_lr(cool_lecturer, "Python", 8)
best_student.rate_lr(lecturer2, "Python", 9)

print(cool_mentor)
print()
print(cool_lecturer)
print()
print(lecturer2)
print()
print(best_student)
print()
print(good_student)
print()


print("Сравниваем двух студентов", best_student > good_student)
print("Сравниваем двух лекторов", cool_lecturer > lecturer2)

students = [best_student, good_student]
print(
    "Средняя оценка за домашние задания по всем студентам в рамках конкретного курса:",
    round(avg_students_grades_by_course(students, "Python"), 1),
)

lecturers = [cool_lecturer, lecturer2]
print(
    "Средняя оценка за лекции всех лекторов в рамках курса",
    round(avg_lecturers_grades_by_course(lecturers, "Python"), 1),
)
