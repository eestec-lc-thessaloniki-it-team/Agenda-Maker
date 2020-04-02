from BasicClasses.Agenda import *


class ResponseWrapper:

    def __init__(self, object: Agenda, found=False, operationDone=False):
        self.object = object
        self.found = found
        self.operationDone = operationDone
