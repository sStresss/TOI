def bread(func1):
    def wrapper():
        print("</------\>")
        func1()
        print("<\______/>")

    return wrapper


def ingredients(func):
    def wrapper():
        print("#помидоры#")
        func()
        print("~салат~")

    return wrapper


@bread
@ingredients
def sandwich(food="--ветчина--"):
    print(food)

class Myclass():
    @staticmethod
    def staticmethod():
        print('static method called')

Myclass.staticmethod()
# sandwich()
