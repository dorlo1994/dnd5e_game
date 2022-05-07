import abc

from collections import namedtuple

from dice.dice import BaseDie
from dice.dice_factory import get_base_dice
from dice.dice_roller import DiceRoller
from functools import partial


STANDARD_STAT_NAMES = ['str',
                       'dex',
                       'con',
                       'int',
                       'wis',
                       'cha']


class Stat:
    """
    Class for holding the data of a single stat.
    """
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    @property
    def modifier(self) -> int:
        """
        Stat Modifier, as defined in the PHB page 13.
        :return: integer representing stat modifier.
        """
        return (self.value - 10) // 2

    def increment(self):
        """
        Increases stat score by 1.
        :return: None
        """
        self.value += 1

    def __repr__(self):
        return f"{self.modifier} ({self.value})"


class Stats:
    """
    Class for holding an entity's list of stats and iterating over them.
    """
    def __init__(self, stats: list[Stat]):
        self.stats = {s.name: s for s in stats}

    def __getitem__(self, item):
        return self.stats[item]

    def __iter__(self):
        self.stat_names = list(self.stats.keys())
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.stat_names):
            stat_name = self.stat_names[self.index]
            stat = self.stats[stat_name]
            self.index += 1
            return stat
        else:
            raise StopIteration

    def __repr__(self):
        repr_str = ""
        for name, value in self.stats.items():
            repr_str += f"{name}: {value}\n"
        return repr_str

# Value Generators:
# Functions that take no argument and return some integer.
# Will be wrapped in partial() in the initializers.


def constant_value_generator(value: int):
    return value


def random_value_generator(roller: DiceRoller, dice_count: int, dice_type: BaseDie, keep: int, min_val: int):
    return roller.roll_keep_reroll(dice_count, dice_type, keep, min_val)[0]

# Stats Validators
# Functions that take a list of stats and either return True or raise a ValueError.


def universal_validator(stats: list[Stat]) -> bool:
    """
    Returns true on any list.
    :param stats: List of Stat objects
    :return: True
    """
    return True


def array_validator(stats: list[Stat], array: list[int]) -> bool:
    """
    Validates all elements of the stat list appear once and only once in array.
    :param stats: List of stats to validate
    :param array: Array to check against
    :return: True iff stats is a permutation of array.
    :raises: ValueErrorTrue
    """
    expected_array = array.copy()
    stat_iter = iter(stats)
    for s in stat_iter:
        if s.value not in expected_array:
            raise ValueError(f"Stat value {s.value} not in given array.")
        expected_array.remove(s.value)
    return True


def cost_validator(stats: list[Stat], costs: dict[int: int], total: int) -> bool:
    """
    Validates that the sum of the costs of stats equals total.
    :param stats: List of stats
    :param costs: Dict specifying cost of each stat score.
    :param total: Total amount that can be payed.
    :return: True iff sum(costs[stats]) == total.
    :raises: ValueError
    """
    stat_iter = iter(stats)
    total_cost = 0
    for s in stat_iter:
        cost = costs.get(s.value)
        if cost is None:
            raise ValueError(f"Got invalid stat value {s.value}")
        total_cost += cost
    if total_cost != total:
        raise ValueError(f"Total cost is {total_cost}, should be {total}")
    return True


class AbstractStatsInitializer(abc.ABC):
    """
    Class for initializing a stats object using a set of value generators.
    Optionally: Validates the stats object with a validator.
    """

    StatGenerator = namedtuple('StatGenerator', ['name', 'value_generator'])

    def __init__(self, names, value_generators, validator=universal_validator):
        assert len(names) == len(value_generators), f"Given {len(names)} names but {len(value_generators)} generators!"
        self.generators = [self.StatGenerator(names[i], value_generators[i]) for i in range(len(names))]
        self.validator = validator

    def generate(self):
        """
        Iterates over the generators and fixes a value to them.
        :return: A Stats object with the generated stats.
        """
        generated_stats = [Stat(g.name, g.value_generator()) for g in self.generators]
        self.validator(generated_stats)
        return Stats(generated_stats)


class DiceStatsInitializer(AbstractStatsInitializer):
    """
    Generates values with random rolls, no validation.
    """
    def __init__(self, roller, dice_count, dice_type, keep, min_val, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        generators = [partial(random_value_generator,
                              roller=roller,
                              dice_count=dice_count,
                              dice_type=dice_type,
                              keep=keep,
                              min_val=min_val)] * len(stat_names)
        super().__init__(stat_names, generators)


class StandardDiceStatsInitializer(DiceStatsInitializer):
    """
    Standard dice rolls for stat rolling: 4D6, keeping the highest 3 as defined in the PHB page 13.
    """
    def __init__(self, stat_names=None):
        roller = DiceRoller()
        d = get_base_dice()
        super().__init__(roller, 4, d['6'], 3, 1, stat_names)


class ArrayStatsInitializer(AbstractStatsInitializer):
    """
    Generate stats from a given list of values, and validates they are a permutation of a given array.
    """
    def __init__(self, values, array, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        generators = [partial(constant_value_generator, value=value) for value in values]
        validator = partial(array_validator, array=array)
        super().__init__(stat_names, generators, validator)


class StandardArrayStatsInitializer(ArrayStatsInitializer):
    """
    Array initializer validating with the standard array as defined in the PHB page 13.
    """

    STANDARD_ARRAY = [8, 10, 12, 13, 14, 15]

    def __init__(self, values, stat_names=None):
        super().__init__(values, self.STANDARD_ARRAY, stat_names)


class PointBuyStatsInitializer(AbstractStatsInitializer):
    """
    Generates stats from a list of given values, and validates the sum of their costs equals some total.
    """
    def __init__(self, values, stat_costs, stat_total, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        generators = [partial(constant_value_generator, value=value) for value in values]
        validator = partial(cost_validator, costs=stat_costs, total=stat_total)
        super().__init__(stat_names, generators, validator)


class StandardPointBuyStatsInitializer(PointBuyStatsInitializer):
    """
    Point Buy initializer validating using the standard point buy system as defined in the PHB page 13.
    """

    STAT_COSTS = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    STAT_TOTAL = 27

    def __init__(self, values, stat_names=None):
        super().__init__(values, self.STAT_COSTS, self.STAT_TOTAL, stat_names)
