# program.py

import controller
import model
import view
# small program to test MVC from tutorial.


def main():

    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5},
    ]

    c = controller.Controller(model.ModelBasic(my_items), view.View())
    c.show_items()
    c.show_items(True)
    c.show_item('chocolate')


if __name__ == '__main__':
    main()
