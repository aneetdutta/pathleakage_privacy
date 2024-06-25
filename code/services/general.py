from random import choices
from string import ascii_uppercase, digits
from math import sqrt
import os
# import cython
import numpy as np
import copy
from collections import defaultdict
from pprint import pprint
import orjson
import pandas as pd
import yaml
from shapely.geometry import Point, Polygon
import concurrent.futures

class UnionFind:
    def __init__(self):
        self.parent = {}
    
    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]
    
    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        if root1 != root2:
            self.parent[root2] = root1
    
    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item

def group_identifiers(tuples_list):
    uf = UnionFind()
    
    for i, time_epoch, type_, identifiers, ta in tuples_list:
        identifiers = list(identifiers)
        for identifier in identifiers:
            uf.add(identifier)
        for i in range(1, len(identifiers)):
            uf.union(identifiers[0], identifiers[i])
    
    groups = {}
    for identifier in uf.parent:
        root = uf.find(identifier)
        if root not in groups:
            groups[root] = set()
        groups[root].add(identifier)
    
    return list(groups.values())

# def group_identifiers(tuples_list):
#     groups = []
#     identifier_to_group = {}

#     for i, time_epoch, type_, identifiers, ta in tuples_list:
#         current_group = None
        
#         # Find the group for the current tuple
#         for identifier in identifiers:
#             if identifier in identifier_to_group:
#                 current_group = identifier_to_group[identifier]
#                 break
        
#         # If no existing group is found, create a new one
#         if current_group is None:
#             current_group = len(groups)
#             groups.append(set())
        
#         # Add the identifiers to the found/created group
#         groups[current_group].update(identifiers)
        
#         # Update the identifier to group mapping
#         for identifier in identifiers:
#             identifier_to_group[identifier] = current_group

#     # Convert sets to lists for the final output
#     return [set(group) for group in groups]

IDENTIFIER_LENGTH = os.getenv("IDENTIFIER_LENGTH")

def str_to_bool(s):
    return {'true': True, 'false': False}.get(s.strip().lower(), None)

def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def set_env_from_config(section, config):
    for key, value in config.get(section, {}).items():
        if isinstance(value, list):
            # Convert list (e.g., list of lists) to a string representation
            os.environ[key] = str(value)
        else:
            os.environ[key] = str(value)


def remove_subsets_and_merge(data):
    result = []
    for key, value in data.items():
        chain = [key] + value
        chain_set = set(chain)
        # Check if the chain is a subset of any existing chain or if it intersects with any existing chain
        subset = next((existing for existing in result if chain_set.issubset(set(existing))), None)
        intersection = next((existing for existing in result if chain_set.intersection(set(existing))), None)
        if subset:
            continue  # Skip if the chain is a subset of an existing chain
        elif intersection:
            # Merge the chains and remove the old ones
            result = [list(set(existing + chain)) if existing == intersection else existing for existing in result]
        else:
            result.append(chain)
    return result


def get_list_containing_value(merged_data, value):
    for chain in merged_data:
        if value in chain:
            return chain
    return None



def calculate_privacy_score(row):
    if row['duration'] == 0 and row['ideal_duration'] == 0:
        return 1
    else:
        return row['duration'] / row['ideal_duration']

def process_mappings(m1, m2, visited_intra_list):
    local_intra_potential_mapping = defaultdict(set)
    for p1, ids1 in m1.items():
        ''' Comparing with only same protocol types during intra mapping'''
        if p1 not in m2:
            continue
        ids1_set = set(ids1)
        ids2_set = set(m2[p1])
        
        if ids1_set.intersection(ids2_set):
            t0_1 = ids1_set - ids2_set
            t1_0 = ids2_set - ids1_set
        
            if t0_1 and t1_0:
                for i in t0_1:
                    common_set_for_i = visited_intra_list[i].intersection(t1_0)
                    not_common_set = t1_0 - common_set_for_i
                    # local_intra_potential_mapping[i] = set(local_intra_potential_mapping[i])
                    local_intra_potential_mapping[i].update(not_common_set) 
                     
    return local_intra_potential_mapping

def optimized_mapping_comparison(mapping0, mapping1, visited_intra_list, intra_potential_mapping):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_mapping = {
            executor.submit(process_mappings, m1, m2, visited_intra_list): (m1, m2)
            for m1 in mapping0 for m2 in mapping1
        }

        for future in concurrent.futures.as_completed(future_to_mapping):
            result = future.result()
            for key, value in result.items():
                if key not in intra_potential_mapping:
                    intra_potential_mapping[key] = set()
                intra_potential_mapping[key].update(value)
                
    return visited_intra_list, intra_potential_mapping
                
