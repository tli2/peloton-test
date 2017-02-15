import random

from string import ascii_uppercase


def create_random_int(lower, upper):
    return random.randint(lower, upper)


def create_random_float(lower, upper):
    return random.uniform(lower, upper)


def create_random_string(length):
    return ''.join(random.choice(ascii_uppercase) for i in range(length))
