from dice.dice import UniformDie

creation_functions = {}

BASE_DICE = [4,
             6,
             8,
             10,
             100,
             12,
             20]


def register(die_type, creation_function):
    """
    Insert new dice type to the factory
    :param die_type: String representing the die
    :param creation_function: Object creation function for that dice type
    :return:
    """
    creation_functions[die_type] = creation_function


def get_die(die_type, *args, **kwargs):
    creation_function = creation_functions[die_type]
    return creation_function(*args, **kwargs)


def initialize_dice():
    register('uniform', UniformDie)


def get_base_dice() -> dict:
    """
    Returns a dict containing a set of standard D&D dice:
    D4, D6, D8, D10, D100 (A.K.A D%), and D20
    """
    return {f'{d}': get_die('uniform', d, f'D{d}') for d in BASE_DICE}
