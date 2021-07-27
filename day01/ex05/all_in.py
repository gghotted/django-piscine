import sys


def search_by_value(dic, search_val):
    for key, val in dic.items():
        if val == search_val:
            return key


def search_city(cities_dict, key):
    try:
        return key, cities_dict[key]
    except:
        return search_by_value(cities_dict, key), key


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
    cities_dict = {key: capital_cities[val] for key, val in states.items()}
    keys = map(
        lambda key: key.strip(),
        sys.argv[1].split(",")
    )

    for key in keys:
        if not key:
            continue

        state, capital_city = search_city(cities_dict, key.title())
        if state and capital_city:
            print(f'{capital_city} is the capital of {state}')
        else:
            print(f'{key} is neither a capital city nor a state')


if __name__ == '__main__':
    main()
