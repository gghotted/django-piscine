import sys
import requests
from bs4 import BeautifulSoup


class PhilosophyFinder:
    ROOT_URL = 'https://en.wikipedia.org'

    def __init__(self, title):
        title = title.capitalize()
        self.url = f'{self.ROOT_URL}/wiki/{title}'
        self.titles = [title]

    def find(self):
        if self.titles and self.titles[-1] == 'Philosophy':
            return

        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        '''
        :is(condition) == condition인 것 == 괄호 효과를 냄
        :is(a):is(b) == a이고 b인 것
        :is(a):not(b) == a이고 b가 아닌 것
        space == 자손
        > == 자식
        . == class

        :is(.mw-parser-output :is(p,li) > a) == .mw-parser-output의 자손 중 (p 또는 li)의 자식 중 a
        :not(table a) == table의 자손이 아닌 a
        :not(#toc a) == id(toc)의 자손이 아닌 a
        3조건을 모두 만족하는 a
        '''
        redirect = soup.select_one(':is(.mw-parser-output :is(p,li) > a):not(table a):not(#toc a)')

        if not redirect:
            raise Exception('It leads to a dead end !')

        title = redirect.attrs['title']
        if title in self.titles:
            raise Exception('It leads to an infinite loop !')

        self.titles.append(title)
        self.url = self.ROOT_URL +  redirect.attrs['href']
        return self.find()


def main():
    '''
    examples
    normal: "42 (number)", "banana", "apple", "python", "korean"
    dead: "4s2eoul"
    infinite: "lol"
    '''
    if len(sys.argv) != 2:
        return print('Argv length error')

    pf = PhilosophyFinder(sys.argv[1])
    try:
        pf.find()
        print(*pf.titles, sep='\n')
        print(f'{len(pf.titles)} roads from {sys.argv[1]} to philosophy')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
