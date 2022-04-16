import random
import abc

from dataclasses import dataclass


@dataclass
class DieRoll:
    min: int
    max: int
    value: int
    name: str

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return f'{self.min} - {self.max}: {self.value}'


@dataclass
class DieRollSet:
    rolls: list[DieRoll]

    @property
    def values(self):
        return [roll.value for roll in self.rolls]

    @property
    def value(self):
        return sum(self.values)

    def __repr__(self):
        repr_str = f'{len(self.rolls)}*{self.rolls[0].name}:\n'
        repr_str += '\n'.join([str(roll) for roll in self.rolls])
        if len(self.rolls) > 1:
            repr_str += f'\nTotal: {self.value}'
        return repr_str


class BaseDie(abc.ABC):
    """
    Base class for die.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def roll(self, min_val):
        """
        Rolls the die once.
        :param min_val: Minimum value of roll (reroll value)
        :return: One roll object
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

    def __init__(self, max_val, name):
        super().__init__(name)
        self._max_val = max_val

    def roll(self, min_val=0):
        value = random.randint(min_val+1, self._max_val)
        return DieRoll(min_val+1, self._max_val, value, self.name)

    @property
    def min(self):
        return 1
