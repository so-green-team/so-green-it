import time

class Task:
    PENDING = 0
    RUNNING = 1
    DONE = 2
    FAILED = -1

    def __init__(self, id, test):
        self.status = Task.PENDING
        self.id = id
        self.timestamp = time.time()
        self.result = None
        self.__test = test

    def start(self, url):
        self.status = Task.RUNNING
        self.result = self.__test(url)

        if isinstance(self.result, bool) and not self.result:
            self.status = Task.FAILED
        else:
            self.status = Task.DONE
