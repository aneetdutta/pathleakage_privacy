from collections import defaultdict
import itertools
from pprint import pprint

''' Tracking Algorithm: 
Input: Data of Two timesteps along with existing potential mapping and visited list 
Output: Visited List, Potential Mapping'''
def tracking_algorithm(two_timestep_data, intra_potential_mapping: defaultdict[set], inter_potential_mapping: defaultdict[set], visited_inter_list:defaultdict[set], visited_intra_list:defaultdict[set]):
    intra_potential_mapping: defaultdict[set]  = defaultdict(set,intra_potential_mapping)
    inter_potential_mapping: defaultdict[set] = defaultdict(set, inter_potential_mapping)
    visited_intra_list = defaultdict(set, visited_intra_list)
    visited_inter_list = defaultdict(set, visited_inter_list)
    
    timestep0 = two_timestep_data[0][0]
    mapping0 = two_timestep_data[0][1]
    
    timestep1 = two_timestep_data[1][0]
    mapping1 = two_timestep_data[1][1]
    
    # print("Timestep", timestep0, timestep1)
    
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
                    visited_intra_list[id1] = set(visited_intra_list[id1])
                    visited_intra_list[id1].update(visited_items)

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
                    ''' If id existing in mapping 2, then ignore, do not compute
                    Else check if id part of the visited list of mapping 2 and add it if it does not exists '''
                    if id1 in ids2:
                        continue
                    potential = {id2 for id2 in ids2 if id2 not in visited_intra_list.get(id1, set())}
                    
                    if potential:
                        intra_potential_mapping[id1] = set(intra_potential_mapping[id1])
                        intra_potential_mapping[id1].update(potential)
                        
    # print("Intra potential mapping - Initial")
    # pprint(intra_potential_mapping)
    ''' Performing Inter Mapping '''
    
    ''' Step 1: Calculate mapping for timestep 0 and timestep 1'''
    
    
    ''' Looping through mapping 0 '''
    timestep_0_potential_mapping = defaultdict(set)
    if inter_potential_mapping:
        timestep_0_potential_mapping = inter_potential_mapping#defaultdict(set)
    else:
        for m1 in mapping0:
            ''' Fetching protocols and the identifiers in mapping 1
            Compare the identifiers with each other for different protocols'''
            for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
                for id1 in ids1:
                    # print(p1, id1, ids1)
                    if id1 not in visited_inter_list:
                        timestep_0_potential_mapping[id1].update(ids2)
                for id2 in ids2:
                    # print(p2, id2)
                    if id2 not in visited_inter_list:
                        timestep_0_potential_mapping[id2].update(ids1)
                        
    '''Looping through mapping 1'''
    timestep_1_potential_mapping = defaultdict(set)
    # print("Mapping1 ", mapping1)
    # print("Interpotential ", inter_potential_mapping)
    # print("visited ",visited_inter_list)
    for m1 in mapping1:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            ids1 = set(ids1)
            ids2 = set(ids2)
            for id1 in ids1:
                if id1 not in visited_inter_list:
                    timestep_1_potential_mapping[id1].update(ids2)
                else:
                    diff1 = ids2 - visited_inter_list[id1].intersection(ids2)
                    timestep_1_potential_mapping[id1].update(diff1)
            for id2 in ids2:
                if id2 not in visited_inter_list:
                    timestep_1_potential_mapping[id2].update(ids1)
                else:
                    diff2 = ids1 - visited_inter_list[id2].intersection(ids1)
                    timestep_1_potential_mapping[id2].update(diff2)
                    
    # print("Timestep 0 Intermapping: ")
    # pprint(timestep_0_potential_mapping)
    # print("Timestep 1 Intermapping: ")
    # pprint(timestep_1_potential_mapping)
    # print("Visited Intermapping: ")
    # pprint(visited_inter_list)
    
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
        if not t0_1 and t1_0:
            visited_inter_list[id].update(t1_0)
        elif t0_1 and not t1_0:
            visited_inter_list[id].update(t0_1)
        if t0_1 and t1_0:
            common_set_for_t1_0 = set()
            not_common_set = set()
            for i in t0_1:
                intra_potential_mapping[i] = set(intra_potential_mapping[i])
                id_in_t1_0_common = intra_potential_mapping[i].intersection(t1_0)
                common_set_for_t1_0.update(id_in_t1_0_common)
                not_common_set.update(t1_0 - id_in_t1_0_common)
                if id_in_t1_0_common:
                    ''' Update both id in t0_1 and id in t1_0'''
                    inter_potential_mapping[id].update(id_in_t1_0_common)
                    inter_potential_mapping[id].update({i})
                else:
                    visited_inter_list[id].update({i})
                    # print(visited_inter_list[id])
            if not_common_set:
                # print(not_common_set - common_set_for_t1_0, "check")
                visited_inter_list[id].update(not_common_set - common_set_for_t1_0)


    # print("Intra potential mapping - After Inter")
    # pprint(intra_potential_mapping)
    # print("Inter potential mapping without filtering")
    # pprint(inter_potential_mapping)
    
    # print("Visited Inter List without filtering")
    # pprint(visited_inter_list)

    ''' Update the inter potential mappings and intra potential mappings 
    Here, if L1 -> W3,W1, but W3 does not contain L1 then remove W3 from L1's mapping; check iteratively in while loop'''
    inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    inter_potential_mapping = defaultdict(set, inter_potential_mapping)
    # print("Sorted Mapping", inter_potential_mapping)
    removal = True
    while removal:
        removal = False
        for key, value_set in list(inter_potential_mapping.items()):
            value_set = set(value_set)
            ''' Filter 1'''
            to_remove = set()
            ''' Filter 2'''
            to_remove_single= set()
            for element in value_set:
                inter_potential_mapping_elem = inter_potential_mapping[element]
                ''' Filter 1 '''
                ''' Check if element exists in the dictionary and key is not in its set '''
                if element in inter_potential_mapping and key not in inter_potential_mapping_elem:
                    to_remove.add(element)
                    removal = True
                
                ''' Filter 2 '''
                if element in inter_potential_mapping and key in inter_potential_mapping_elem:
                    len_key = len(inter_potential_mapping[key])
                    len_element = len(inter_potential_mapping_elem)
                    if len_key > len_element:
                        if len_element == 1:
                            temp_set_key = {key}.union(inter_potential_mapping[key])
                            temp_set_element = {element}.union(inter_potential_mapping_elem)
                            """ add conditions for W1 - L1, L1`, L2 
                            L1` - W1 ; check intra mapping for L1, L2 """
                            uncommon_elements = temp_set_key - temp_set_element
                            for i in uncommon_elements:
                                # print(i, common_elements, element, inter_potential_mapping_elem)
                                ''' let case be: W1->[L1, L1`], L1->[W1], L1`->[W1`]
                                while checking through L1, L1` for W1, let element = L1`
                                if due to randomization, L1` does not exists, then check opposite direction (i in intra[element]) '''
                                if (element not in intra_potential_mapping and i in intra_potential_mapping) and (element not in intra_potential_mapping[i]):
                                    # to_remove_single.update({i})
                                    # removal = True
                                    pass

                                # if element in intra_potential_mapping:
                                #     # if (i not in intra_potential_mapping[element]):
                                #     #     print("case 1: ", element, intra_potential_mapping[element], i, intra_potential_mapping[i])
                                #     #     print(key, value_set)
                                #     #     to_remove_single.update({i})
                                #     #     removal = True
                                #     pass
                                #     ''' if not randomization, intra mapping element exists -> check single direction only '''
                                # elif i in intra_potential_mapping:
                                #     if element not in intra_potential_mapping[i]:
                                #         # print("case 2: ", element, i)
                                #         to_remove_single.update({i})
                                #         removal = True
                                    # pass
                                # if element not in intra_potential_mapping:
                                #     if (i not in intra_potential_mapping[element]):
                
            ''' Remove elements that are unnecessary '''
            if to_remove:
                value_set -= to_remove
                # print(key, to_remove, "to_remove")
                visited_inter_list[key].update(to_remove)
            if to_remove_single:
                value_set -= to_remove_single
                # print(key, to_remove_single, "to_remove_single")
                visited_inter_list[key].update(to_remove_single)
            if removal:
                inter_potential_mapping[key] = value_set
        # Only re-sort the dictionary if changes were made
        if removal:
            inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
            inter_potential_mapping = defaultdict(set, inter_potential_mapping)

    inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    inter_potential_mapping = defaultdict(set, inter_potential_mapping)
    
    # print("intra_potential_mapping - before updation")
    # pprint(intra_potential_mapping)
    # print("inter_potential_mapping - before updation")
    # pprint(inter_potential_mapping)
    ''' Update the intra potential mappings based on inter potential mappings '''
    removal = True
    while removal:
        removal = False
        for id1, value_set in intra_potential_mapping.items():
            # if len(value_set) == 1:
            #     continue
            value_set_ = set(value_set)
            to_remove = set()
            for id2 in value_set_:
                set_id1: set = set(inter_potential_mapping[id1])
                set_id2: set = set(inter_potential_mapping[id2])
                common_set = set_id1.intersection(set_id2)
                # print(id1, id2, common_set, set_id1, set_id2)
                if not common_set and set_id1 and set_id2:
                    ''' Remove id2 from the value of intra potential mapping of id1 '''
                    to_remove.add(id2)
                    removal = True
            if to_remove:
                value_set_ -= to_remove
                ''' Updating in visited list - to optimizing the processing'''
                visited_intra_list[id1].update(to_remove)
                
            if removal:
                intra_potential_mapping[id1] = set(value_set_)  
                # removal = False                 

    return intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list

