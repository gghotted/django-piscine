def read_file(file, mode='r'):
    with open(file, mode) as f:
        return f.read()


def main():
    numbers = read_file('numbers.txt').strip().split(',')
    print(*numbers, sep='\n')


if __name__ == '__main__':
    main()
