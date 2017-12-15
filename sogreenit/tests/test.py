#TODO abstract class that raise an exception when the run method is called
from abc import ABC

class TestException(Exception):
    """Exception raised when a wrong call to run is done"""
    pass

class Test(ABC):
    """Base class for all rules tested"""

    @staticmethod
    @abstractmethod
    def run():
        raise TestException
