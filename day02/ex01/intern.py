class Intern:
    def __init__(self, name='My name? I’m nobody, an intern, I have no name.'):
        self.name = name

    def __str__(self):
        return self.name

    class WorkError(Exception):
        def __init__(self):
            super().__init__('I’m just an intern, I can’t do that...')

    def work(self):
        raise self.WorkError()

    class Coffee:
        def __str__(self):
            return 'This is the worst coffee you ever tasted.'

    def make_coffee(self):
        return self.Coffee()


def main():
    # test case1
    intern = Intern()
    print(intern)
    try:
        intern.work()
    except Exception as e:
        print(e)

    # test case2
    mark = Intern('Mark')
    print(mark)
    print(mark.make_coffee())


if __name__ == '__main__':
    main()

