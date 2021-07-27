import sys


def reverse_dict(d):
    return dict(map(reversed, d.items()))


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

    rstates = reverse_dict(states)
    rcapital_cities = reverse_dict(capital_cities)
    key = sys.argv[1]

    try:
        print(rstates[rcapital_cities[key]])
    except:
        print("Unknown capital city")


if __name__ == '__main__':
    main()
