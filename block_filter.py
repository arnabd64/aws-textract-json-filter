from datastructures import Cell, Table, Page, Document




class Blocks:

    ids = dict(
        PAGE  = list(),
        TABLE = list(),
        CELL  = list(),
        WORD  = list()
    )

    _OBJECTS = {"WORD", "CELL", "TABLE", "PAGE"}


    def __init__(self, response):
        self.blocks = response

        for block in self.blocks:
            if block["BlockType"] in self._OBJECTS:
                self.ids[block["BlockType"]].append(block["Id"])


    def _getChildIds(self, parent_id: str, child: str):
        childIds = list()

        for block in self.blocks:
            if block["Id"] == parent_id and "Relationships" in block:
                childIds = block["Relationships"][0]["Ids"]
                childIds = [item for item in self.ids[child] if item in childIds]

        return childIds
    

    def _getBlockProperty(self, block_id: str, property: str):
        for block in self.blocks:
            if block["Id"] == block_id and property in block:
                return block[property]

        return None



    def getRelationMap(self):
        # create a document object
        document = Document()

        # Add pages
        for page_idx, page_id in enumerate(self.ids['PAGE'], 1):
            # create candidate object 
            _page = Page(object_id = page_id, index = page_idx)

            # add tables
            for table_idx, table_id in enumerate(self._getChildIds(page_id, 'TABLE'), 1):
                # candidate table object
                _table = Table(object_id = table_id, table_index = table_idx)
                
                # add cells
                for cell_idx, cell_id in enumerate(self._getChildIds(table_id, 'CELL'), 1):
                    # candidate cell object
                    _cell = Cell(row_index=0, column_index=0, words="")

                    # add words
                    _text = list()
                    for word_idx, word_id in enumerate(self._getChildIds(cell_id, 'WORD'), 1):
                        _text.append(self._getBlockProperty(word_id, "Text"))
                    _cell.words = " ".join(_text)
                    
                    # add other properties
                    _cell.row_index = self._getBlockProperty(cell_id, "RowIndex")
                    _cell.column_index = self._getBlockProperty(cell_id, "ColumnIndex")

                    # add cell to table
                    _table.cells.append(_cell)
                    _table.cells_count += 1

                # add table to page
                _page.tables.append(_table)
                _page.tables_count += 1

            # add page to Document
            document.pages.append(_page)
            document.page_count += 1

        return document.model_dump()
    