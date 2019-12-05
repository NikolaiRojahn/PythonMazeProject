class Demo():
    staticVariable = "Im so static"

    def __init__(self, dynamicVariable):
        self.dynamicVariable = dynamicVariable

    def printStatic(self):
        print(self.staticVariable)
        
if __name__ == '__main__':
    a = Demo("a")
    b = Demo("b")

    print(a.staticVariable)
    a.printStatic()
    print(a.dynamicVariable)
    print(b.staticVariable)
    print(b.dynamicVariable)
    Demo.staticVariable = "Im excited"
    print(a.staticVariable)
    print(b.staticVariable)
    print(Demo.staticVariable)
