from local_lib import path


def main():
    d = path.Path('./tmp')
    # f = d.joinpath('file')
    f = path.Path('./tmp/file')

    if d.isfile():
        d.remove()
    if d.isdir():
        d.rmtree()

    d.mkdir()
    f.write_text('hello world!')
    print(f.read_text())


if __name__ == '__main__':
    main()
