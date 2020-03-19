class Person:
    """
    This class is representing a person
    """

    def __init__(self, age, gender, name):
        """
        :param age: his/her age
        :param gender: his gender
        :param name: his name
        """
        self.age = age
        self.gender = gender
        self.name = name

    def makeJson(self):
        dict = {"age": self.age, "gender": self.gender, "name": self.name}
        return dict


tasos = Person(19, "mail", "Tasos")
kallioph = Person(24, "fi-mail", "Poppy")
dict = tasos.makeJson()
print(dict.get("age"))

if kallioph.age>tasos.age:
    print("Krubei xronia")
else:
    print("leei alh8eia")

print(dict)
