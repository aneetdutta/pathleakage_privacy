# from env import BLUETOOTH_LOCALIZATION_ERROR, WIFI_LOCALIZATION_ERROR, LTE_LOCALIZATION_ERROR, MAX_MOBILITY_FACTOR
import copy, os
from services.general import remove_subsets_and_duplicates, remove_subsets_group
from collections import defaultdict, deque
import sys


def group_distances(sniffer_groups, incompatible_ids: defaultdict[set]):
    BLUETOOTH_LOCALIZATION_ERROR = int(os.getenv("BLUETOOTH_LOCALIZATION_ERROR"))
    WIFI_LOCALIZATION_ERROR = int(os.getenv("WIFI_LOCALIZATION_ERROR"))
    LTE_LOCALIZATION_ERROR = int(os.getenv("LTE_LOCALIZATION_ERROR"))
    MAX_MOBILITY_FACTOR = float(os.getenv("MAX_MOBILITY_FACTOR"))
    groups = []  # Initialize list to store final groups
    '''iterate through sniffer_groups'''
    updated_timestep_dict = defaultdict()
    dist_dict = defaultdict()
    sniffer_groups: dict
    for sg in sniffer_groups:
        # print(sg)
        updated_timestep_dict[sg["id"]] = sg['timestep']
        dist_dict[sg["id"]] = sg['dist_S_U']
        sg_tup = (sg["protocol"],sg["id"])
        
        if not groups:
            first_group = set()
            first_group.add(tuple(sg_tup))
            groups.append(first_group)
        # incompatible_set: set = set()
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
                abs_dist = abs(int(dist_dict[d[1]]) - int(sg['dist_S_U']))
                mobility_error = abs(int(updated_timestep_dict[d[1]]) - int(sg['timestep']))*MAX_MOBILITY_FACTOR
                
                if d[0] == "LTE" and sg["protocol"] == "LTE" and abs_dist <= (LTE_LOCALIZATION_ERROR+LTE_LOCALIZATION_ERROR+ mobility_error):
                    compatible=True
                elif d[0] == "WiFi" and sg["protocol"] == "WiFi" and abs_dist <= (WIFI_LOCALIZATION_ERROR+WIFI_LOCALIZATION_ERROR+ mobility_error):
                    compatible=True
                elif d[0] == "Bluetooth" and sg["protocol"] == "Bluetooth" and abs_dist <= (BLUETOOTH_LOCALIZATION_ERROR+BLUETOOTH_LOCALIZATION_ERROR+ mobility_error):
                    compatible=True
                elif d[0] == "LTE" and sg["protocol"] == "WiFi":
                    compatible = False
                elif d[0] == "LTE" and sg["protocol"] == "Bluetooth":
                    compatible = False
                elif d[0] == "WiFi" and sg["protocol"] == "LTE":
                    compatible = False
                elif d[0] == "WiFi" and sg["protocol"] == "Bluetooth":
                    compatible = False
                elif d[0] == "Bluetooth" and sg["protocol"] == "LTE":
                    compatible = False
                elif d[0] == "Bluetooth" and sg["protocol"] == "WiFi":
                    compatible = False
                else: 
                    compatible = False
                    
                if compatible:
                    if not incompatible_ids[sg["id"]].intersection({d[1]}):
                        compatible_set.add(d)
                else:
                    incompatible_ids[sg["id"]].update({d[1]})
                    incompatible_ids[d[1]].update({sg["id"]})

            if sg_tup in group and not compatible:
                group.remove(sg_tup)
                
            i = i+1
            
        if not compatible_set:
            groups.append(set({tuple(sg_tup)}))
        else:
            for c_set in compatible_set:
                groups.append({sg_tup, c_set})

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
    return incompatible_ids, group_list

def grouper(sniffer_data, incompatible_ids: defaultdict[set]):
    grouped_list = deque()
    for sniffer_id, data in sniffer_data.items():
        incompatible_ids, distance_groups = group_distances(data, incompatible_ids)
        grouped_list.extend(distance_groups)
    grouped_list = remove_subsets_and_duplicates(grouped_list)
    return incompatible_ids, grouped_list
