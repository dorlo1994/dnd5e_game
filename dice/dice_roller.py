

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
        return self.roll_keep_reroll(num, dice, num, dice.min - 1)

    def roll_keep_reroll(self, num, dice, keep, min_val) -> int:
        """
        Rolls <num>d<roll>, keep highest <keep> rolls and reroll on <min_val> or less.
        :param num: Number of rolls
        :param dice: Dice to roll
        :param keep: Number of highest rolls to keep
        :param min_val: Lowest number to reroll on.
        :return: Result of roll
        """
        results = [dice.roll(min_val=min_val) for _ in range(num)]
        results.sort()
        highest_k = results[0:keep]
        return sum(highest_k)

    def roll_advantage(self, dice):
        """
        Rolls with advantage.
        :param dice: Dice to roll
        :return: Max of two rolls.
        """
        return max(self.base_roll(1, dice), self.base_roll(1, dice))

    def roll_disadvantage(self, dice):
        """
        Rolls with disadvantage.
        :param dice: Dice to roll
        :return: Max of two rolls.
        """
        return min(self.base_roll(1, dice), self.base_roll(1, dice))
