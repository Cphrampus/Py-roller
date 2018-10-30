import math
import random
import re

op_open_paren = "\(?"
number = "\d+"
dice_formula = number + "d" + number
die_or_number = "(?:" + dice_formula + "|" + number + ")"
math_operator = "[+*/-]"
op_close_paren = "\)?"
additional_dice = "(?:" + math_operator + op_open_paren + die_or_number + op_close_paren + ")*"
dice_pattern_string = op_open_paren + die_or_number + additional_dice


def _roll_single(die_string) -> int:
    """
    :rtype: int
    :param die_string: a string of the form xdy
    :return: the result of rolling x y-sided dice
    """
    # remove any spaces that remain
    die_string = die_string.strip(' ')

    # base case, no dice
    if re.match("^\d+$", die_string):
        return die_string
    # complex case, math, can't do here
    if re.search("[+*/-]", die_string):
        return
    number, sides = [int(r) for r in die_string.split('d')]
    total = 0
    for _ in range(number):
        total += random.randint(1, sides)
    return total


def roll(roll_string) -> int:
    """
    :rtype: int
    :param roll_string: a string containing dice values (xdy), simple math (+,-,*,/), and constants (c)
    :return: the result of evaluating the roll expression
    """
    roll_string = roll_string.replace(' ', '')

    # base case, just numbers
    if re.match("^\d+$", roll_string):
        return roll_string

    if re.match(dice_pattern_string, roll_string):
        die_strings = [x for x in re.split("\+|-|\*|/|\(|\)", roll_string) if x is not '']
    for die_string in die_strings:
        roll_string = re.sub(die_string, str(_roll_single(die_string)), roll_string)
    return math.floor(eval(roll_string))

def replace_rolls_in_string(string) -> str:
    """
    :param string: the string to replace rolls in
    :return: the string with rolls replaced with a resolved value
    """
    if not re.search("\dd\d", string):
        return string

    for die in re.findall(dice_pattern_string, string):
        # only replace the first instance, the other will be replaced as evaluated
        string = string.replace(die, str(roll(die)), 1)

    return string

print(replace_rolls_in_string("The bearer of this weapon spend a bonus action and a hit die to turn this weapon into a +1 magic weapon for 1d4 turns and is stunned for 1d6+1d4+1 rounds."))
