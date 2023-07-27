from pydantic import BaseModel
from typing import List


class Cell(BaseModel):

    row_index: int = 0
    column_index: int = 0
    words: str = ""



class Table(BaseModel):

    object_id: str
    table_index: int
    rows: int = 0
    columns: int = 0
    cells_count: int = 0
    cells: List[Cell] = list()



class Page(BaseModel):

    object_id: str
    index: int
    tables_count: int = 0
    tables: List[Table] = list()



class Document(BaseModel):

    page_count: int = 0
    pages: List[Page] = list()
