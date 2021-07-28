import settings
import sys
import os
import re


def render(file, variables):
    def replace(match):
        match = match.group()
        key = match[1:-1]
        return str(variables.get(key, ''))

    with open(file, 'r') as f:
        template = f.read()
        return re.sub('{.*}', replace, template)


def main():
    assert len(sys.argv) == 2, 'argument length error'

    file = sys.argv[1]
    assert os.path.isfile(file), 'not available file error'

    non_ext, ext = os.path.splitext(file)
    assert ext == '.template', 'input file extention error'

    variables = {
        key: getattr(settings, key)
        for key in dir(settings)
        if not key.startswith('__')
    }
    with open(non_ext + '.html', 'w') as f:
        f.write(render(file, variables))


if __name__ == '__main__':
    main()