def combine_values(dicts, keys):
    # Initialize a dictionary to hold combined sets for each key
    combined_dict = {key: set() for key in keys}
    
    # Combine values for each key from all dictionaries
    for d in dicts:
        for key in keys:
            combined_dict[key].update(d.get(key, []))
    
    return combined_dict

def create_exclusion_set(combined_set, element):
    return {item for item in combined_set if item != element}

def combine_and_exclude_all(dicts, keys, result_dict=None):
    # Initialize a dictionary to hold combined sets for each key
    combined_dict = {key: set() for key in keys}
    
    # print(dicts, keys)
    # Combine values for each key from all dictionaries
    for d in dicts:
        # print(d)
        for key in keys:
            combined_dict[key].update(d.get(key, []))
        # print(combined_dict, key)
    
    # Initialize result_dict if not provided
    if result_dict is None:
        result_dict = {}
    else:
        # Ensure existing result_dict values are sets
        for key in result_dict:
            result_dict[key] = set(result_dict[key])
    
    # Create the final dictionary with each element as key and the set without that element as value
    for key in keys:
        combined_list = list(combined_dict[key])
        for element in combined_list:
            exclusion_set = {item for item in combined_list if item != element}
            if element not in result_dict:
                result_dict[element] = exclusion_set
            else:
                result_dict[element].update(exclusion_set)
    
    # Convert sets back to lists for the final result
    # result_dict = {key: list(value) for key, value in result_dict.items()}
    
    return result_dict

# def combine_and_exclude_all(dicts, keys, result_dict=None):
#     combined_dict = combine_values(dicts, keys)
    
#     if result_dict is None:
#         result_dict = {}
#     else:
#         # Ensure existing result_dict values are sets
#         for key in result_dict:
#             result_dict[key] = set(result_dict[key])
    
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_to_element = {}
        
#         for key in keys:
#             combined_set = combined_dict[key]
#             for element in combined_set:
#                 future = executor.submit(create_exclusion_set, combined_set, element)
#                 future_to_element[future] = element
        
#         for future in concurrent.futures.as_completed(future_to_element):
#             element = future_to_element[future]
#             exclusion_set = future.result()
#             if element not in result_dict:
#                 result_dict[element] = exclusion_set
#             else:
#                 result_dict[element].update(exclusion_set)
    
#     # Convert sets back to lists for the final result
#     result_dict = {key: value for key, value in result_dict.items()}
    
#     return result_dict

def remove_subsets(chains):
    chains_copy = sorted(chains, key=len, reverse=True)
    subsets_removed = []
    for chain in chains_copy:
        if not any(set(chain).issubset(set(other)) for other in subsets_removed):
            subsets_removed.append(chain)
    return subsets_removed

def remove_subsets_group(sets):
    # Sort the list of sets by length in descending order
    sets = sorted(sets, key=len, reverse=True)
    unique_sets = []

    for current_set in sets:
        is_subset = False
        for unique_set in unique_sets:
            if current_set.issubset(unique_set):
                is_subset = True
                break
        if not is_subset:
            unique_sets.append(current_set)

    return unique_sets

def build_chain_for_key(current_key, current_chain:list, visited: set, data: dict, all_chains, user_id):
    if current_key in visited:
        return

    visited.add(current_key)
    current_chain.append(current_key)

    result = data.get(current_key)
    if result:
        # print(result, "result")
        next_key, next_user_id = result
    else:
        next_key, next_user_id = None, None
        
    if next_user_id != user_id and next_user_id and next_key:
        current_chain.remove(current_key)
        
    if next_key and user_id==next_user_id:
        build_chain_for_key(next_key, current_chain.copy(), visited.copy(), data, all_chains, user_id=user_id)
    else:
        all_chains.append(current_chain.copy())

def find_chain_for_key(data, start_key, user_id):
    all_chains = []
    build_chain_for_key(start_key, [], set(), data, all_chains, user_id)
    return remove_subsets(all_chains)

def convert_sets_to_lists(d):
    d1 = copy.deepcopy(d)
    for k, v in d1.items():
        if isinstance(v, set):
            d1[k] = list(v)
        elif isinstance(v, dict):
            convert_sets_to_lists(v)
    return d1


def serialize_floats(obj):
    if isinstance(obj, np.float64):
        return float(obj)
    return obj

# data_array = pd.DataFrame(data)
def extract_orjson(filename):
    with open(filename, 'rb') as f:
        return orjson.loads(f.read())


def dump_orjson(filename, data):
    with open(filename, "wb") as f:
        f.write(orjson.dumps(data, default=serialize_floats))
    

# Function to check if a point is inside the polygon
def is_point_inside_polygon(x, y, polygon: Polygon):
    point = Point(x, y)
    return polygon.contains(point)

"""
Generates Random Device Identifier
"""
def random_identifier():
    return "".join(choices(ascii_uppercase + digits, k=int(IDENTIFIER_LENGTH)))


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


class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0