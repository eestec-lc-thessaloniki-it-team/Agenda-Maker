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

    def addSection(self, section_name) -> bool:
        """
        add a section object at the end of the sections
        :param section_name: name of the section
        :return: True if everything went ok or False if something went wrong
        """
        return True

    def addSectionInPosition(self, section_name, position) -> bool:
        """
        add a section object at a given position in sections, starting from 0
        :param section_name: name of the section
        :return: True if everything went ok or False if position or something else was wrong
        """
        return True

    def addTopic(self, section_position, topic: Topic) -> bool:
        """
        add a new Topic at the given section_position at the end
        :param topic: new Topic added at the end of the section_position
        :return: True if everything went ok or False if position or something else was wrong
        """
        return True

    def addTopicInPosition(self, section_position, topic: Topic, topic_position) -> bool:
        """
        :param section_position: the position of the section in sections
        :param topic: a new Topic to be added
        :param topic_position: position of topic in the sections
        :return: True if everything was ok or False otherwise
        """
        return True

    def getTopic(self, section_position, topic_position) -> Topic:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in the section
        :return: the topic in the given positions or None if something bad happend
        """
        return None

    def getSection(self, section_position) -> Section:
        """
        :param section_position: position of the section
        :return: the section in this position of sections or None otherwise
        """
        return None

    def deleteToic(self, section_position, topic_position) -> bool:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in the section
        :return: True if everything went ok, or False otherwise
        """
        return True

    def deleteSection(self, section_position) -> bool:
        """
        :param section_position: position of the section
        :return: True if everything went ok, or False otherwise
        """
        return True

    def setSection(self,section_position,newSection:Section)->bool:
        """
        :param section_position: position of the section that wil be overwritten
        :param newSection: the new section object
        :return: True if everything went ok, or False otherwise
        """
        return True

    def setTopic(self,section_position,topic_position,newTopic:Topic)->bool:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in section
        :param newTopic: the new topic that will be written in that index
        :return: True if everything went ok, or False otherwise
        """
        return True
    
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


def getAgendaFromJson(json) -> Agenda:
    """
    :param json: the representation of an Agenda as json
    :return: an Agenda Object from json file
    """
    return None
