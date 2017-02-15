import random

from string import ascii_uppercase

def create_random_int(min, max):
    return random.randint(min,max)

def create_random_float(min,max):
    return random.uniform(min, max)

def create_random_string(length):
    return ''.join(random.choice(ascii_uppercase) for i in range(length))

