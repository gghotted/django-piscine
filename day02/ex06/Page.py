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
               all(Page.is_valid_elem_recursive(child)
                   for child in getattr(elem, 'content', []))

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


class Test:
    # valid elements
    body = Body()
    meta = Meta()
    img = Img()
    table = Table()
    p = P()
    div = Div()
    span = Span()
    hr = Hr()
    br = Br()
    text = Text('text')
    th = Th(text)
    tr = Tr(th)
    title = Title(text)
    head = Head(title)
    html = Html([head, body])
    h1 = H1(text)
    h2 = H2(text)
    td = Td(text)
    li = Li(text)
    ul = Ul(li)
    ol = Ol(li)

    def run(self):
        for key in dir(self):
            if not key.startswith('test_'):
                continue

            test_case = getattr(self, key)
            test_case()
            print(test_case.__name__, ': OK')

    def test_html(self):
        assert Page(
            self.html
        ).is_valid() == True, 'valid case'

        assert Page(
            Html(
                self.head
            )
        ).is_valid() == False, 'non-body case'

        assert Page(
            Html(
                self.body
            )
        ).is_valid() == False, 'non-head case'

        assert Page(
            Html()
        ).is_valid() == False, 'non-content case'

        assert Page(
            Html([
                self.body,
                self.head
            ])
        ).is_valid() == False, 'invalid order case'

        assert Page(
            Html([
                self.head,
                self.body,
                self.body
            ])
        ).is_valid() == False, 'invalid content length case'

    def test_head(self):
        assert Page(
            self.head
        ).is_valid() == True, 'valid case'

        assert Page(
            Head()
        ).is_valid() == False, 'non-title case'

        assert Page(
            Head([
                self.title,
                self.title
            ])
        ).is_valid() == False, 'duplicate title case'

        assert Page(
            Head([
                self.title,
                self.text
            ])
        ).is_valid() == False, 'contain non-title case'

    # Body, Div same rule
    def test_body(self, elem=None):
        elem = elem if elem else self.body

        assert Page(
            elem
        ).is_valid() == True, 'valid case'

        assert Page(
            elem.__class__([
                self.h1,
                self.h2,
                self.div,
                self.table,
                self.ul,
                self.ol,
                self.span,
                self.text
            ])
        ).is_valid() == True, 'valid elements case'

        assert Page(
            elem.__class__(
                self.br
            )
        ).is_valid() == False, 'contain invalid elem case'

    def test_div(self):
        self.test_body(self.div)

    def test_title(self, elem=None):
        elem = elem if elem else self.title

        assert Page(
            elem
        ).is_valid() == True, 'valid case'

        assert Page(
            elem.__class__()
        ).is_valid() == False, 'non-content case'

        assert Page(
            elem.__class__(
                self.br
            )
        ).is_valid() == False, 'contain non-text case'

        assert Page(
            elem.__class__([
                self.text,
                self.br
            ])
        ).is_valid() == False, 'contain non-test case2'

        assert Page(
            elem.__class__([
                self.text,
                self.text
            ])
        ).is_valid() == False, 'duplicate text case'

    def test_h1(self):
        self.test_title(self.h1)

    def test_h2(self):
        self.test_title(self.h2)

    def test_li(self):
        self.test_title(self.li)

    def test_th(self):
        self.test_title(self.th)

    def test_td(self):
        self.test_title(self.td)

    def test_p(self):
        assert Page(
            self.p
        ).is_valid() == True, 'valid case'

        assert Page(
            P()
        ).is_valid() == True, 'non-content case'

        assert Page(
            P(
                self.text,
                self.text
            )
        ).is_valid() == True, 'multi-text case'

        assert Page(
            P(
                self.br
            )
        ).is_valid() == False, 'contain non-text case'

    def test_span(self):
        assert Page(
            self.span
        ).is_valid() == True, 'valid case'

        assert Page(
            Span(
                self.text
            )
        ).is_valid() == True, 'contain valid-elem case'

        assert Page(
            Span(
                self.p
            )
        ).is_valid() == True, 'contain valid-elem case2'

        assert Page(
            Span([
                self.text,
                self.p
            ])
        ).is_valid() == True, 'contain valid-elem case3'

        assert Page(
            Span([
                self.text,
                self.p,
                self.text,
                self.p
            ])
        ).is_valid() == True, 'contain valid-elem case4'

        assert Page(
            Span([
                self.text,
                self.p,
                self.br
            ])
        ).is_valid() == False, 'contain invalid-elem case'

    def test_ul(self, elem=None):
        elem = elem or self.ul

        assert Page(
            elem
        ).is_valid() == True, 'valid case'

        assert Page(
            elem.__class__([
                self.li,
                self.li
            ])
        ).is_valid() == True, 'multi-li case'

        assert Page(
            elem.__class__()
        ).is_valid() == False, 'empty content case'

        assert Page(
            elem.__class__(
                self.br
            )
        ).is_valid() == False, 'contain invalid-elem case'

        assert Page(
            elem.__class__([
                self.li,
                self.br
            ])
        ).is_valid() == False, 'contain invalid-elem case2'

    def test_ol(self):
        self.test_ul(self.ol)

    def test_tr(self):
        assert Page(
            self.tr
        ).is_valid() == True, 'valid case'

        assert Page(
            Tr(
                self.td
            )
        ).is_valid() == True, 'contain td case'

        assert Page(
            Tr([
                self.th,
                self.th
            ])
        ).is_valid() == True, 'contain multi-th case'

        assert Page(
            Tr([
                self.td,
                self.td
            ])
        ).is_valid() == True, 'contain multi-td case'

        assert Page(
            Tr([
                self.th,
                self.td
            ])
        ).is_valid() == False, 'contain mix-th-td case'

        assert Page(
            Tr()
        ).is_valid() == False, 'empty content case'

    def test_table(self):
        assert Page(
            self.table
        ).is_valid() == True, 'valid case'

        assert Page(
            Table(
                self.tr
            )
        ).is_valid() == True, 'contain tr case'

        assert Page(
            Table([
                self.tr,
                self.tr
            ])
        ).is_valid() == True, 'contain multi-tr case'

        assert Page(
            Table(
                self.br
            )
        ).is_valid() == False, 'contain invalid-elem case'

        assert Page(
            Table([
                self.tr,
                self.br
            ])
        ).is_valid() == False, 'contain invalid-elem case2'

    def test_contain_invalid_object(self):
        assert Page(1).is_valid() == False, 'int case'
        assert Page(Elem()).is_valid() == False, 'base class case'

    def test_recursive(self):
        assert Page(
            Html([
                Head(
                    Title(Br())
                ),
                self.body
            ])
        ).is_valid() == False, 'html ok, but head ko case'

    def test_page_str(self):
        assert Page(
            self.html
        ).__str__().startswith('<!DOCTYPE html>\n'), 'add DOCTYPE on front'

        assert Page(
            self.h1
        ).__str__().startswith('<h1>'), 'non DOCTYPE'

    def test_page_wirte_to_file(self):
        Page(
            Html([
                Head(
                    Title(Text('complete-page'))
                ),
                Body(
                    H1(Text('Complete page!'))
                )
            ])
        ).write_to_file('complete_page.html')

        Page(
            H1(Text('Non Complete page!'))
        ).write_to_file('non_complete_page.html')


if __name__ == '__main__':
    Test().run()
