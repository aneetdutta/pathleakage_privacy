from random import uniform, randint, choices
from string import ascii_uppercase, digits
from env import IDENTIFIER_LENGTH, BLUETOOTH_LOCALIZATION_ERROR, WIFI_LOCALIZATION_ERROR, LTE_LOCALIZATION_ERROR
import numpy as np
from math import sqrt
# import cython
import orjson
import sys
from bson.objectid import ObjectId
import time
import copy
import pandas as pd
import polars as pl
from collections import defaultdict, deque
from funct.mongofn import MongoDB


class MyCollection:
    def __init__(self, maxlen):
        self.d = deque(maxlen=maxlen)

    def add(self, new_first_object):
        result = None if len(self.d)==0 else self.d[0]
        self.d.append(new_first_object)
        return result


def group_distances(sniffer_groups):
    
    protocol_to_id = {
        "Bluetooth": "bluetooth_id",
        "WiFi": "WiFi_id",
        "LTE": "lte_id",
    }
    
    groups = []  # Initialize list to store final groups

    '''iterate through sniffer_groups'''
    sniffer_groups: dict
    for sg in sniffer_groups:
        # print(sg)
        # print(sg["protocol"], sg[protocol_to_id[sg["protocol"]]], sg['dist_S_U'], "sg_tup")
        sg_tup = (sg["protocol"],sg[protocol_to_id[sg["protocol"]]],sg['dist_S_U'])
        if not groups:
            first_group = set()
            first_group.add(tuple(sg_tup))
            groups.append(first_group)
        incompatible_set: set = set()
        compatible_set: set = set()
        i = 0
        # print(groups, "check")
        groups: list
        while i < len(groups):
            # print(i,group)
            group = groups[i]
            # print(i, group, "check")
            compatible = True  # Flag to check if distance is compatible with the group
            group: list
            for d in group:
                abs_dist = abs(int(d[2]) - int(sg['dist_S_U']))
                # print(d, sg['WiFi_id'], abs_dist)
                if d[0] == "LTE" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "LTE" and sg["protocol"] == "WiFi" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "LTE" and sg["protocol"] == "Bluetooth" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "WiFi" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "Bluetooth" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "WiFi" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "Bluetooth" and abs_dist <= BLUETOOTH_LOCALIZATION_ERROR:
                    compatible = True
                else: 
                    compatible = False
                    # print(compatible, sg['lte_id'], sg['WiFi_id'])
                
                if compatible == True:
                    if d not in compatible_set:
                        compatible_set.add(d)
                        
                elif compatible == False:
                    if d not in incompatible_set:
                        incompatible_set.add(d)
        
            i = i+1
            
        if not compatible_set:
            fg = set()
            fg.add(tuple(sg_tup))
            groups.append(fg)
        else:
            temp_group = copy.deepcopy(groups)
            diff_checker = True
            for i, group in enumerate(groups):
                
                ''' Intersection of Compatible Set and Group - Get common items'''
                common_set = group.intersection(compatible_set)

                if not common_set:
                    continue
                diff = group - compatible_set
                if not diff:
                    temp_group[i].add(sg_tup)
                    diff_checker = False
            if diff_checker:
                compatible_set.add(sg_tup)
                temp_group.append(compatible_set)
            groups = temp_group
    
    '''
    [
        {('WiFi', 'W1', 40), ('LTE', 'L1', 40), ('LTE', 'L2', 30), ('Bluetooth', 'B1', 40)},
        {('LTE', 'L1', 40), ('WiFi', 'W2', 30), ('LTE', 'L2', 30), ('Bluetooth', 'B2', 30)},
        {('WiFi', 'W2', 30), ('LTE', 'L3', 20), ('LTE', 'L2', 30), ('Bluetooth', 'B2', 30)},
        {('WiFi', 'W3', 20), ('LTE', 'L3', 20), ('Bluetooth', 'B3', 20), ('LTE', 'L2', 30)},
        {('WiFi', 'W3', 20), ('Bluetooth', 'B3', 20), ('LTE', 'L4', 10), ('LTE', 'L3', 20)},
        {('Bluetooth', 'B4', 10), ('LTE', 'L3', 20), ('WiFi', 'W4', 10), ('LTE', 'L4', 10)}
    ]
    '''
            
    group_list:list = []
    for element in groups:
        temp_dict = dict()
        for devtup in list(element):
            if devtup[0] in {"Bluetooth", "WiFi", "LTE"}:
                # print(devtup[0], devtup[1])
                if devtup[0] not in temp_dict:
                    temp_dict[devtup[0]] = [devtup[1]]
                else:
                    temp_dict[devtup[0]].append(devtup[1])     
        group_list.append(temp_dict)       
    # defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))
    return group_list



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

def calculate_distance_df(loc1, loc2):
    return sqrt((loc1[0] - loc2[0])**2+(loc1[1] - loc2[1])**2)


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



