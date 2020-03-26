from BasicClasses.Agenda import *
from BasicClasses.Section import Section
from BasicClasses.Topic import Topic

"""
Test.py is a test we run as an example to see how our classes (Agenda/Section/Topic) would work.
"""

gmElectionsTopics = [Topic("openGmstaffEl", True, True, False, ),
                     Topic("MinutesElection", True, False, True, ["Marios", "Tasos", "urMOM"])]
WorkshopTopics = [Topic("openVote", True, True, False),
                  Topic("Future of Workshop", True, False, True, ["Cancelation", "Postpone", "proceed"])]
KrasiaTopics = [Topic("openVote", True, True, False), Topic("Wanna go ?", True, True, True),
                Topic("Where", True, False, True, ["Omprella, Podhlato, SomeWeirdAssPlace"]), Topic("Lets go", False)]
MemberTopic = Topic("Promoted by attending GMs", False)
newMemberTopic = Topic("Promoted by organizing an event", False)
TichuTopic = [Topic("Tichu", False)]
CAHTopic = Topic("Cards Against Humanity", False)

section1 = Section("gmElections", gmElectionsTopics)
section2 = Section("WorkShop", WorkshopTopics)
section3 = Section("Krasia", KrasiaTopics)
section4 = Section("Quarantine Games", TichuTopic)
sections = [section1, section2, section3]

agenda = Agenda("23-3-20", "001", "Thessaloniki", sections)


dict = agenda.makeJson()
print("Make Json: " + "\n" + str(dict) + "\n")
myAgenda = getAgendaFromJson(dict)
print("Json to Agenda and back to Json: " + "\n" + str(myAgenda.makeJson()) + "\n")

print(agenda.addSection("Member Promotions"))
# checks duplicate (works)
print("\n")
print(agenda.addSection("Member Promotions"))
print("\n")
print("New section added: " + str(agenda.makeJson()) + "\n")
agenda.addTopic(3, MemberTopic)
print("Added topic to end of section at index 3: " + str(agenda.makeJson()) + "\n")
agenda.addTopicInPosition(3, newMemberTopic, 0)
print("Added topic at index 0 of section at index 3: " + str(agenda.makeJson()) + "\n")
agenda.deleteTopic(3, 0)
print("Deleted topic at index 0 of section at index 3: " + str(agenda.makeJson()) + "\n")
agenda.deleteSection(3)
print("Deleted section at index 3: " + str(agenda.makeJson()) + "\n")
agenda.addSectionInPosition("Member Promotions", 1)
print("Added section at index 1: " + str(agenda.makeJson()) + "\n")
agenda.setSection(2, section4)
print("Changed section at index 2: " + str(agenda.makeJson()) + "\n")
agenda.setTopic(2, 0, CAHTopic)
print("Changed topic at index 0 of section at index 2: " + str(agenda.makeJson()) + "\n")
