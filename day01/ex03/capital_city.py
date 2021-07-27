import sys


def main():

    if len(sys.argv) != 2:
        return

    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    key = sys.argv[1]

    try:
        print(capital_cities[states[key]])
    except:
        print("Unknown state")


if __name__ == '__main__':
    main()
