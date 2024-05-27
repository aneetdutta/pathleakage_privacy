from env import IDENTIFIER_LENGTH, BLUETOOTH_LOCALIZATION_ERROR, WIFI_LOCALIZATION_ERROR, LTE_LOCALIZATION_ERROR
from math import sqrt
# import cython
import copy
from pprint import pprint
from funct.mongofn import MongoDB
from collections import defaultdict
import itertools

def convert_sets_to_lists(d):
    d1 = copy.deepcopy(d)
    for k, v in d1.items():
        if isinstance(v, set):
            d1[k] = list(v)
        elif isinstance(v, dict):
            convert_sets_to_lists(v)
    return d1



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

def grouper(sniffer_data, md: MongoDB, id):
    grouped_list = []
    for sniffer_id, data in sniffer_data.items():
        distance_groups = group_distances(data)
        grouped_list.extend(distance_groups)
    return grouped_list

def clean_dict_of_sets(mapping):
    cleaned_mapping = defaultdict(set)

    # First pass: Initialize cleaned_mapping with the necessary elements
    for key, value_set in mapping.items():
        for element in value_set:
            if element in mapping and key in mapping[element]:
                cleaned_mapping[key].add(element)

    # Second pass: Remove redundant elements
    for key, value_set in mapping.items():
        if key in cleaned_mapping:
            necessary_elements = cleaned_mapping[key]
            for element in value_set:
                if element not in necessary_elements:
                    if all(key not in mapping[other_element] for other_element in necessary_elements):
                        necessary_elements.add(element)

    return dict(cleaned_mapping)

