import random
import abc


class BaseDie(abc.ABC):
    """
    Base class for die.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def roll(self, min_val):
        """
        Rolls the die once.
        :param min_val: Minimum value of roll (reroll value)
        :return: Result of one roll
        """
        ...

    @property
    @abc.abstractmethod
    def min(self):
        ...


class UniformDie(BaseDie):
    """
    Regular D&D Die, using uniform distribution.
    """

    def __init__(self, max_val):
        self._max_val = max_val

    def roll(self, min_val=0):
        return random.randint(min_val+1, self._max_val)

    @property
    def min(self):
        return 1
