# https://www.mediawiki.org/wiki/API:Search#Python

import requests
import dewiki
import sys


class WikiSearcher:
    URL = 'https://en.wikipedia.org/w/api.php'

    def __init__(self, title):
        self.title = title

    def parse_response(self, res):
        data = res.json()
        try:
            return list(data['query']['pages'].items())[0][1]['revisions'][0]['slots']['main']['*']
        except:
            raise Exception('Not matched error')

    def get_page_by_title(self):
        # https://stackoverflow.com/questions/55779015/get-wikitext-from-wikipedia-api
        params = {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'json',
            'rvslots': 'main',
            'titles': self.title
        }
        res = requests.get(self.URL, params=params)

        if res.status_code != 200:
            raise Exception(f'Response status error: {res.status_code}')

        wikitext = self.parse_response(res)

        if wikitext.startswith('#REDIRECT'):
            self.title = self.parse_redirect(wikitext)
            return f'# 입력 내용이 적절하지 않아 "{self.title}"로 수정되어 검색된 결과입니다\n\n' + self.get_page_by_title()

        text = dewiki.from_string(wikitext)
        return text.strip()

    def parse_redirect(self, wikitext):
        start = wikitext.find('[[') + 2
        end = wikitext.find(']]')
        return wikitext[start:end]


def parse_response(res):
    data = res.json()
    return list(data['query']['pages'].items())[0][1]['revisions'][0]['slots']['main']['*']


def main():
    if len(sys.argv) != 2:
        print('argv length error')
        return

    '''
    examples
    normal: python
    redirect: pythom
    not matched: "markup languag"
    '''
    try:
        content = WikiSearcher(sys.argv[1]).get_page_by_title()
        with open(sys.argv[1] + '.wiki', 'w') as f:
            f.write(content)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
