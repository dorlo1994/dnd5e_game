import random
import abc


class BaseDice(abc.ABC):
    """
    Base class for dice.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def roll(self, reroll):
        ...


class UniformDice(BaseDice):
    """
    Regular D&D Dice, using uniform distribution.
    """

    def __init__(self, max_val):
        self._max_val = max_val

    def roll(self, reroll=0):
        return random.randint(reroll, self._max_val)


BASIC_DICES = {
    'D_4': UniformDice(4),
    'D_6': UniformDice(6),
    'D_8': UniformDice(8),
    'D_10': UniformDice(10),
    'D_PERCENT': UniformDice(100),
    'D_12': UniformDice(12),
    'D_20': UniformDice(20)
}
