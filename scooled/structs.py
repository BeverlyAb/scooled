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
    add : str = "Add lesson plan"
    new : str = "Create a new assignment"
    status : str = "View Student Status"
    edit : str = "Edit Assignment"