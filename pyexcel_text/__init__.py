#from pyexcel.io import READERS
#from pyexcel.io import WRITERS
#
#READERS["test"] = "test"
#WRITERS["test"] = "test"
from pyexcel.presentation import STRINGIFICATION


TABLEFMT="simple"


def present_matrix(matrix_instance):
    import tabulate
    return tabulate.tabulate(matrix_instance.to_array(), tablefmt=TABLEFMT)

    
def present_nominable_sheet(nmsheet_instance):
    import tabulate
    ret = "Sheet Name: %s\n" % nmsheet_instance.name
    if len(nmsheet_instance.colnames) > 0:
        data = nmsheet_instance.to_array()
        return ret+tabulate.tabulate(data, headers="firstrow")
    else:
        return ret+present_matrix(nmsheet_instance)

        
def present_book(book_instance):
    ret = ""
    for sheet in book_instance.sheets:
        ret += present_nominable_sheet(book_instance.sheets[sheet])
        ret += "\n"
    return ret.strip('\n')

    
STRINGIFICATION["pyexcel.sheets.matrix.Matrix"] = present_matrix
STRINGIFICATION["pyexcel.sheets.matrix.FormattableSheet"] = present_matrix
STRINGIFICATION["pyexcel.sheets.matrix.FilterableSheet"] = present_matrix
STRINGIFICATION["pyexcel.sheets.sheet.NominableSheet"] = present_nominable_sheet
STRINGIFICATION["pyexcel.sheets.sheet.Sheet"] = present_nominable_sheet
STRINGIFICATION["pyexcel.book.Book"] = present_book

