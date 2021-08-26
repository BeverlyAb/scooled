# structs.py

from dataclasses import dataclass

@dataclass
class PageType:
    teacher : str = 'teacher'
    edit_pg : str = 'edit_page'
    new_pg : str = 'new_page'