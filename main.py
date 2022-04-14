from dice import dice_factory, dice_roller


def main():
    dice_factory.initialize_dice()
    roller = dice_roller.DiceRoller()
    d20 = dice_factory.get_dice('uniform', 20)
    roll = roller.roll_advantage(d20)
    print(roll)


if __name__ == '__main__':
    main()
