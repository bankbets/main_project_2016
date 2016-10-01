import random, os


def roll(user, amt):

    theroll = random.randint(1, 100)
    if theroll > 54:
        return True
    return False