from BasicClasses.Agenda import Agenda
from BasicClasses.Section import Section
from BasicClasses.Topic import Topic

"""
Test.py is a test we run as an example to see how our classes (Agenda/Section/Topic) would work.
"""

gmElectionsTopics = [Topic("openGmstaffEl", True, True, False, ), Topic("MinutesElection", True, False, True, ["Marios", "Tasos", "urMOM"])]
WorkshopTopics = [Topic("openVote", True, True, False), Topic("Future of Workshop", True, False, True, ["Cancelation", "Postpone", "procced"])]
KrasiaTopics = [Topic("openVote", True, True, False), Topic("Wanna go ?", True, True, True), Topic("Where", True, False, True, ["Omprella, Podhlato, SomeWeirdAssPlace"]), Topic("Lets go", False)]

section1 = Section("gmElections", gmElectionsTopics)
section2 = Section("WorkShop", WorkshopTopics)
section3 = Section("Krasia", KrasiaTopics)
sections = [section1, section2, section3]

agenda = Agenda("23-3-20", "001", sections)

dict = agenda.makeJson()
print(dict)

