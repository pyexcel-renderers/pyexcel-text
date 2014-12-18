"""
    pyexcel.ext.text
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from pyexcel.presentation import STRINGIFICATION


TABLEFMT="simple"


def class_name(name):
    return "<class '%s'>" % name


def present_matrix(matrix_instance):
    """Textualize a Matrix"""
    if TABLEFMT == "json":
        import json
        return json.dumps(matrix_instance.to_array())
    else:
        import tabulate
        return tabulate.tabulate(matrix_instance.to_array(), tablefmt=TABLEFMT)

    
def present_nominable_sheet(nmsheet_instance):
    """Textualize a NominableSheet"""
    if TABLEFMT == "json":
        import json
        return json.dumps({nmsheet_instance.name:nmsheet_instance.to_array()})
    else:
        import tabulate
        ret = "Sheet Name: %s\n" % nmsheet_instance.name
        if len(nmsheet_instance.colnames) > 0:
            data = nmsheet_instance.to_array()
            return ret+tabulate.tabulate(data, headers="firstrow")
        else:
            return ret+present_matrix(nmsheet_instance)

        
def present_book(book_instance):
    """Textualize a pyexcel Book"""
    if TABLEFMT == "json":
        import json
        return json.dumps(book_instance.to_dict())
    else:
        ret = ""
        for sheet in book_instance.sheets:
            ret += present_nominable_sheet(book_instance.sheets[sheet])
            ret += "\n"
        return ret.strip('\n')
        

def save_as(instance, filename):
    """Save a pyexcel instance as text to a file"""
    f = open(filename, "w")
    f.write(str(instance))
    f.close()


def save_to_memory(instance, stream):
    """Save a pyexcel instance as text to a stream"""
    stream.write(str(instance))

    
STRINGIFICATION[class_name("pyexcel.sheets.matrix.Matrix")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.matrix.FormattableSheet")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.matrix.FilterableSheet")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.sheet.NominableSheet")] = present_nominable_sheet
STRINGIFICATION[class_name("pyexcel.sheets.sheet.Sheet")] = present_nominable_sheet
STRINGIFICATION[class_name("pyexcel.book.Book")] = present_book

