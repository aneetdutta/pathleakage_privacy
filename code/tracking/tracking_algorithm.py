import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import defaultdict
import itertools
from services.general import str_to_bool
from pprint import pprint

''' Tracking Algorithm: 
Input: Data of Two timesteps along with existing potential mapping and visited list 
Output: Visited List, Potential Mapping'''

def tracking_phase1(mapping0, mapping1, intra_potential_mapping, visited_intra_list):
    
    for m1 in mapping0:
        ''' Loop through mapping 0 and mapping 1 '''
        for m2 in mapping1:
            ''' Compare protocols and identifiers '''
            for p1, ids1 in m1.items():
                ''' Comparing with only same protocol types during intra mapping'''
                if p1 not in m2:
                    continue
                ids2 = m2[p1]
                id1,id2 = ids1[0], ids2[0]
                if id1 not in intra_potential_mapping: intra_potential_mapping[id1] = set()
                if id1 not in visited_intra_list: visited_intra_list[id1] = set()
                
                if id1 == id2:
                    continue
                
                if id2 not in visited_intra_list[id1] and id2 not in intra_potential_mapping[id1]:
                    intra_potential_mapping[id1].update({id2})
                
                if id2 in intra_potential_mapping:
                    if id1 not in visited_intra_list[id2] and id2 not in visited_intra_list[id1]:
                        if id1 in intra_potential_mapping[id2]:
                            intra_potential_mapping[id1].remove(id2)
                            visited_intra_list[id1] = set(visited_intra_list[id1])
                            visited_intra_list[id1].add(id2)
                            intra_potential_mapping[id2].remove(id1)
                            visited_intra_list[id2] = set(visited_intra_list[id2])
                            visited_intra_list[id2].add(id1)

                        
    return intra_potential_mapping, visited_intra_list
    
def tracking_phase_2_part_1(mapping0, mapping1, visited_inter_list, inter_potential_mapping):
    # if inter_potential_mapping:
    #     timestep_0_potential_mapping = inter_potential_mapping#defaultdict(set)
    # else:
    timestep_0_potential_mapping = defaultdict(lambda: defaultdict(set))
    for m1 in mapping0:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            id1, id2 = ids1[0], ids2[0]
            if id1 not in visited_inter_list[id2]:
                ''' Check if different protocol exists, and add it to its set'''
                # if p1 in timestep_0_potential_mapping[id2]:
                timestep_0_potential_mapping[id2][p1].add(id1)

            if id2 not in visited_inter_list[id1]:
                # if p2 in timestep_0_potential_mapping[id1]:
                timestep_0_potential_mapping[id1][p2].add(id2)
    
    '''Looping through mapping 1'''
    timestep_1_potential_mapping = defaultdict(lambda: defaultdict(set))
    # print("Mapping1 ", mapping1)

    # print("visited ",visited_inter_list)
    for m1 in mapping1:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            id1, id2 = ids1[0], ids2[0]
            ''' Check if different protocol exists, and add it to its set'''
            if id1 not in visited_inter_list[id2]:
                timestep_1_potential_mapping[id2][p1].add(id1)
            if id2 not in visited_inter_list[id1]:
                # if p2 in timestep_1_potential_mapping[id1]:
                timestep_1_potential_mapping[id1][p2].add(id2)
    return timestep_0_potential_mapping, timestep_1_potential_mapping

