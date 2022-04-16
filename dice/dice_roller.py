from dice.dice import BaseDie, DieRollSet


class RollHistory:
    def __init__(self, limit: int):
        self._limit = limit
        self._data = []

    def inset(self, roll: DieRollSet):
        if len(self._data) == self._limit:
            self._data = [roll] + self._data[:-1]
        else:
            self._data = [roll] + self._data

    def get_data(self):
        return self._data.copy()

    def __repr__(self):
        repr_str = f'Roll History up to {self._limit} last rolls:\n'
        repr_str += '\n'.join([str(roll_set) for roll_set in self._data])
        return repr_str


class DiceRoller:
    """
    Dice roller class, keeps a history of rolls.
    """

    HISTORY_LIMIT_DEFAULT = 5

    def __init__(self, history_limit: int = HISTORY_LIMIT_DEFAULT):
        self._history = RollHistory(history_limit)

    def base_roll(self, num: int, die: BaseDie, save_result: bool = True) -> (int, DieRollSet):
        """
        Rolls <num>d<dice>.
        :param num: Number of rolls
        :param die: Die to roll
        :param save_result: Set to true to save result in history.
        :return: Sum of rolls
        """
        return self.roll_keep_reroll(num, die, num, die.min - 1, save_result)

    def roll_keep_reroll(self, num: int, die: BaseDie, keep: int, min_val: int, save_result: bool = True) -> (int, DieRollSet):
        """
        Rolls <num>d<roll>, keep highest <keep> rolls and reroll on <min_val> or less.
        :param num: Number of rolls
        :param die: Die to roll
        :param keep: Number of highest rolls to keep
        :param min_val: Lowest number to reroll on.
        :param save_result: Set to true to save result in history.
        :return: Result of roll and the Dice rolled
        """
        results = [die.roll(min_val=min_val) for _ in range(num)]
        results.sort()
        highest_k = results[0:keep]
        roll_set = DieRollSet(highest_k)
        if save_result:
            self._history.inset(roll_set)
        return roll_set.value, roll_set

    def roll_advantage(self, die: BaseDie) -> int:
        """
        Rolls with advantage.
        :param die: Die to roll
        :return: Max of two rolls.
        """
        total_a, roll_a = self.base_roll(1, die, save_result=False)
        total_b, roll_b = self.base_roll(1, die, save_result=False)
        self._history.inset(roll_a)
        self._history.inset(roll_b)
        return max(total_a, total_b)

    def roll_disadvantage(self, die: BaseDie) -> int:
        """
        Rolls with disadvantage.
        :param die: Die to roll
        :return: Max of two rolls.
        """
        total_a, roll_a = self.base_roll(1, die, save_result=False)
        total_b, roll_b = self.base_roll(1, die, save_result=False)
        self._history.inset(roll_a)
        self._history.inset(roll_b)
        return min(total_a, total_b)

    def get_history(self):
        return self._history
