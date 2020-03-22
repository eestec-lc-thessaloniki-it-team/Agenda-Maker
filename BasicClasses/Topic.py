class Topic:

    def __init__(self, topic_name, votable, yes_no_vote = None, open_ballot = None, possible_answers = None):
        self.topic_name = topic_name
        self.votable = votable
        self.yes_no_vote = yes_no_vote
        self.open_ballot = open_ballot
        self.possible_answers = possible_answers

    def makeJson(self):
        dict = {"topic_name": self.topic_name, "votable": self.votable}
        if self.votable:
            dict["yes_no_vote"] =  self.yes_no_vote
            if not self.yes_no_vote:
                dict["possible_answers"] = self.possible_answers
            dict["open_ballot"] = self.open_ballot
        return dict



