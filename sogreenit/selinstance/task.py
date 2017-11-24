from time import time

class Task:
    """
    Represent as task to be handled by so-green-it
    """

    PENDING = 0
    RUNNING = 1
    DONE = 2
    FAILED = -1

    def __init__(self, id, test):
        self.status = Task.PENDING
        self.id = id
        self.created = time()
        self.completed = None
        self.result = None
        self.__test = test
