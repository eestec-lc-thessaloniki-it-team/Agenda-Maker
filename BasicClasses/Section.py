from BasicClasses.Topic import Topic

"""
This class represents a section of the agenda of a general meeting.
Every section contains the topics that are going to be discussed.
A function that converts a section's data into Json format(makeJson) is also included.
"""
class Section:
    def __init__(self, section_name, topics):
        self.section_name = section_name
        self.topics = topics

    def makeJson(self):
        dict = { "section_name": self.section_name}
        topics_Json_list = []
        for topic in self.topics:
            topics_Json_list.append(topic.makeJson())
        dict["topics"] = topics_Json_list

        return dict

