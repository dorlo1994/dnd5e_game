import abc

from collections import namedtuple
from dice import dice_factory, dice_roller


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


class ValueGenerator:
    def __init__(self, generator):
        self.generator = generator

    def generate_value(self):
        return self.generator()


class ConstantValueGenerator(ValueGenerator):
    def __init__(self, value):
        def generate_const(): return value
        super().__init__(generate_const)


class RandomValueGenerator(ValueGenerator):
    def __init__(self, roller, dice_count, dice_type, reroll, min_val):
        def roll(): return roller.roll_keep_reroll(dice_count, dice_type, reroll, min_val)[0]
        super().__init__(roll)


class AbstractStatsInitializer(abc.ABC):

    StatGenerator = namedtuple('StatGenerator', ['name', 'value_generator'])

    def __init__(self, names, value_generators):
        assert len(names) == len(value_generators), f"Given {len(names)} names but {len(value_generators)} generators!"
        self.generators = [self.StatGenerator(names[i], value_generators[i]) for i in range(len(names))]

    def _generate(self):
        """
        Iterates over the generators and fixes a value to them.
        :return: A Stats object with the generated stats.
        """
        generated_stats = [Stat(g.name, g.value_generator.generate_value()) for g in self.generators]
        return Stats(generated_stats)

    @abc.abstractmethod
    def generate(self):
        """
        Abstract method to wrap _generate(self).
        :return: A Stats object with the generated stats.
        """
        ...


class StandardDiceStatsInitializer(AbstractStatsInitializer):
    def __init__(self):
        roller = dice_roller.DiceRoller()
        d = dice_factory.get_base_dice()
        generators = [RandomValueGenerator(roller, 4, d['6'], 3, 1)] * len(STANDARD_STAT_NAMES)
        super().__init__(STANDARD_STAT_NAMES, generators)

    def generate(self):
        return self._generate()


class StandardArrayStatsInitializer(AbstractStatsInitializer):

    STANDARD_ARRAY = [8, 10, 12, 13, 14, 15]

    def __init__(self, values):
        generators = [ConstantValueGenerator(value) for value in values]
        super().__init__(STANDARD_STAT_NAMES, generators)

    def generate(self):
        stats = self._generate()
        expected_array = self.STANDARD_ARRAY.copy()
        stat_iter = iter(stats)
        for s in stat_iter:
            if s.value not in expected_array:
                raise ValueError(f"Stat value {s.value} not in standard array.")
            expected_array.remove(s.value)
        return stats


class StandardPointBuyStatsInitializer(AbstractStatsInitializer):

    STAT_COSTS = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    STAT_TOTAL = 27

    def __init__(self, values):
        generators = [ConstantValueGenerator(value) for value in values]
        super().__init__(STANDARD_STAT_NAMES, generators)

    def generate(self):
        """
        Assuming you have to use ALL available points
        """
        stats = self._generate()
        stat_iter = iter(stats)
        total_cost = 0
        for s in stat_iter:
            cost = self.STAT_COSTS.get(s.value)
            if cost is None:
                raise ValueError(f"Got invalid stat value {s.value}")
            total_cost += cost
        if total_cost != self.STAT_TOTAL:
            raise ValueError(f"Total cost is {total_cost}, should be {self.STAT_TOTAL}")
        return stats
