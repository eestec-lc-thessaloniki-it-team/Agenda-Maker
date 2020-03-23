class connectMongo:

    def __init__(self):
        """
        connect to database with creadentials and get an obect of mongoclient
        """
        # self.client = MongoClient(url, authSource="admin")[database]
        # db = client.lcThessaloniki
    #
    def getAllDatabasesFromLC(self):
        """
        :return: all the databases from this lc
        """
        pass

    def createNewAgenda(self, json_agenda):
        """
        Add this agenda to mongo
        :param json_agenda:
        :return:
        """
        pass

    def getAgendaById(self, agenda_id):
        pass

    def updateAgenda(self, agenda_id, new_agenda):
        pass

    def createNewTopic(self, agenda_id, topic_json):
        """
        Get agenda
        Make it object
        Add topic
        Update agenda
        :param agenda_id:
        :param topic_json:
        :return:
        """
        pass

    def createNewTSession(self, agenda_id, session_name):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param session_name:
        :return:
        """
        pass

    def deleteNewTopic(self, agenda_id, topic_name):
        """
        Get agenda
        Make it object
        Add topic
        Update agenda
        :param agenda_id:
        :param topic_json:
        :return:
        """
        pass

    def deleteNewTSession(self, agenda_id, session_name):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param session_name:
        :return:
        """
        pass

    def deleteAgenda(self, agenda_id):
        pass
