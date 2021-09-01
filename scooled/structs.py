# structs.py

from dataclasses import dataclass
from question_bank import QuestionBank

@dataclass
class PageType:
    teacher : str = 'teacher'
    edit_pg : str = 'edit_page'
    new_pg : str = 'new_page'
    assign : str = 'assignment'
    submit : str = 'submit'
    bank : str = 'question_bank'

class PageName:
    lesson : str = "Lesson plan"
    new_assign : str = "Create a new assignment"
    status : str = "View Student Status"
    assignment : str = "View Assignment"