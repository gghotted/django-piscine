from elements import *
from elem import Text


class Page:
    def __init__(self, elem):
        self.elem = elem

    def is_valid(self):
        return self.is_valid_elem_recursive(self.elem)

    @staticmethod
    def is_valid_elem_recursive(elem):
        return Page.is_valid_elem(elem) and \
               all(Page.is_valid_elem_recursive(child) for child in elem.content)

    @staticmethod
    def is_valid_elem(elem):
        return (isinstance(elem, Text) or isinstance(elem, Elem)) and \
               getattr(elem, 'is_valid', lambda: False)()

    def __str__(self):
        if isinstance(self.elem, Html):
            return '<!DOCTYPE html>\n' + str(self.elem)
        return str(self.elem)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))


if __name__ == '__main__':
    print(set().issubset({Text, Html}))