def list_of_dicts_exists_in_list(target_list, list_of_lists):
    # Convert the target list of dicts to a set of frozensets
    target_set = {frozenset(d.items()) for d in target_list}
    
    for lst in list_of_lists:
        # Convert each list of dicts in list_of_lists to a set of frozensets
        current_set = {frozenset(d.items()) for d in lst}
        if target_set == current_set:
            return True
    return False



def D_getter(df: pl.DataFrame):
    # data_array = np.array(data)
    ''' Droping user_id as not required '''
    df = df.drop("user_id")
    ''' Calculating distance between sniffer and its sniffed user location '''
    df = df.with_columns(pl.struct(['sniffer_location', 'location']).apply(lambda x: calculate_distance_df(x['sniffer_location'], x['location']), return_dtype=pl.Float64).alias('dist_S_U'))
    ''' Droping sniffer_location and location as we have calculated the distance between '''
    df = df.drop(["sniffer_location", "location"])
    ''' Grouping by timestamp and then grouping by sniffers such that 
    Timestep | Sniffer_id | Sniffer_data
    0           0           [{},{},{}]
    0           1           [{},{},{}]   
    '''
    df = df.with_columns(pl.col('timestep').cast(pl.Utf8))
    df = df.with_columns(pl.col('sniffer_id').cast(pl.Utf8))
    df_columns, expressions = [name for name in df.columns if (name != "timestep" and name != "sniffer_id")], [pl.col(name) for name in df.columns if (name != "timestep" and name != "sniffer_id")]
    struct_data = pl.struct({name: expr for name, expr in zip(df_columns, expressions)}).alias("sniffer_data")
    df = df.select(pl.col('timestep'),pl.col('sniffer_id'),struct_data)
    df = df.to_pandas()
    grouped_df = df.groupby(['timestep', 'sniffer_id'])['sniffer_data'].apply(list).reset_index()
    ''' Grouping based on timestamp and sniffers done: th'''
    
    ''' Grouping based on distance '''
    ''' Iterating through rows and comparing distance to add them in same group - O(n2)'''
    
    print(grouped_df)
    dict_grouped = grouped_df.to_dict('records')
    

    marks_list = df['timestep'].tolist()
    print(marks_list[0:300])
    sys.exit()
    group_dict: dict[list] = {}
    old_timestep = ""
    groups = []
    datagroup = {}
    i = 0
    a = set()
    for data in dict_grouped:
        timestep = data['timestep']
        print(timestep)
        '''first timestep'''
        if not datagroup: 
            old_timestep = timestep
            datagroup[old_timestep] = []
        sniffer_groups = data['sniffer_data']

        distance_groups = group_distances(sniffer_groups)
        # print(distance_groups)
        if timestep != old_timestep:
            old_timestep = timestep
            datagroup[timestep] = [distance_groups]
        else:
            datagroup[timestep].append(distance_groups)
        if int(timestep) > 2:
            break
        
    # sys.exit()
    return datagroup
    
        # if i > 1000:
        #     break
        # i+=1
    # for index, row in grouped_df.iterrows():
    #     print(row['timestep'])
    #     if i > 100:
    #         break
    #     i = i +1
        # sniffer_groups = row['sniffer_data']
        # timestep = row['timestep']
        # distance_groups = group_distances(sniffer_groups)
        # groups.append(distance_groups)
        # if not groups:
        #     old_timestep = timestep
        # if timestep != old_timestep:
        #     group[old_timestep] = groups
        #     old_timestep = timestep
            
        # print(timestep)

    # print(group)
    sys.exit()
    # for target_time in range(0, 7200):
    #     if target_time % 100 == 0:
    #         print(target_time)
    #     lines_with_same_time = extract_lines_with_same_time(data_array, target_time)
    #     print(lines_with_same_time)
    #     break
    #     groups = group_lines_by_distance(lines_with_same_time, 0.1)
    #     location_dict[target_time] = {}
    #     for item in groups:
    #         # print(item)
    #         # List comprehension with conditional tuples
    #         # print(item)
    #         temp_dict = defaultdict(set)
    #         temp_dict1 = defaultdict()
    #         for element in item:
    #             if element["protocol"] in {"Bluetooth", "WiFi", "LTE"}:
    #                 temp_dict[element["protocol"]].add(element[protocol_to_id[element["protocol"]]])
    #                 temp_dict1[f'{element["protocol"]}_{element[protocol_to_id[element["protocol"]]]}'] = element["location"]
                    
    #         # defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))
    #         data_dict[target_time].append(defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))) 
    #         location_dict[target_time].update(temp_dict1)
    #     # print(data_dict)
    #     # print(location_dict)
    #     # break
    #     # print([target_time])
    #     # break
    # # print(data_dict)
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