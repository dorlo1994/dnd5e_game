from dice import dice_factory, dice_roller


def main():
    dice_factory.initialize_dice()
    roller = dice_roller.DiceRoller()
    D = dice_factory.get_base_dice()
    for i in range(10):
        roll = roller.roll_advantage(D['20'])
        print(roll)
    print(roller.get_history())


if __name__ == '__main__':
    main()
