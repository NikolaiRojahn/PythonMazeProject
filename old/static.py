class Demo():
    staticVariable = "Im so static"

    def __init__(self, dynamicVariable):
        self.dynamicVariable = dynamicVariable

    def printStaticVariables(self):
        print(self.dynamicVariable + ".staticVariable: " + self.staticVariable)
        print("Demo.staticVariable: " + Demo.staticVariable)


if __name__ == '__main__':
    a = Demo("a")
    b = Demo("b")

    print(a.dynamicVariable)
    a.printStaticVariables()
    print(b.dynamicVariable)
    b.printStaticVariables()

    # changes copy of Demo.staticVariable of instance a.
    print("\nChanging a.staticVariable to \"Im excited\"...")
    a.staticVariable = "Im excited"
    print("Changing Demo.staticVariable to \"Im still static\"...\n")
    Demo.staticVariable = "Im still static"
    a.printStaticVariables()
    b.printStaticVariables()
    print(Demo.staticVariable)
