from env import IDENTIFIER_LENGTH
from random import uniform, randint, choices
from string import ascii_uppercase, digits
from math import sqrt
# import cython
import copy
from pprint import pprint
from modules.mongofn import MongoDB
import orjson

def convert_sets_to_lists(d):
    d1 = copy.deepcopy(d)
    for k, v in d1.items():
        if isinstance(v, set):
            d1[k] = list(v)
        elif isinstance(v, dict):
            convert_sets_to_lists(v)
    return d1


# data_array = pd.DataFrame(data)
def extract_orjson(filename):
    with open(filename, 'rb') as f:
        return orjson.loads(f.read())

"""
Generates Random Device Identifier
"""
def random_identifier():
    return "".join(choices(ascii_uppercase + digits, k=IDENTIFIER_LENGTH))

