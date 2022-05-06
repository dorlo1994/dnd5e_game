import abc

from collections import namedtuple
from dice import dice_factory, dice_roller
from functools import partial


STANDARD_STAT_NAMES = ['str',
                       'dex',
                       'con',
                       'int',
                       'wis',
                       'cha']


class Stat:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def modifier(self):
        return (self.value - 10) // 2

    def increment(self):
        self.value += 1

    def __repr__(self):
        return f"{self.modifier} ({self.value})"


class Stats:
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


class AbstractValueGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_value(self):
        ...


class ConstantValueGenerator(AbstractValueGenerator):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def generate_value(self):
        return self._value


class RandomValueGenerator(AbstractValueGenerator):
    def __init__(self, roller, dice_count, dice_type, reroll, min_val):
        super().__init__()
        self._roller = roller
        self._dice_count = dice_count
        self._dice_type = dice_type
        self._reroll = reroll
        self._min_val = min_val

    def generate_value(self):
        return self._roller.roll_keep_reroll(self._dice_count, self._dice_type, self._reroll, self._min_val)[0]


def universal_validator(stats):
    return True


def array_validator(stats, array):
    expected_array = array.copy()
    stat_iter = iter(stats)
    for s in stat_iter:
        if s.value not in expected_array:
            raise ValueError(f"Stat value {s.value} not in given array.")
        expected_array.remove(s.value)
    return True


def cost_validator(stats, costs, total):
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
        generated_stats = [Stat(g.name, g.value_generator.generate_value()) for g in self.generators]
        self.validate(generated_stats)
        return Stats(generated_stats)

    def validate(self, stats):
        self.validator(stats)


class StandardDiceStatsInitializer(AbstractStatsInitializer):
    def __init__(self, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        roller = dice_roller.DiceRoller()
        d = dice_factory.get_base_dice()
        generators = [RandomValueGenerator(roller, 4, d['6'], 3, 1)] * len(stat_names)
        super().__init__(stat_names, generators)


class ArrayStatsInitializer(AbstractStatsInitializer):
    def __init__(self, values, array, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        generators = [ConstantValueGenerator(value) for value in values]
        validator = partial(array_validator, array=array)
        super().__init__(stat_names, generators, validator)


class StandardArrayStatsInitializer(ArrayStatsInitializer):

    STANDARD_ARRAY = [8, 10, 12, 13, 14, 15]

    def __init__(self, values, stat_names=None):
        super().__init__(values, self.STANDARD_ARRAY, stat_names)


class PointBuyStatsInitializer(AbstractStatsInitializer):
    def __init__(self, values, stat_costs, stat_total, stat_names=None):
        if not stat_names:
            stat_names = STANDARD_STAT_NAMES
        generators = [ConstantValueGenerator(value) for value in values]
        validator = partial(cost_validator, costs=stat_costs, total=stat_total)
        super().__init__(stat_names, generators, validator)


class StandardPointBuyStatsInitializer(PointBuyStatsInitializer):

    STAT_COSTS = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    STAT_TOTAL = 27

    def __init__(self, values, stat_names=None):
        super().__init__(values, self.STAT_COSTS, self.STAT_TOTAL, stat_names)