def tracking_phase_2_part_2(timestep_0_potential_mapping, timestep_1_potential_mapping,inter_potential_mapping,visited_inter_list, intra_potential_mapping, ENABLE_PARTIAL_COVERAGE: bool):
    t0_ids = set(list(timestep_0_potential_mapping))
    t1_ids = set(list(timestep_1_potential_mapping))
    
    # print(t0_ids, t1_ids)
    # print(timestep_0_potential_mapping, timestep_1_potential_mapping)
    
    ''' Fetching common ids in both intermapping dicts '''
    common_ids = t0_ids.intersection(t1_ids)
    
    ''' IDs whose either T0 or T1 does not exists'''
    different_ids_0 = t0_ids - t1_ids
    different_ids_1 = t1_ids - t0_ids
    
    # print(different_ids_0, different_ids_1, common_ids)
    # print("\n")
    
    # if '8WJDMMBYOBK2' in inter_potential_mapping:
    #     print('inter_potential_mapping - 8WJDMMBYOBK2 found')
    #     print(inter_potential_mapping["8WJDMMBYOBK2"])
    # print("Hello")
    # print(inter_potential_mapping)
    ''' Adding these ids to interpotential mapping directly '''
    # if not inter_potential_mapping:
    for id in different_ids_0:
        for p, inter_ids in timestep_0_potential_mapping[id].items():
            for j in inter_ids:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id][p].add(j)
            
    for id in different_ids_1:
        # inter_potential_mapping[id] = set(inter_potential_mapping[id])
        for p, inter_ids in timestep_1_potential_mapping[id].items():
            for j in inter_ids:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id][p].add(j)
                
    
    if ENABLE_PARTIAL_COVERAGE:
        for id in common_ids:
            # inter_potential_mapping[id] = set(inter_potential_mapping[id])
            for p, inter_ids in timestep_0_potential_mapping[id].items():
                for j in inter_ids:
                    if j not in visited_inter_list[id]:
                        inter_potential_mapping[id][p].add(j)
            for p, inter_ids in timestep_1_potential_mapping[id].items():
                for j in inter_ids:
                    if j not in visited_inter_list[id]:
                        inter_potential_mapping[id][p].add(j)
        return inter_potential_mapping, visited_inter_list
    # print("Inter potential Mapping: ", inter_potential_mapping)
    
    for id in common_ids:
        ''' Sanity check if id exists but is inter t0 mapping is null'''
        if not timestep_0_potential_mapping[id]:
            for p, inter_ids in timestep_1_potential_mapping[id].items():
                for j in inter_ids:
                    if j not in visited_inter_list[id]:
                        inter_potential_mapping[id].add(j)
            continue
        if not timestep_1_potential_mapping[id]:
            # inter_potential_mapping[id].update(timestep_0_potential_mapping[id])
            for p, inter_ids in timestep_0_potential_mapping[id].items():
                for j in inter_ids:
                    if j not in visited_inter_list[id]:
                        inter_potential_mapping[id].add(j)
            continue
            
        ''' Get protocol list'''
        
        if set(list(timestep_0_potential_mapping[id])) != set(list(timestep_1_potential_mapping[id])):
            raise Exception(f"Grouping not proper, inconsistency found {list(timestep_0_potential_mapping[id])} - {list(timestep_1_potential_mapping[id])}")
        protocols = set(list(timestep_0_potential_mapping[id])).intersection(set(list(timestep_0_potential_mapping[id])))
        # print(protocols)
        for p in protocols:
            common_mappings = timestep_0_potential_mapping[id][p].intersection(timestep_1_potential_mapping[id][p])
        
            # print("Common_mappings for ", id, ": ", common_mappings, "\n")
            
            ''' Adding the common mappings directly to the interpotential mappings'''
            inter_potential_mapping[id][p] = set(inter_potential_mapping[id][p])
            inter_potential_mapping[id][p].update(common_mappings)
            # print(inter_potential_mapping)
            inter_potential_mapping[id][p] = inter_potential_mapping[id][p] - visited_inter_list[id]
            # print(inter_potential_mapping)
            # print("Updated common mappings to inter potential mapping")
            # print(inter_potential_mapping, "\n")
            
            ''' Calculating non common mappings (T0_1) AND (T1_0) in the common ids (having T0 and T1)'''

            t0_1 = timestep_0_potential_mapping[id][p] - timestep_1_potential_mapping[id][p]
            t1_0 = timestep_1_potential_mapping[id][p] - timestep_0_potential_mapping[id][p]
            
            # print(t0_1, t1_0, "inside common mappings")
            # print(inter_potential_mapping)
            if not t0_1 and t1_0:
                for i in t1_0:
                    checker = False
                    for j in common_mappings:
                        if i in intra_potential_mapping[j]:
                            checker=True
                            break
                    if checker:
                        if i not in visited_inter_list[id]:
                            inter_potential_mapping[id][p].add(i)
                    else:
                        if i in inter_potential_mapping[id]:
                            inter_potential_mapping[id][p].remove(i)
                        visited_inter_list[id].add(i)
                    
            elif t0_1 and not t1_0:
                for i in t0_1:
                    if not intra_potential_mapping[i].intersection(common_mappings):
                        if i in inter_potential_mapping[id]:
                            inter_potential_mapping[id][p].remove(i)
                        visited_inter_list[id].add(i)
                    else:
                        if i not in visited_inter_list[id]:
                            inter_potential_mapping[id][p].add(i)
                    
            elif t0_1 and t1_0:
                total_ids = t0_1.union(t1_0)
                added_ids = set()
                for i in t0_1:
                    for j in common_mappings:
                        if i == j:
                            '''Already added through common mappings'''
                            continue
                        if j in intra_potential_mapping[i]:
                            if i not in visited_inter_list[id]:
                                inter_potential_mapping[id][p].add(i)
                                added_ids.add(i)

                    if intra_potential_mapping[i].intersection(t1_0):
                        if i not in visited_inter_list[id]:
                            inter_potential_mapping[id][p].add(i)
                            inter_potential_mapping[id][p].update(intra_potential_mapping[i].intersection(t1_0))
                            added_ids.add(i)
                            added_ids.update(intra_potential_mapping[i].intersection(t1_0))
                    # else:
                    #     visited_inter_list[id].add(i)
                        # if i in inter_potential_mapping[id]:
                        #     inter_potential_mapping[id].remove(i)
                            
                for i in t1_0:
                    for j in common_mappings:
                        if i in intra_potential_mapping[j]:
                            if i not in visited_inter_list[id]:
                                inter_potential_mapping[id][p].add(i)
                                added_ids.add(i)
                    # if i not in inter_potential_mapping[id]:
                    #     visited_inter_list[id].add(i)
                    #     if i in inter_potential_mapping[id]:
                    #         inter_potential_mapping[id].remove(i)
                
                s = total_ids - added_ids
                
                for i in s:
                    if i in inter_potential_mapping[id][p]:
                        inter_potential_mapping[id][p].remove(i)
                    if i not in visited_inter_list[id]:
                        visited_inter_list[id].add(i)
    # print(inter_potential_mapping)
    return inter_potential_mapping, visited_inter_list
    
