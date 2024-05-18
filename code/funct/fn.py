from random import uniform, randint, choices
from string import ascii_uppercase, digits
from env import IDENTIFIER_LENGTH
import numpy as np
from math import sqrt
# import cython
import orjson
import pandas as pd
import polars as pl
from collections import defaultdict, deque



class MyCollection:
    def __init__(self, maxlen):
        self.d = deque(maxlen=maxlen)

    def add(self, new_first_object):
        result = None if len(self.d)==0 else self.d[0]
        self.d.append(new_first_object)
        return result

# data_array = pd.DataFrame(data)
def extract_orjson(filename):
    with open(filename, 'rb') as f:
        return orjson.loads(f.read())

def extract_json(filename):
    # with open(filename, 'rb') as f:
    #     # return pd.DataFrame(orjson.loads(f.read()))
    #     return 
    return pl.read_json(filename)


def json_read_process(filename):
    with open(filename, 'rb') as f:
        j = orjson.loads(f.read())
    return [pl.DataFrame(k) for i, k in j.items()]


def id_to_location_link(filename):
    with open(filename, 'rb') as f:
        j = orjson.loads(f.read())

"""
Generates Random Device Identifier
"""
def random_identifier():
    return "".join(choices(ascii_uppercase + digits, k=IDENTIFIER_LENGTH))

"""
Euclidean Distance
"""
def calculate_distance(line1: dict, line2: dict):
    dx = line1["location"][0] - line2["location"][0]
    dy = line1["location"][1] - line2["location"][1]
    return sqrt(dx * dx + dy * dy)

def calculate_distance_l(location1: list, location2: list):
    dx = location1[0] - location2[0]
    dy = location1[1] - location2[1]
    return sqrt(dx * dx + dy * dy)

def group_lines_by_distance(lines: pd.DataFrame, threshold_distance):
    groups = []
    line: dict
    for line in lines:
        distance_threshold_lte = 10
        distance_threshold = 1
        added_to_existing_group = False
        lte = False
        list2 = []
        group: list
        for group in groups:
            line_in_group: dict
            for line_in_group in group:
                distance = calculate_distance(line, line_in_group)
                # print(line, line_in_group)
                # break
                if (
                    distance <= distance_threshold_lte
                    and distance <= distance_threshold
                ):
                    group.append(line)
                    added_to_existing_group = True
                    break
                elif (
                    distance <= distance_threshold_lte and distance > distance_threshold
                ):
                    if line["protocol"] == "LTE":
                        group.append(line)
                        added_to_existing_group = True
                    elif line_in_group["protocol"] == "LTE":
                        list2.append(line_in_group)
                        lte = True
                        added_to_existing_group = False
            if added_to_existing_group:
                continue
        # If the line does not fit into any existing group, create a new group
        if not added_to_existing_group and not lte:
            groups.append([line])
        if not added_to_existing_group and lte:
            list2.append(line)
            groups.append(list2)
    return groups


def extract_lines_with_same_time(data: pl.DataFrame, target_time):
    return data.filter(pl.col('timestep') == target_time).to_dicts()

def D_getter(data_array: pl.DataFrame):
    # data_array = np.array(data)
    protocol_to_id = {
        "Bluetooth": "bluetooth_id",
        "WiFi": "WiFi_id",
        "LTE": "lte_id",
    }
    target_time = 0
    data_dict = defaultdict(list)
    location_dict = defaultdict(list)
    for target_time in range(0, 7200):
        if target_time % 100 == 0:
            print(target_time)
        lines_with_same_time = extract_lines_with_same_time(data_array, target_time)
        groups = group_lines_by_distance(lines_with_same_time, 0.1)
        location_dict[target_time] = {}
        for item in groups:
            # print(item)
            # List comprehension with conditional tuples
            # print(item)
            temp_dict = defaultdict(set)
            temp_dict1 = defaultdict()
            for element in item:
                if element["protocol"] in {"Bluetooth", "WiFi", "LTE"}:
                    temp_dict[element["protocol"]].add(element[protocol_to_id[element["protocol"]]])
                    temp_dict1[f'{element["protocol"]}_{element[protocol_to_id[element["protocol"]]]}'] = element["location"]
                    
            # defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))
            data_dict[target_time].append(defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))) 
            location_dict[target_time].update(temp_dict1)
        # print(data_dict)
        # print(location_dict)
        # break
        # print([target_time])
        # break
    # print(data_dict)
    return data_dict, location_dict


def generate_traces(bluetooth_id,wifi_id,lte_id, data: list, linked_ids, tracking: list):
    flag=0
    print("hi")
    for line in data:
        if line['protocol']=='Bluetooth' and line['bluetooth_id']==bluetooth_id:
            #print(line)
            tracking.append(line['timestep'])
            #r.append(bluetooth_id)
        if line['protocol']=='WiFi' and line['WiFi_id']==wifi_id:
            #print(line)
            #r.append(wifi_id)
            tracking.append(line['timestep'])
        if line['protocol']=='LTE' and line['lte_id']==lte_id:
            #print(line)
            tracking.append(line['timestep'])
            #r.append(lte_id)
        
    if lte_id in linked_ids:
        # print(lte_id)s
        lte_id=linked_ids[lte_id]
        # print(lte_id)
        flag=1
        
    if bluetooth_id in linked_ids:
        # print(bluetooth_id)
        bluetooth_id=linked_ids[bluetooth_id]  
        # print(bluetooth_id)
        flag=1
        
    if wifi_id in linked_ids:
        # print(wifi_id)
        wifi_id=linked_ids[wifi_id]
        # print(wifi_id)
        flag=1
        
    if flag==1:
        generate_traces(bluetooth_id,wifi_id,lte_id)
    else:
        return
        
        


# def group_lines_by_field(timed_data, sniffer_id, specific_values):
#     # groups = {}
#     groups = [[] for _ in range(len(specific_values))]
#     for line in timed_data:
#         # print(line)
#         if sniffer_id in line and line[sniffer_id] in specific_values:
#             index = specific_values.index(line[sniffer_id])
#             groups[index].append(line)

#     return groups






# def generate_traces(bluetooth_id, wifi_id, lte_id):
#     flag = 0
#     for line in data:
#         if line["protocol"] == "Bluetooth" and line["bluetooth_id"] == bluetooth_id:
#             tracking.append(line["timestep"])
#         if line["protocol"] == "WiFi" and line["WiFi_id"] == wifi_id:
#             tracking.append(line["timestep"])
#         if line["protocol"] == "LTE" and line["lte_id"] == lte_id:
#             tracking.append(line["timestep"])
#     for key, value in linked_ids.items():
#         if value == lte_id:
#             lte_id = str(key)
#             # print(lte_id)
#             flag = 1

#         if value == bluetooth_id:
#             bluetooth_id = str(key)
#             flag = 1

#         if value == wifi_id:
#             wifi_id = str(key)
#             flag = 1

#     if flag == 1:
#         generate_traces(bluetooth_id, wifi_id, lte_id)
#     else:
#         return