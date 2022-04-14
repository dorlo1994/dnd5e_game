from dice import dice_factory, dice_roller


def main():
    dice_factory.initialize_dice()
    roller = dice_roller.DiceRoller()
    d = dice_factory.get_base_dice()

    # EXAMPLE: Making a character randomly
    stats = ['str', 'dex', 'con', 'int', 'wis', 'cha']
    for i in range(6):
        roll = roller.roll_keep_reroll(4, d['6'], 3, 1)
        print(f"{stats[i]}:\t{roll}")


if __name__ == '__main__':
    main()
