class Parent():
    def __new__(cls: object, feature):
        subclass_map = {subclass.feature: subclass for subclass in cls.__subclasses__()}
        subclass = subclass_map[feature]
        instance = super(Parent, subclass).__new__(subclass)
        return instance

class Child1(Parent):
    def __init__(self) -> None:
        super().__init__()
        self.feature = 1

class Child2(Parent):
    def __init__(self) -> None:
        super().__init__()
        self.feature = 2


type(Parent(1))  # <class '__main__.Child1'>
type(Parent(2))  # <class '__main__.Child2'>