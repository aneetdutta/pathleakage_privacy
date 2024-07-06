import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.general import remove_subsets_and_duplicates, remove_subsets_group, str_to_bool
from collections import defaultdict, deque
from itertools import product
import sys


def group_distances(sniffer_groups, incompatible_intra_ids: defaultdict[set], incompatible_inter_ids: defaultdict[set]):    
    BLUETOOTH_LOCALIZATION_ERROR = int(os.getenv("BLUETOOTH_LOCALIZATION_ERROR", 1))
    WIFI_LOCALIZATION_ERROR = int(os.getenv("WIFI_LOCALIZATION_ERROR", 5))
    LTE_LOCALIZATION_ERROR = int(os.getenv("LTE_LOCALIZATION_ERROR", 10))
    MAX_MOBILITY_FACTOR = float(os.getenv("MAX_MOBILITY_FACTOR", 1.66))
    ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH", "false"))
    
    # print(BLUETOOTH_LOCALIZATION_ERROR, WIFI_LOCALIZATION_ERROR, LTE_LOCALIZATION_ERROR, MAX_MOBILITY_FACTOR)
    
    groups = []  # Initialize list to store final groups
    incompatible_intra_ids = defaultdict(set, incompatible_intra_ids)
    incompatible_inter_ids = defaultdict(set, incompatible_inter_ids)
    '''iterate through sniffer_groups'''
    updated_timestep_dict = defaultdict()
    dist_dict = defaultdict()
    sniffer_groups: dict
    for sg in sniffer_groups:
        if sg["id"] not in incompatible_intra_ids: incompatible_intra_ids[sg["id"]] = set()
        if sg["id"] not in incompatible_inter_ids: incompatible_inter_ids[sg["id"]] = set()
        # print(sg)
        updated_timestep_dict[sg["id"]] = sg['timestep']
        dist_dict[sg["id"]] = sg['dist_S_U']
        sg_tup = (sg["protocol"],sg["id"])
        
        if not groups:
            first_group = set()
            first_group.add(tuple(sg_tup))
            groups.append(first_group)
        else:
            # incompatible_set: set = set()
            compatible_set: set = set()
            i = 0
            groups: list
            while i < len(groups):
                # print(groups, i)
                # print("hello")
                # print(i,group)
                group = set(groups[i])
                # print(i, group, "check")
                compatible = True  # Flag to check if distance is compatible with the group
                group: list
                for d in group:
                    abs_dist = abs(int(dist_dict[d[1]]) - int(sg['dist_S_U']))
                    mobility_error = abs(int(updated_timestep_dict[d[1]]) - int(sg['timestep']))*MAX_MOBILITY_FACTOR
                    
                    if d[0] == "LTE" and sg["protocol"] == "WiFi" and abs_dist <= (LTE_LOCALIZATION_ERROR + WIFI_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    elif d[0] == "LTE" and sg["protocol"] == "Bluetooth" and abs_dist <= (LTE_LOCALIZATION_ERROR+BLUETOOTH_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    elif d[0] == "WiFi" and sg["protocol"] == "LTE" and abs_dist <= (LTE_LOCALIZATION_ERROR + WIFI_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    elif d[0] == "WiFi" and sg["protocol"] == "Bluetooth" and abs_dist <= (WIFI_LOCALIZATION_ERROR+BLUETOOTH_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    elif d[0] == "Bluetooth" and sg["protocol"] == "LTE" and abs_dist <= (LTE_LOCALIZATION_ERROR+BLUETOOTH_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    elif d[0] == "Bluetooth" and sg["protocol"] == "WiFi" and abs_dist <= (WIFI_LOCALIZATION_ERROR+BLUETOOTH_LOCALIZATION_ERROR + mobility_error):
                        compatible = True
                    else: 
                        compatible = False

                    if compatible:
                        if not incompatible_inter_ids[sg["id"]].intersection({d[1]}) or incompatible_intra_ids[sg["id"]].intersection({d[1]}):
                            compatible_set.add(d)
                    else:
                        if sg["id"] != d[1]:
                            if sg["protocol"] != d[0]:
                                incompatible_inter_ids[sg["id"]].add(d[1])
                                incompatible_inter_ids[d[1]].add(sg["id"])
                            else:
                                incompatible_intra_ids[sg["id"]].add(d[1])
                                incompatible_intra_ids[d[1]].add(sg["id"])

                if sg_tup in group and not compatible:
                    # print(sg_tup, group, compatible)
                    group.remove(sg_tup)
                    groups[i] = group
                    
                i = i+1
                
            if not compatible_set:
                groups.append(set({tuple(sg_tup)}))
            else:
                compatible_set.add(sg_tup)
                protocol_dict = {}
                for protocol, id in compatible_set:
                    if protocol not in protocol_dict:
                        protocol_dict[protocol] = []
                    protocol_dict[protocol].append((protocol, id))
                # Generate all combinations of distinct protocols
                combinations = [set(combo) for combo in product(*protocol_dict.values())]
                groups.extend(combinations)

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
    # print(groups)
    groups = remove_subsets_group(groups)

    # print(groups)
    if ENABLE_BLUETOOTH:
        to_remove = []
        for g in groups:
            if len(g) < 3:
                to_remove.append(g)
        groups = [item for item in groups if item not in to_remove]
    else:
        to_remove = []
        for g in groups:
            if len(g) < 2:
                to_remove.append(g)
        groups = [item for item in groups if item not in to_remove]
    # print(groups)

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
    return incompatible_intra_ids, incompatible_inter_ids, group_list


def grouper(sniffer_data, incompatible_intra_ids: defaultdict[set], incompatible_inter_ids: defaultdict[set]):
    
    grouped_list = deque()
    for sniffer_id, data in sniffer_data.items():
        # print(sniffer_id, data)
        # for i in data:
        #     if i["protocol"] == "Bluetooth":
        #         print(data)
        #         sys.exit()
        incompatible_intra_ids, incompatible_inter_ids, distance_groups = group_distances(data, incompatible_intra_ids, incompatible_inter_ids,)
        grouped_list.extend(distance_groups)
    grouped_list = remove_subsets_and_duplicates(grouped_list)
    # print(grouped_list)
    return incompatible_intra_ids, incompatible_inter_ids, grouped_list
