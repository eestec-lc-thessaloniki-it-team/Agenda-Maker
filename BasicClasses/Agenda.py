from BasicClasses.Section import *
from BasicClasses.Topic import Topic

"""
This class represents the agenda of a general meeting
(a.k.a. Basic information about the gm and also what is going to be discussed, divided into thematic sections)
"""


class Agenda:

    def __init__(self, date, id, lc, sections=[]):
        self.date = date
        self.id = id
        self.lc = lc
        self.sections = sections

    def addSection(self, section_name) -> bool:
        """
        add a section object at the end of the sections
        :param section_name: name of the section
        :return: True if everything went ok or False if something went wrong
        """

        return self.addSectionInPosition(section_name, len(self.sections))

    def addSectionInPosition(self, section_name, position) -> bool:
        """
        add a section object at a given position in sections, starting from 0
        :param section_name: name of the section
        :return: True if everything went ok or False if position or something else was wrong
        """

        already_exists = False
        for section in self.sections:
            if section.section_name == section_name:
                already_exists = True
        if position > len(self.sections) or already_exists:
            return False
        self.sections.insert(position, Section(section_name, []))
        return True

    def addTopic(self, section_position, topic: Topic) -> bool:
        """
        add a new Topic at the given section_position at the end
        :param topic: new Topic added at the end of the section_position
        :return: True if everything went ok or False if position or something else was wrong
        """

        return self.addTopicInPosition(section_position, topic, len(self.sections[section_position].topics))

    def addTopicInPosition(self, section_position, topic: Topic, topic_position) -> bool:
        """
        :param section_position: the position of the section in sections
        :param topic: a new Topic to be added
        :param topic_position: position of topic in the sections
        :return: True if everything was ok or False otherwise
        """

        if topic in self.sections[section_position].topics or section_position > len(self.sections) \
                or topic_position > len(self.sections[section_position].topics):
            return False
        self.sections[section_position].topics.insert(topic_position, topic)
        return True

    def getTopic(self, section_position, topic_position) -> Topic:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in the section
        :return: the topic in the given positions or None if something bad happened
        """

        if section_position < len(self.sections) and topic_position < len(self.sections[section_position].topics):
            return self.sections[section_position].topics[topic_position]
        return None

    def getSection(self, section_position) -> Section:
        """
        :param section_position: position of the section
        :return: the section in this position of sections or None otherwise
        """

        if section_position < len(self.sections):
            return self.sections[section_position]
        return None

    def deleteTopic(self, section_position, topic_position) -> bool:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in the section
        :return: True if everything went ok, or False otherwise
        """

        if section_position < len(self.sections) and topic_position < len(self.sections[section_position].topics):
            self.sections[section_position].topics.pop(topic_position)
            return True
        return False

    def deleteSection(self, section_position) -> bool:
        """
        :param section_position: position of the section
        :return: True if everything went ok, or False otherwise
        """

        if section_position < len(self.sections):
            self.sections.pop(section_position)
            return True
        return False

    def setSection(self, section_position, newSection: Section) -> bool:
        """
        :param section_position: position of the section that wil be overwritten
        :param newSection: the new section object
        :return: True if everything went ok, or False otherwise
        """

        if section_position < len(self.sections):
            self.sections[section_position] = newSection
            return True
        return False

    def setTopic(self, section_position, topic_position, newTopic: Topic) -> bool:
        """
        :param section_position: position of the section
        :param topic_position: position of the topic in section
        :param newTopic: the new topic that will be written in that index
        :return: True if everything went ok, or False otherwise
        """

        if section_position < len(self.sections) and topic_position < len(self.sections[section_position].topics):
            self.sections[section_position].topics[topic_position] = newTopic
            return True
        return False

    def __eq__(self, other):
        if not (self.id == other.id and self.lc == other.lc):
            return False
        for index, section in enumerate(self.sections):
            if not section == other.sections[index]:
                return False
        return True

    def makeJson(self):
        """
            A function that converts an Agenda's data into Json format
        """

        dict = {
            "date": self.date,
            "id": self.id,
            "lc": self.lc
        }
        sections_json_list = []
        for section in self.sections:
            sections_json_list.append(section.makeJson())
        dict["sections"] = sections_json_list

        return dict


def getAgendaFromJson(json) -> Agenda:
    """
    :param json: the representation of an Agenda as json
    :return: an Agenda Object from json file
    """

    if "date" in json and "lc" in json and "id" in json and "sections" in json:
        new_sections = []
        for section_json in json.get("sections"):
            new_sections.append(getSectionFromJson(section_json))
        return Agenda(json.get("date"), json.get("id"), json.get("lc"), new_sections)
    else:
        return None
