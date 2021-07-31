import antigravity
import sys


def main():
    if len(sys.argv) != 4:
        return print('Argv length error')

    try:
        antigravity.geohash(
            float(sys.argv[1]),
            float(sys.argv[2]),
            sys.argv[3].encode()
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
