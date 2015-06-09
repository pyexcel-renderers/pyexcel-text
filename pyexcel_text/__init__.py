"""
    pyexcel.ext.text
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from pyexcel.presentation import STRINGIFICATION
from pyexcel_io import BookWriter, SheetWriterBase, is_string, WRITERS
from pyexcel.deprecated import deprecated
from functools import partial


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
            return ret+tabulate.tabulate(data, headers="firstrow",
                                         tablefmt=TABLEFMT)
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
        
@partial(
    deprecated,
    message="Deprecated since v0.0.3! Please use pyexcel's save_as, save_book_as or instance method Sheet.save_as or Book.save_as")
def save_as(instance, filename):
    """Save a pyexcel instance as text to a file"""
    f = open(filename, "w")
    f.write(str(instance))
    f.close()


@partial(
    deprecated,
    message="Deprecated since v0.0.3! Please use pyexcel's save_as, save_book_as or instance method Sheet.save_to_memory or Book.save_to_memory")
def save_to_memory(instance, stream):
    """Save a pyexcel instance as text to a stream"""
    stream.write(str(instance))

    
STRINGIFICATION[class_name("pyexcel.sheets.matrix.Matrix")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.matrix.FormattableSheet")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.matrix.FilterableSheet")] = present_matrix
STRINGIFICATION[class_name("pyexcel.sheets.sheet.NominableSheet")] = present_nominable_sheet
STRINGIFICATION[class_name("pyexcel.sheets.sheet.Sheet")] = present_nominable_sheet
STRINGIFICATION[class_name("pyexcel.book.Book")] = present_book


class TextSheetWriter(SheetWriterBase):
    def __init__(self, filehandle, file_type, name, **keywords):
        self.filehandle = filehandle
        self.file_type = file_type
        self.keywords = keywords
        title = "Sheet Name: %s\n" % name
        self.filehandle.write(title)

    def set_size(self, size):
        pass

    def write_array(self, table):
        import tabulate
        if 'single_sheet_in_book' in self.keywords:
            self.keywords.pop('single_sheet_in_book')
        self.filehandle.write(tabulate.tabulate(table,
                                                tablefmt=self.file_type,
                                                **self.keywords))

    def close(self):
        self.filehandle.write('\n')
        pass


class TextWriter(BookWriter):
    def __init__(self, file, **keywords):
        BookWriter.__init__(self, file, **keywords)
        if is_string(type(file)):
            self.f = open(file, 'w')
        else:
            self.f = file

    def create_sheet(self, name):
        return TextSheetWriter(
            self.f,
            self.file_type,
            name,
            **self.keywords)

    def close(self):
        if is_string(type(file)):
            self.f.close()


class JsonSheetWriter(TextSheetWriter):
    def __init__(self, filehandle, name, **keywords):
        self.filehandle = filehandle
        self.keywords = keywords

    def write_array(self, table):
        import json
        self.filehandle.write(json.dumps(table))

    def close(self):
        pass


class JsonWriter(TextWriter):
    def __init__(self, file, **keywords):
        TextWriter.__init__(self, file, **keywords)

    def write(self, sheet_dicts):
        import json
        self.f.write(json.dumps(sheet_dicts))

    def create_sheet(self, name):
        return JsonSheetWriter(self.f, name)

    def close(self):
        TextWriter.close(self)


WRITERS.update({
    "simple": TextWriter,
    "plain": TextWriter,
    "grid": TextWriter,
    "pipe": TextWriter,
    "orgtbl": TextWriter,
    "rst": TextWriter,
    "mediawiki": TextWriter,
    "latex": TextWriter,
    "latex_booktabs": TextWriter,
    "json": JsonWriter
})
