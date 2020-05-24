from grades import Grades


if __name__ == '__main__':
    login = input('Введите логин пользователя: ')
    password = input('Введите пароль пользователя: ')
    grades = Grades(login, password)
    for grade in grades:
        print(f'{grade.name:.<50}.{str(grade.all_grades).strip("{}")}, middle: {grade.middle}')
    input()
