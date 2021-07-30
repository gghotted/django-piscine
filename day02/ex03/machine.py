from beverages import *
import random


class CoffeeMachine:
    class EmptyCup(HotBeverage):
        price = 0.90
        name = 'empty cup'

        def description(self):
            return 'An empty cup?! Gimme my money back!'

    def __init__(self):
        self.hp = 10

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__('This coffee machine has to be repaired.')

    def repair(self):
        self.hp = 10

    def serve(self, beverage_cls):
        if self.hp == 0:
            raise CoffeeMachine.BrokenMachineException()

        self.hp -= 1
        return random.choices([beverage_cls(), CoffeeMachine.EmptyCup()], weights=[0.8, 0.2])[0]


def serve_until_broken(machine):
    while True:
        try:
            beverage_cls = random.choice((HotBeverage, Coffee, Tea, Chocolate, Cappuccino))
            beverage = machine.serve(beverage_cls)
            print(beverage, end='\n\n')
        except Exception as e:
            print(e, end='\n\n')
            break


def main():
    machine = CoffeeMachine()
    serve_until_broken(machine)
    machine.repair()
    serve_until_broken(machine)


if __name__ == '__main__':
    main()