def tracking_phase_2_part_3(inter_potential_mapping, visited_inter_list):
    # inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    inter_potential_mapping = defaultdict(set, inter_potential_mapping)
    # print("Sorted Mapping", inter_potential_mapping)
    removal = True
    while removal:
        removal = False
        # print(inter_potential_mapping)
        for key, p_set in inter_potential_mapping.items():
            for p, value_set in  p_set.items():
                value_set = set(value_set)
                ''' Filter 1'''
                to_remove = set()
                for element in value_set:
                    inter_potential_mapping_elem = set().union(*inter_potential_mapping[element].values())
                    # inter_potential_mapping_elem = inter_potential_mapping[element]
                    ''' Filter 1 '''
                    ''' Check if element exists in the dictionary and key is not in its set '''
                    if element in inter_potential_mapping and key not in inter_potential_mapping_elem:
                        to_remove.add(element)
                        removal = True
                
                ''' Remove elements that are unnecessary '''
                if to_remove:
                    value_set -= to_remove
                    # print(key, to_remove, "to_remove")
                    visited_inter_list[key].update(to_remove)
                    inter_potential_mapping[key][p] = value_set
        # Only re-sort the dictionary if changes were made
        # if removal:
            # inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
            # inter_potential_mapping = defaultdict(set, inter_potential_mapping)

    # inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    # inter_potential_mapping = defaultdict(set, inter_potential_mapping)

    return inter_potential_mapping, visited_inter_list
    
    
def tracking_phase_3(inter_potential_mapping, intra_potential_mapping, visited_intra_list):
    # for i
    # for id1 in intra_potential_mapping:
    #     for p, value_set_ in intra_potential_mapping[id1]:
    #         value_set_ = set(value_set_)
    #         to_remove = set()
    #         for id2 in value_set_:
    #             set_id1: set = set(inter_potential_mapping[id1][p])
    #             set_id2: set = set(inter_potential_mapping[id2][p])
    #             common_set = set_id1.intersection(set_id2)
                
    for id1, value_set in intra_potential_mapping.items():
        value_set_ = set(value_set)
        to_remove = set()
        for id2 in value_set_:
            for p in inter_potential_mapping[id1]:
                set_id1: set = set(inter_potential_mapping[id1][p])
                set_id2: set = set(inter_potential_mapping[id2][p])
                common_set = set_id1.intersection(set_id2)
                if not set_id1 or not set_id2:
                    raise Exception("Null Ids exists somewhere prior")
                # print(id1, id2, common_set, set_id1, set_id2)
                if not common_set:# and set_id1 and set_id2:
                    ''' Remove id2 from the value of intra potential mapping of id1 '''
                    to_remove.add(id2)
                    break
        if to_remove:
            value_set_ -= to_remove
            ''' Updating in visited list - to optimizing the processing'''
            visited_intra_list[id1].update(to_remove)
            intra_potential_mapping[id1] = set(value_set_) 
    return intra_potential_mapping, visited_intra_list

