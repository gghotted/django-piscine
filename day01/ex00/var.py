def print_info(var):
    print(f'{var} has a type {type(var)}')


def my_var():
    vars = [
        42,
        '42',
        'quarante-deux',
        42.0,
        True,
        [42],
        {42: 42},
        (42,),
        set()
    ]
    for var in vars:
        print_info(var)


if __name__ == '__main__':
    my_var()
