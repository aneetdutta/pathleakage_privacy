from random import uniform, randint, choices
from string import ascii_uppercase, digits
from env import IDENTIFIER_LENGTH
import numpy as np
from math import sqrt
# import cython
import orjson
import pandas as pd
import polars as pl
from collections import defaultdict


# data_array = pd.DataFrame(data)

def extract_json(filename):
    # with open(filename, 'rb') as f:
    #     # return pd.DataFrame(orjson.loads(f.read()))
    #     return 
    return pl.read_json(filename)


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

    for target_time in range(0, 7200):
        if target_time % 100 == 0:
            print(target_time)
            
        lines_with_same_time = extract_lines_with_same_time(data_array, target_time)
        groups = group_lines_by_distance(lines_with_same_time, 0.1)
        for item in groups:
            # List comprehension with conditional tuples
            l = list({
                (element["protocol"], element[protocol_to_id[element["protocol"]]])
                for element in item
                if element["protocol"] in {"Bluetooth", "WiFi", "LTE"}
            })
            data_dict[target_time].append(l)      
    return data_dict

# def group_lines_by_field(timed_data, sniffer_id, specific_values):
#     # groups = {}
#     groups = [[] for _ in range(len(specific_values))]
#     for line in timed_data:
#         # print(line)
#         if sniffer_id in line and line[sniffer_id] in specific_values:
#             index = specific_values.index(line[sniffer_id])
#             groups[index].append(line)

#     return groups



# def elimination(mapping, line1, line2):
#     sa_1 = []
#     sb_1 = []
#     sc_1 = []
#     for item in line1:
#         if item[0] == "Bluetooth":
#             sa_1.append(item[1])
#         elif item[0] == "WiFi":
#             sb_1.append(item[1])
#         elif item[0] == "LTE":
#             sc_1.append(item[1])

#     sa_2 = []
#     sb_2 = []
#     sc_2 = []

#     for item in line2:
#         if item[0] == "Bluetooth":
#             sa_2.append(item[1])
#         elif item[0] == "WiFi":
#             sb_2.append(item[1])
#         elif item[0] == "LTE":
#             sc_2.append(item[1])

#     l = list(set(sa_1) - set(mapping))
#     l1 = list(set(sa_2).intersection(set(l)))

#     l2 = list(set(sb_1) - set(mapping))
#     l3 = list(set(sb_2).intersection(set(l2)))

#     l4 = list(set(sc_1) - set(mapping))
#     l5 = list(set(sc_2).intersection(set(l4)))

#     if len(l1) == 0:
#         if len(l3) == 1 and len(l5) == 1:
#             print(l3[0], l5[0])
#     else:
#         if len(l3) == 1 and len(l5) == 1 and len(l1) == 1:
#             print(l1[0], l3[0], l5[0])


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