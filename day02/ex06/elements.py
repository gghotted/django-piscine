from elem import Elem, Text


class DoubleElem(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(self.__class__.__name__.lower(), attr, content, 'double')


class SimpleElem(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(self.__class__.__name__.lower(), attr, content, 'simple')


class Html(DoubleElem):
    def is_valid(self):
        return len(self.content) == 2 and \
               isinstance(self.content[0], Head) and \
               isinstance(self.content[1], Body)


class Head(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Title)


class Body(DoubleElem):
    def is_valid(self):
        return {child.__class__ for child in self.content}.issubset(
            {H1, H2, Div, Table, Ul, Ol, Span, Text}
        )


class Title(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class Meta(SimpleElem):
    def is_valid(self):
        return True


class Img(SimpleElem):
    def is_valid(self):
        return True


class Table(DoubleElem):
    def is_valid(self):
        return all(child.__class__ == Tr for child in self.content)


class Th(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class Tr(DoubleElem):
    def is_valid(self):
        return len(self.content) >= 1 and \
               {child.__class__ for child in self.content} in ({Th}, {Td})


class Td(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class Ul(DoubleElem):
    def is_valid(self):
        return len(self.content) >= 1 and \
               all(child.__class__ == Li for child in self.content)


class Ol(DoubleElem):
    def is_valid(self):
        return len(self.content) >= 1 and \
               all(child.__class__ == Li for child in self.content)


class Li(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class H1(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class H2(DoubleElem):
    def is_valid(self):
        return len(self.content) == 1 and \
               isinstance(self.content[0], Text)


class P(DoubleElem):
    def is_valid(self):
        return {child.__class__ for child in self.content}.issubset(
            {Text}
        )


class Div(DoubleElem):
    def is_valid(self):
        return {child.__class__ for child in self.content}.issubset(
            {H1, H2, Div, Table, Ul, Ol, Span, Text}
        )


class Span(DoubleElem):
    def is_valid(self):
        return {child.__class__ for child in self.content}.issubset(
            {Text, P}
        )


class Hr(SimpleElem):
    def is_valid(self):
        return True


class Br(SimpleElem):
    def is_valid(self):
        return True


if __name__ == '__main__':
    print(
        Html([
            Head(
                Title(Text('"Hello ground!"', escape=False))
            ),
            Body([
                H1(Text('"Oh no, not again!"', escape=False)),
                Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
            ])
        ])
    )
