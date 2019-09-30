# basic_backend.py

import mvc_exceptions

items = list()  # a global variable where we keep the data.


def create_items(app_items):
    global items
    items = app_items


def create_item(name, price, quantity):
    global items
    results = list(filter(lambda x: x['name'] == name, items))
    if results:  # truthy hvis results har elementer
        raise mvc_exceptions.ItemAlreadyStored(
            '"{}" already stored!'.format(name)
        )
    else:
        items.append({'name': name, 'price': price, 'quantity': quantity})


def read_item(name):
    global items
    myitems = list(filter(lambda x: x['name'] == name, items))
    if myitems:  # truthy hvis elementer fundet
        return myitems[0]
    else:
        raise mvc_exceptions.ItemNotStored(
            'Can\'t read "{}", because it is not stored.'.format(name))


def read_items():
    global items
    return [item for item in items]


def update_item(name, price, quantity):
    global items

    # i_x er en tuple som kommer fra enumerate(items).
    # i_x ser f.eks. således ud: (0, items[0]).
    # Da vi vil evaluere name, må vi tilgå elementet på tuplens index 1.

    # Lambda udtrykket kigger således efter tupler fra enumerate(items) hvor navnet passer.
    # Filteret tager de tupler, som returnerer sand, dvs. hvor name passer.
    # list putter tuplerne i en liste, den gemmes i idxs_items.
    idxs_items = list(
        filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))

    if idxs_items:  # truthy hvis listen ikke er tom.
        # husk, tuplen ser ud som: (0, items[0]), hent nu disse data
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]

        # opdater samlingen med nye data på ret plads.
        items[i] = {'name': name, 'price': price, 'quantity': quantity}
    else:
        raise mvc_exceptions.ItemNotStored(
            'Can\'t update "{}", bacause it is not stored.'.format(name))


def delete_item(name):
    global items

    # i_x er en tuple som kommer fra enumerate(items).
    # i_x ser f.eks. således ud: (0, items[0]).
    # Da vi vil evaluere name, må vi tilgå elementet på tuplens index 1.

    # Lambda udtrykket kigger således efter tupler fra enumerate(items) hvor navnet passer.
    # Filteret tager de tupler, som returnerer sand, dvs. hvor name passer.
    # list putter tuplerne i en liste, den gemmes i idxs_items.
    idxs_items = list(
        filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))

    if idxs_items:
        # husk, tuplen ser ud som: (0, items[0]), hent nu disse data
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        # opdater samlingen - slet på ret plads.
        del items[i]
    else:
        raise mvc_exceptions.ItemNotStored(
            'Can\'t delete "{}", because it is not stored.'.format(name))


def main():

    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5}
    ]

    # CREATE
    create_items(my_items)
    create_item(name="beer", price=3.0, quantity=15)
    # Fejl hvis beer oprettes igen.
    create_item(name="beer", price=2.5, quantity=10)

    # READ
    print("READ items")
    print(read_items())
    # Fejl hvis vi aflæser vare som ikke er oprettet.
    # print("READ chocolate")
    # print(read_item(name="chocolate"))

    print("READ bread")
    print(read_item("bread"))

    # UPDATE
    print("UPDATE bread")
    update_item("bread", price=2.0, quantity=30)
    print(read_item("bread"))

    # DELETE
    print("DELETE beer")
    delete_item("beer")
    # Fejl hvis vi sletter vare som ikke er oprettet.
    # print("DELETE chocolate")
    # delete_item("chocolate")

    print("READ items")
    print(read_items())


if __name__ == "__main__":
    main()
