from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 1)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_grade()}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 1)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_grade()}')

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


# --- Задание 4: полевые испытания ---
def average_hw_grade(students, course):
    """Средняя оценка за ДЗ по всем студентам в рамках одного курса."""
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades += student.grades[course]
    if not all_grades:
        return f'Ни у кого нет оценок по курсу {course}'
    return round(sum(all_grades) / len(all_grades), 1)
 
 
def average_lecture_grade(lecturers, course):
    """Средняя оценка за лекции по всем лекторам в рамках одного курса."""
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades += lecturer.grades[course]
    if not all_grades:
        return f'Ни у кого нет оценок по курсу {course}'
    return round(sum(all_grades) / len(all_grades), 1)
 
 

 
# по два экземпляра каждого класса
student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_2 = Student('Иван', 'Смирнов', 'М')
lecturer_1 = Lecturer('Сергей', 'Сергеев')
lecturer_2 = Lecturer('Анна', 'Кузнецова')
reviewer_1 = Reviewer('Пётр', 'Петров')
reviewer_2 = Reviewer('Мария', 'Орлова')
 
# распределяем курсы
student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Введение в программирование']
student_2.courses_in_progress += ['Python', 'Git']
student_2.finished_courses += ['Введение в программирование']
 
lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2.courses_attached += ['Python', 'Git']
reviewer_1.courses_attached += ['Python']
reviewer_2.courses_attached += ['Git']
 
# студенты оценивают лекции
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)
student_1.rate_lecture(lecturer_2, 'Python', 8)
student_2.rate_lecture(lecturer_1, 'Python', 9)
student_2.rate_lecture(lecturer_2, 'Python', 7)
student_2.rate_lecture(lecturer_2, 'Git', 10)
 
# проверяющие оценивают домашки
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_2, 'Python', 8)
reviewer_2.rate_hw(student_1, 'Git', 9)
reviewer_2.rate_hw(student_2, 'Git', 7)
reviewer_2.rate_hw(student_2, 'Git', 8)
 
# ошибочные вызовы: курс не тот / объект не того класса
print(reviewer_1.rate_hw(student_1, 'Git', 10))        # Ошибка — Git не закреплён за reviewer_1
print(student_1.rate_lecture(reviewer_1, 'Python', 5))  # Ошибка — reviewer не лектор
print()
 
# __str__ всех классов
print(student_1, '\n')
print(student_2, '\n')
print(lecturer_1, '\n')
print(lecturer_2, '\n')
print(reviewer_1, '\n')
print(reviewer_2, '\n')
 
# сравнение через операторы
print('Студенты:')
print(f'{student_1.surname} > {student_2.surname}: {student_1 > student_2}')
print(f'{student_1.surname} == {student_2.surname}: {student_1 == student_2}')
print('Лекторы:')
print(f'{lecturer_1.surname} > {lecturer_2.surname}: {lecturer_1 > lecturer_2}')
print(f'{lecturer_1.surname} <= {lecturer_2.surname}: {lecturer_1 <= lecturer_2}')
print()
 
# средние оценки по курсам
students = [student_1, student_2]
lecturers = [lecturer_1, lecturer_2]
 
for course in ['Python', 'Git', 'C++']:
    print(f'Средняя оценка за ДЗ по курсу {course}: {average_hw_grade(students, course)}')
for course in ['Python', 'Git', 'C++']:
    print(f'Средняя оценка за лекции по курсу {course}: {average_lecture_grade(lecturers, course)}')