# def tracking_phase_4(inter_potential_mapping, intra_potential_mapping, visited_inter_list):
    
    # tracking_phase_2_part_3(inter_potential_mapping, visited_inter_list)
    # for id, mapping in inter_potential_mapping.items():
    #     # mapping = inter_potential_mapping[id]
    #     mapping = set(mapping)
    #     to_remove = set()
    #     union_set = set()
    #     if intra_potential_mapping[id]:
    #         for id2 in intra_potential_mapping[id]:
    #             union_set = union_set.union(inter_potential_mapping[id2])
                
    #         inter_potential_mapping[id] = mapping.intersection(union_set)
    #         # print(id, inter_potential_mapping[id], mapping, union_set, inter_potential_mapping[id2])  
    #         visited_inter_list[id].update(mapping - union_set)
        
    # return inter_potential_mapping, visited_inter_list
# Function to convert nested dictionaries to defaultdict of sets
def convert_to_defaultdict(d):
    if not isinstance(d, dict):
        return d
    return defaultdict(set, {k: convert_to_defaultdict(v) for k, v in d.items()})


def tracking_algorithm(two_timestep_data, intra_potential_mapping: defaultdict[set], inter_potential_mapping: defaultdict[dict], visited_inter_list:defaultdict[set], visited_intra_list:defaultdict[set]):
    intra_potential_mapping: defaultdict[set]  = defaultdict(set,intra_potential_mapping)
    if not inter_potential_mapping:
        inter_potential_mapping = defaultdict(lambda: defaultdict(set))
    else:
        inter_potential_mapping = defaultdict(
                lambda: defaultdict(set),
                {k: convert_to_defaultdict(v) for k, v in inter_potential_mapping.items()}
            )
    # inter_potential_mapping: defaultdict[dict] = defaultdict(dict, inter_potential_mapping)
    visited_intra_list = defaultdict(set, visited_intra_list)
    visited_inter_list = defaultdict(set, visited_inter_list)
    
    timestep0 = two_timestep_data[0][0]
    mapping0 = two_timestep_data[0][1]
    
    timestep1 = two_timestep_data[1][0]
    mapping1 = two_timestep_data[1][1]
    
    ENABLE_PARTIAL_COVERAGE = str_to_bool(os.getenv("ENABLE_PARTIAL_COVERAGE", "false"))
    
    # pprint(mapping0)
    # pprint(mapping1)
    print(timestep0, timestep1)
    ''' Performing Intra Mapping '''
    intra_potential_mapping, visited_intra_list = tracking_phase1(mapping0, mapping1, intra_potential_mapping, visited_intra_list)
                        
    print("Intra potential mapping - Initial")
    pprint(intra_potential_mapping)
    print("Visited intra mapping - Initial")
    pprint(visited_intra_list)
    
    ''' Performing Inter Mapping '''
    
    ''' Step 1: Calculate mapping for timestep 0 and timestep 1'''
    timestep_0_potential_mapping, timestep_1_potential_mapping = tracking_phase_2_part_1(mapping0, mapping1, visited_inter_list, inter_potential_mapping)
    print("Inter potential mapping - timestep")
    pprint(timestep_0_potential_mapping)
    pprint(timestep_1_potential_mapping)

    inter_potential_mapping, visited_inter_list = tracking_phase_2_part_2(timestep_0_potential_mapping, timestep_1_potential_mapping, inter_potential_mapping, visited_inter_list, intra_potential_mapping, ENABLE_PARTIAL_COVERAGE)
    print("Intra potential mapping - After Inter")
    pprint(intra_potential_mapping)
    print("Inter potential mapping without filtering")
    pprint(inter_potential_mapping)
    
    # print("Visited Inter List without filtering")
    # pprint(visited_inter_list)

    ''' Update the inter potential mappings and intra potential mappings 
    Here, if L1 -> W3,W1, but W3 does not contain L1 then remove W3 from L1's mapping; check iteratively in while loop'''
    if not ENABLE_PARTIAL_COVERAGE:
        inter_potential_mapping, visited_inter_list = tracking_phase_2_part_3(inter_potential_mapping, visited_inter_list)
    print("intra_potential_mapping - before updation")
    pprint(intra_potential_mapping)
    print("inter_potential_mapping - before updation")
    pprint(inter_potential_mapping)
    inter_potential_mapping = defaultdict(
        lambda: defaultdict(set),
        {k: convert_to_defaultdict(v) for k, v in inter_potential_mapping.items()}
    )
    # print("Visited intra list prior phase 3")
    # pprint(visited_intra_list)
    # print("Visited Inter mapping prior phase 3")
    # pprint(visited_inter_list)
    ''' Update the intra potential mappings based on inter potential mappings '''
    intra_potential_mapping, visited_intra_list = tracking_phase_3(inter_potential_mapping, intra_potential_mapping, visited_intra_list)
    
    return intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list

