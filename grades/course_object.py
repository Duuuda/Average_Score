class Course:
    def __init__(self, name: str):
        self.__is_variable = True
        self.name = name
        self.middle = float()
        self.__is_variable = False

    def __eq__(self, other):
        return self.name == other

    def __bool__(self):
        return bool(self.name)

    def __len__(self):
        return len(self.all_grades)

    def __repr__(self):
        description = f"<Course(name='{self.name}'"
        grades = self.all_grades
        for attrib in grades:
            description += f', {attrib}={grades[attrib]}'
        return description + f', middle={self.middle})>'

    def __setattr__(self, key, value):
        if key != '_Course__is_variable' and not self.__is_variable:
            raise AttributeError("can't set this attribute")
        super().__setattr__(key, value)

    @property
    def all_grades(self):
        return {attr: getattr(self, attr) for attr in self.__dir__() if 'test' in attr}

    def _add_grade(self, test_num: str, grade: float):
        self.__is_variable = True
        setattr(self, f'test_{test_num}', grade)
        self.middle = self.__get_middle
        self.__is_variable = False

    @property
    def __get_middle(self):
        grades = self.all_grades.values()
        length = len(grades)
        if length:
            return sum(grades) / length
        return 0
