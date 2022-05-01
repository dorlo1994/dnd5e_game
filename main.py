from dice import dice_factory
from entity.utils.stats import StandardDiceStatsInitializer, StandardPointBuyStatsInitializer, \
    StandardArrayStatsInitializer


def main():
    dice_factory.initialize_dice()
    rand_stats = StandardDiceStatsInitializer()
    point_buy = StandardPointBuyStatsInitializer([15, 15, 14, 10, 8, 8])
    standard_array = StandardArrayStatsInitializer([12, 10, 15, 13, 14, 8])

    print(rand_stats.generate())
    print(point_buy.generate())
    print(standard_array.generate())


if __name__ == '__main__':
    main()
