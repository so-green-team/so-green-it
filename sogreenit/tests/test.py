#TODO abstract class that raise an exception when the run method is called

class TestException(Exception):
    """Exception raised when a wrong call to run is done"""
    pass

class Test():
    """Base class for all rules tested"""

    @staticmethod
    def run():
        raise TestException
