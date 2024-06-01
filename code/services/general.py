from env import IDENTIFIER_LENGTH
from random import uniform, randint, choices
from string import ascii_uppercase, digits
from math import sqrt
# import cython
import copy
from collections import defaultdict
from pprint import pprint
import orjson
from shapely.geometry import Point, Polygon

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



# Function to check if a point is inside the polygon
def is_point_inside_polygon(x, y, polygon: Polygon):
    point = Point(x, y)
    return polygon.contains(point)

"""
Generates Random Device Identifier
"""
def random_identifier():
    return "".join(choices(ascii_uppercase + digits, k=IDENTIFIER_LENGTH))


def dict_to_tuple(dictionary):
    """
    Convert dictionary to tuple of sorted (key, value) pairs.
    """
    return tuple(sorted((key, tuple(value)) for key, value in dictionary.items()))

def remove_subsets_and_duplicates(list_of_arrays):
    """
    Remove arrays that are subsets of another array and remove identical arrays.
    """
    unique_arrays = []
    for array1 in list_of_arrays:
        is_subset_flag = False
        tuple1 = dict_to_tuple(array1)
        for array2 in unique_arrays:
            tuple2 = dict_to_tuple(array2)
            if set(tuple1).issubset(set(tuple2)):
                is_subset_flag = True
                break
        if not is_subset_flag:
            unique_arrays = [arr for arr in unique_arrays if not set(dict_to_tuple(arr)).issubset(set(tuple1))]
            unique_arrays.append(array1)
    return unique_arrays

def calculate_distance_l(location1: list, location2: list):
    dx = location1[0] - location2[0]
    # print(dx)
    dy = location1[1] - location2[1]
    # print(dy)
    return sqrt(dx * dx + dy * dy)


def process_dict(data, threshold):
    segments = []
    for key, values in data.items():
        current_segment = []
        start_time, start_point = values[0]
        current_segment.append(start_point)
        
        for i in range(1, len(values)):
            next_time, next_point = values[i]
            distance = calculate_distance_l(start_point, next_point)
            
            if distance > threshold:
                print(distance, threshold)
                print(start_point, next_point)
                start_point = next_point
                current_segment.append(start_point)
        
        segments.extend(current_segment)
        # # Append the last segment if it's not empty
        # if current_segment:
        #     segments.append(current_segment)
    return segments