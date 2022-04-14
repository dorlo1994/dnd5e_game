from dice.dice import UniformDie

creation_functions = {}


def register(dice_type, creation_function):
    """
    Insert new dice type to the factory
    :param dice_type: String representing the die
    :param creation_function: Object creation function for that dice type
    :return:
    """
    creation_functions[dice_type] = creation_function


def get_dice(dice_type, *args, **kwargs):
    creation_function = creation_functions[dice_type]
    return creation_function(*args, **kwargs)


def initialize_dice():
    register('uniform', UniformDie)
