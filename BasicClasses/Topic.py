"""
This class represents a Topic for conversation in a specific section of a General Meeting (GM)
It can be a votable topic with a yes/no/abstain vote or a multiple choice vote, using an open or close ballot system.
"""


class Topic:

    def __init__(self, topic_name, votable, yes_no_vote=None, open_ballot=None, possible_answers=None):
        self.topic_name = topic_name
        self.votable = votable
        self.yes_no_vote = yes_no_vote
        self.open_ballot = open_ballot
        self.possible_answers = possible_answers

    def __eq__(self, other):
        return (
                    self.topic_name == other.topic_name and self.votable == other.votable and self.yes_no_vote == other.yes_no_vote and self.open_ballot == other.open_ballot)

    def makeJson(self):
        """
            A function that converts a Topic's data into Json format
        """

        dict = {"topic_name": self.topic_name, "votable": self.votable}
        if self.votable:
            dict["yes_no_vote"] = self.yes_no_vote
            if not self.yes_no_vote:
                dict["possible_answers"] = self.possible_answers
            dict["open_ballot"] = self.open_ballot
        return dict


def getTopicFromJson(json) -> Topic:
    """
        :param json: the representation of a Topic as json
        :return: a Topic Object from json file
    """

    new_topic = Topic(json.get("topic_name"), json.get("votable"))
    if new_topic.votable:
        new_topic.yes_no_vote = json.get("yes_no_vote")
        if not new_topic.yes_no_vote:
            new_topic.possible_answers = json.get("possible_answers")
        new_topic.open_ballot = json.get("open_ballot")
    return new_topic
