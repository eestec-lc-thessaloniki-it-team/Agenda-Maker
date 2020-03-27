from BasicClasses.Topic import getTopicFromJson

"""
This class represents a section of the agenda of a general meeting.
Every section contains the topics that are going to be discussed.
"""


class Section:
    def __init__(self, section_name, topics=[]):
        self.section_name = section_name
        self.topics = topics

    def __eq__(self, other):
        if not self.section_name == other.section_name:
            return False
        for index, topic in enumerate(self.topics):
            if topic != other.topics[index]:
                return False
        return True

    def makeJson(self):
        """
            A function that converts a Section's data into Json format
        """

        dict = {"section_name": self.section_name}
        topics_json_list = []
        for topic in self.topics:
            topics_json_list.append(topic.makeJson())
        dict["topics"] = topics_json_list
        return dict


def getSectionFromJson(json) -> Section:
    """
        :param json: the representation of a Section as json
        :return: a Section Object from json file
    """

    new_topics = []
    for topic_json in json.get("topics"):
        new_topics.append(getTopicFromJson(topic_json))
    return Section(json.get("section_name"), new_topics)