''' Tracking Algorithm: 
Input: Data of Two timesteps along with existing potential mapping and visited list 
Output: Visited List, Potential Mapping'''
def tracking_algorithm(two_timestep_data, intra_potential_mapping: defaultdict[set], inter_potential_mapping: defaultdict[set], visited_list:defaultdict[set]):
    intra_potential_mapping: defaultdict[set]  = defaultdict(set,intra_potential_mapping)
    inter_potential_mapping: defaultdict[set] = defaultdict(set, inter_potential_mapping)
    visited_list = defaultdict(set, visited_list)
    
    timestep0 = two_timestep_data[0][0]
    mapping0 = two_timestep_data[0][1]
    
    timestep1 = two_timestep_data[1][0]
    mapping1 = two_timestep_data[1][1]
    
    # print(mapping0,'\n',mapping1)
    
    ''' Performing Intra Mapping '''
    
    ''' Step 1: Loop through all groups of Mapping 1 and Mapping 2 - Get all the visited list mappings'''
    
    '''Looping through mapping 1'''
    for m1 in mapping0:
        ''' Loop through mapping 0 and mapping 1 '''
        for m2 in mapping1:
            ''' Fetching protocols and the identifiers in mapping 1 '''
            for p1, ids1 in m1.items():
                ''' Comparing with only same protocol types during intra mapping'''
                if p1 not in m2:
                    continue
                ids2 = m2[p1]
                for id1 in ids1:
                    if id1 not in intra_potential_mapping: intra_potential_mapping[id1] = set()
                    ''' Remove id from mapping 1 set since it exists already '''
                    visited_items = set(ids1) - {id1}
                    ''' Remove id from mapping 2 set if it exists '''
                    if id1 in ids2:
                        visited_items.update(set(ids2) - {id1})
                    ''' Store the id and visited list to dict '''
                    visited_list[id1] = set(visited_list[id1])
                    visited_list[id1].update(visited_items)

    ''' Step 2: If id not in visited list, add it to the potential mapping '''
    for m1 in mapping0:
        ''' Loop through mapping 0 and mapping 1 '''
        for m2 in mapping1:
            ''' Compare protocols and identifiers '''
            for p1, ids1 in m1.items():
                ''' Comparing with only same protocol types during intra mapping'''
                if p1 not in m2:
                    continue
                ids2 = m2[p1]
                for id1 in ids1:
                    # print(p1, id1, "visited")
                    ''' If id existing in mapping 2, then ignore, do not compute
                    Else check if id part of the visited list of mapping 2 and add it if it does not exists '''
                    if id1 in ids2:
                        continue
                    potential = {id2 for id2 in ids2 if id2 not in visited_list.get(id1, set())}
                    
                    if potential:
                        intra_potential_mapping[id1] = set(intra_potential_mapping[id1])
                        intra_potential_mapping[id1].update(potential)
                    # if id1 == "LTEDevice43":
                    #     print("potential", id1, intra_potential_mapping[id1])
                        
    ''' Performing Inter Mapping '''
    
    ''' Step 1: Calculate mapping for timestep 0 and timestep 1'''
    
    '''Looping through mapping 0'''
    timestep_0_potential_mapping = defaultdict(set)

    for m1 in mapping0:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            for id1 in ids1:
                # print(p1, id1)
                timestep_0_potential_mapping[id1].update(ids2)
            for id2 in ids2:
                # print(p2, id2)
                timestep_0_potential_mapping[id2].update(ids1)
    
    # print('\nIntermapping started')
    # print("Timestep 0 Intermapping: ")
    # pprint(timestep_0_potential_mapping)

    # timestep_1_potential_mapping = {}
    # for m1 in mapping1:
    #     ''' Fetching protocols and the identifiers in mapping 1
    #     Compare the identifiers with each other for different protocols'''
    #     for p1, ids1 in m1.items():
    #         for p2, ids2 in m1.items():
    #             if p1 == p2:
    #                 continue
    #             for id1 in ids1:
    #                 # print(p1, id1, "ninja")
    #                 if id1 in timestep_1_potential_mapping:
    #                     timestep_1_potential_mapping[id1] = timestep_1_potential_mapping[id1].union(set(ids2))
    #                 else:
    #                     timestep_1_potential_mapping[id1] = set(ids2)

    # print(timestep_1_potential_mapping)
    '''Looping through mapping 1'''
    timestep_1_potential_mapping = defaultdict(set)
    
    for m1 in mapping1:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            for id1 in ids1:
                timestep_1_potential_mapping[id1].update(ids2)
            for id2 in ids2:
                timestep_1_potential_mapping[id2].update(ids1)

    # print("Timestep 1 Intermapping: ")
    # pprint(timestep_1_potential_mapping)
    
    ''' Step 2: Cleaning intermapping based on intra mapping '''
    t0_ids = set(list(timestep_0_potential_mapping))
    t1_ids = set(list(timestep_1_potential_mapping))
    
    ''' Fetching common ids in both intermapping dicts '''
    common_ids = t0_ids.intersection(t1_ids)
    
    different_ids_0 = t0_ids - t1_ids
    different_ids_1 = t1_ids - t0_ids
    for id in different_ids_0:
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        inter_potential_mapping[id].update(timestep_0_potential_mapping[id])
    for id in different_ids_1:
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        inter_potential_mapping[id].update(timestep_1_potential_mapping[id])

    for id in common_ids:
        # print(id)
        # pprint(timestep_0_potential_mapping[id])
        # pprint(timestep_1_potential_mapping[id])
        if not timestep_0_potential_mapping[id]:
            inter_potential_mapping[id].update(timestep_1_potential_mapping[id])
            continue
        if not timestep_1_potential_mapping[id]:
            inter_potential_mapping[id].update(timestep_0_potential_mapping[id])
            continue
            
        common_mappings = timestep_0_potential_mapping[id].intersection(timestep_1_potential_mapping[id])
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        inter_potential_mapping[id].update(common_mappings)
        t0_1 = timestep_0_potential_mapping[id] - timestep_1_potential_mapping[id]
        t1_0 = timestep_1_potential_mapping[id] - timestep_0_potential_mapping[id]
        if t0_1 and t1_0:
            for i in t0_1:
                intra_potential_mapping[i] = set(intra_potential_mapping[i])
                id_in_t1_0 = intra_potential_mapping[i].intersection(t1_0)
                # print(intra_potential_mapping[i], t0_1, id_in_t1_0)
                # print(id_in_t1_0)                # print(sorted_inter_potential_mapping)

                if id_in_t1_0:
                    ''' Update both id in t0_1 and id in t1_0'''
                    inter_potential_mapping[id].update(id_in_t1_0)
                    inter_potential_mapping[id].update({i})


    # print("hello")                
    # pprint(inter_potential_mapping)
    # print("Inter potential mapping")
    # pprint(inter_potential_mapping)
    ''' Update the inter potential mappings and intra potential mappings 
    Here, if L1 -> W3,W1, but W3 does not contain L1 then remove W3 from L1's mapping; check iteratively in while loop'''
    sorted_inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    sorted_inter_potential_mapping = defaultdict(set, sorted_inter_potential_mapping)
    # print("Sorted Mapping", sorted_inter_potential_mapping)
    '''
    {
        'L2': {'W1', 'W1`', 'W2', 'W3', 'W4'}, 
        'L3': {'W1', 'W1`', 'W2', 'W3', 'W4'}, 
        'L4': {'W1', 'W1`', 'W2', 'W3', 'W4'}, 
        'W1': {'L4', 'L2', 'L3', 'L1'}, 
        'W1`': {'L4', 'L2', 'L3', 'L1'}, 
        'L1': {'W1', 'W1`', 'W4', 'W2'}, 
        'W2': {'L2', 'L3', 'L1'}, 
        'W3': {'L2', 'L3'}, 
        'W4': {'L4'}
    }
    '''
    removal = True
    while removal:
        removal = False
        for key, value_set in list(sorted_inter_potential_mapping.items()):
            value_set = set(value_set)
            to_remove = set()
            to_remove_single= set()
            for element in value_set:
                ''' Check if element exists in the dictionary and key is not in its set '''
                if element in sorted_inter_potential_mapping and key not in sorted_inter_potential_mapping[element]:
                    to_remove.add(element)
                    removal = True
                
                # if element in sorted_inter_potential_mapping and key in sorted_inter_potential_mapping[element]:
                #     len_key = len(sorted_inter_potential_mapping[key])
                #     len_element = len(sorted_inter_potential_mapping[element])
                #     if len_key > len_element:
                #         if len_element == 1:
                #             temp_set_key = {key}.union(sorted_inter_potential_mapping[key])
                #             temp_set_element = {element}.union(sorted_inter_potential_mapping[element])
                #             to_remove_single.update(temp_set_key - temp_set_element)
                #             removal = True
                
            ''' Remove elements that are unnecessary '''
            if to_remove:
                value_set -= to_remove
            if to_remove_single:
                value_set -= to_remove_single

            if removal:
                sorted_inter_potential_mapping[key] = value_set
        # Only re-sort the dictionary if changes were made
        if removal:
            sorted_inter_potential_mapping = dict(sorted(sorted_inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
            sorted_inter_potential_mapping = defaultdict(set, sorted_inter_potential_mapping)

    sorted_inter_potential_mapping = dict(sorted(sorted_inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    sorted_inter_potential_mapping = defaultdict(set, sorted_inter_potential_mapping)
    
    # print(sorted_inter_potential_mapping)
    inter_potential_mapping = sorted_inter_potential_mapping
    
    ''' Update the intra potential mappings based on inter potential mappings '''
    removal = True
    while removal:
        removal = False
        for id1, value_set in intra_potential_mapping.items():
            value_set_ = set(value_set)
            to_remove = set()
            for id2 in value_set_:
                set_id1: set = set(inter_potential_mapping[id1])
                set_id2: set = set(inter_potential_mapping[id2])
                common_set = set_id1.intersection(set_id2)
                if not common_set and set_id1 and set_id2:
                    ''' Remove id2 from the value of intra potential mapping of id1 '''
                    to_remove.add(id2)
                    removal = True
            value_set_ -= to_remove
            if removal:
                intra_potential_mapping[id1] = set(value_set_)  
                removal = False                 

    # print(intra_potential_mapping["LTEDevice43"], "potential ninja")
    
    return dict(intra_potential_mapping), inter_potential_mapping, visited_list





