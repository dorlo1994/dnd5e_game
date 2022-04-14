import itertools

class DiceRoller:
    def __init__(self):
        ...

    def base_roll(self, num, dice) -> int:
        """
        Rolls <num>d<dice>.
        :param num: Number of rolls
        :param dice: Dice to roll
        :return: Sum of rolls
        """
        return self.roll_keep_reroll(num, dice, num, dice.min() - 1)

    def roll_keep_reroll(self, num, dice, keep, reroll) -> int:
        """
        Rolls <num>d<roll>, keep highest <keep> rolls and reroll on <reroll> or less.
        :param num: Number of rolls
        :param dice: Dice to roll
        :param keep: Number of highest rolls to keep
        :param reroll: Lowest number to reroll on.
        :return: Result of roll
        """
        results = list(list(itertools.repeat(dice.roll(reroll=reroll), num)))
        results.sort()
        highest_k = results[:-keep]
        return sum(highest_k)