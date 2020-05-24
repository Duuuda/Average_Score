from requests import get
from re import search
from grades import Course


DOMAIN = 'https://e.muiv.ru/'


class Getter:
    def __init__(self, login: str, password: str):
        self.token = self.__get_token(login, password)
        self.user_id = self.__get_user_id
        self._courses = self.__get_courses
        self._grades = self.__get_grades

    @staticmethod
    def __get_token(login, password):
        token_url = f'{DOMAIN}login/token.php?username={login}&password={password}&service=moodle_mobile_app'
        return get(token_url).json()['token']

    @property
    def __get_user_id(self):
        user_id_url = f'https://e.muiv.ru/webservice/rest/server.php?moodlewsrestformat=json&wsfunction=' +\
                      f'core_webservice_get_site_info&wstoken={self.token}'
        return get(user_id_url).json()['userid']

    @property
    def __get_courses(self):
        courses_url = f'{DOMAIN}webservice/rest/server.php?moodlewsrestformat=json&wsfunction=' +\
                      f'core_enrol_get_users_courses&wstoken={self.token}&userid={self.user_id}'
        return get(courses_url).json()

    @property
    def __get_grades(self):
        grades_url = f'{DOMAIN}webservice/rest/server.php?moodlewsrestformat=json&wsfunction=' +\
                     f'gradereport_overview_get_course_grades&wstoken={self.token}'
        return get(grades_url).json()['grades']


class Grades(Getter):
    def __init__(self, login: str, password: str):
        super().__init__(login, password)
        self._courses = {course['id']: course['displayname'] for course in self._courses}
        self._grades = {grade['courseid']: grade['rawgrade'] for grade in self._grades if grade['rawgrade'] is not None}
        self.__all_grades: list = self.__handle_grades_data

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.__all_grades[item]
        if isinstance(item, str):
            return self.__all_grades[self.__all_grades.index(item)]
        raise TypeError(f'Grades indices must be integers, strings or slices, not {str(type(item))}')

    def __delitem__(self, key):
        if isinstance(key, (int, slice)):
            del self.__all_grades[key]
            return
        if isinstance(key, str):
            del self.__all_grades[self.__all_grades.index(key)]
            return
        raise TypeError(f'Grades indices must be integers, strings or slices, not {str(type(key))}')

    def __repr__(self):
        return str(self.__all_grades)

    @property
    def __handle_grades_data(self):
        grades_data = list()
        for course_id in self._courses:
            grade = self._grades.get(course_id)
            if grade is not None:
                course_name = search(r'\D+', self._courses[course_id]).group()
                test_num = search(r'\d+', self._courses[course_id]).group()
                if course_name in grades_data:
                    grades_data[grades_data.index(course_name)]._add_grade(test_num, float(grade))
                else:
                    new_course = Course(course_name)
                    new_course._add_grade(test_num, float(grade))
                    grades_data.append(new_course)
        del self._courses, self._grades
        return grades_data
