from BasicClasses.Section import Section
from BasicClasses.Topic import Topic

"""
This class represents the agenda of a general meeting
(a.k.a. Basic information about the gm and also what is going to be discussed, divided into thematic sections)
A function that converts the agenda's data into Json format(makeJson) is also included.
"""
class Agenda:

    def __init__(self, date, id, sections):
        self.date = date
        self.id = id
        self.sections = sections

    def makeJson(self):
        dict = {
                "date": self.date,
                "id": self.id
                }
        sections_Json_list = []
        for section in self.sections:
            sections_Json_list.append(section.makeJson())
        dict["sections"] = sections_Json_list

        return dict











