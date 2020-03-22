from BasicClasses.Section import Section
from BasicClasses.Topic import Topic


class Agenda:

    def __init__(self, date, sections):
        self.date = date
        self.sections = sections

    def makeJson(self):
        dict = {"date": self.date}
        sections_Json_list = []
        for section in self.sections:
            sections_Json_list.append(section.makeJson())
        dict["sections"] = sections_Json_list

        return dict











