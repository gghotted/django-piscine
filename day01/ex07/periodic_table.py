class Tag:
    def __init__(self, tag, children=None, attr=None, end=True):
        self.tag = tag
        self.children = children if children else []
        self.attr = attr if attr else ''
        self.end = end

    def render(self):
        inner_render = ''.join(
            [(child.render() if type(child) == Tag else child) for child in self.children]
        )
        if self.end:
            return f'<{self.tag} {self.attr}> {inner_render} </{self.tag}>'
        return f'<{self.tag} {self.attr}/>'


def parse_value(text, key):
    key += ':'
    start = text.find(key) + len(key)
    return text[start:].strip()


def get_element(text):
    fields = text.split(',')
    return {
        'name': fields[0].split('=')[0].strip(),
        'position': parse_value(fields[0], 'position'),
        'number': parse_value(fields[1], 'number'),
        'small': parse_value(fields[2], 'small'),
        'molar': parse_value(fields[3], 'molar'),
        'electron': parse_value(fields[4], 'electron')
    }


def get_elements():
    with open('periodic_table.txt', 'r') as f:
        lines = f.read().strip().split('\n')
        return [get_element(line) for line in lines]


def make_td_tag(element):
    td = Tag('td', attr='style="border: solid; padding: 10px"')

    if not element:
        return td

    h4 = Tag('h4', [element['name']])
    ul = Tag('ul', [
        Tag('li', ['No ' + element['number']]),
        Tag('li', [element['small']]),
        Tag('li', [element['molar']]),
        Tag('li', [element['electron']])
    ], attr='style="padding-left: 15px;"')
    td.children += [h4, ul]
    return td


def make_table_tag(elements):
    table = Tag('table', attr='style="border: solid; border-collapse: collapse; width: 100%"')

    while elements:
        tr = Tag('tr')

        for pos in range(18):
            if not elements:
                break

            element = elements.pop(0) if str(pos) == elements[0]['position'] else None
            td = make_td_tag(element)
            tr.children.append(td)

        table.children.append(tr)

    return table


def main():
    elements = get_elements()
    table = make_table_tag(elements)
    head = Tag('head', [
        Tag('title', ['ex07']),
        Tag('meta', attr='charset="utf-8"', end=False)
    ])
    body = Tag('body', [table])
    html = Tag('html', [head, body], attr='lang=en')
    rendered = '<!DOCTYPE html>' + html.render()

    with open('periodic_table.html', 'w') as f:
        f.write(rendered)


if __name__ == '__main__':
    main()
