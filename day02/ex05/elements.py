from elem import Elem, Text


class DoubleElem(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(self.__class__.__name__.lower(), attr, content, 'double')


class SimpleElem(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(self.__class__.__name__.lower(), attr, content, 'simple')


class Html(DoubleElem):
    pass


class Head(DoubleElem):
    pass


class Body(DoubleElem):
    pass


class Title(DoubleElem):
    pass


class Meta(SimpleElem):
    pass


class Img(SimpleElem):
    pass


class Table(DoubleElem):
    pass


class Th(DoubleElem):
    pass


class Tr(DoubleElem):
    pass


class Td(DoubleElem):
    pass


class Ul(DoubleElem):
    pass


class Ol(DoubleElem):
    pass


class Li(DoubleElem):
    pass


class H1(DoubleElem):
    pass


class H2(DoubleElem):
    pass


class P(DoubleElem):
    pass


class Div(DoubleElem):
    pass


class Span(DoubleElem):
    pass


class Hr(SimpleElem):
    pass


class Br(SimpleElem):
    pass


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
