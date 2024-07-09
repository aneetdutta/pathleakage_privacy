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
    timestep_0_potential_mapping = defaultdict(set)
    for m1 in mapping0:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            id1, id2 = ids1[0], ids2[0]
            if id1 not in visited_inter_list[id2]:
                timestep_0_potential_mapping[id1].add(id2)

            if id2 not in visited_inter_list[id1]:
                timestep_0_potential_mapping[id2].add(id1)
    
    '''Looping through mapping 1'''
    timestep_1_potential_mapping = defaultdict(set)
    # print("Mapping1 ", mapping1)

    # print("visited ",visited_inter_list)
    for m1 in mapping1:
        ''' Fetching protocols and the identifiers in mapping 1
        Compare the identifiers with each other for different protocols'''
        for (p1, ids1), (p2, ids2) in itertools.combinations(m1.items(), 2):
            id1, id2 = ids1[0], ids2[0]
            if id2 not in visited_inter_list[id1]:
                timestep_1_potential_mapping[id1].add(id2)
            if id1 not in visited_inter_list[id2]:
                timestep_1_potential_mapping[id2].add(id1)
                    
    # if '8WJDMMBYOBK2' in timestep_1_potential_mapping:
    #     print('timestep_1_potential_mapping - 8WJDMMBYOBK2 found')
    #     print(timestep_1_potential_mapping["8WJDMMBYOBK2"])
    # if '8WJDMMBYOBK2' in timestep_0_potential_mapping:
    #     print('timestep_0_potential_mapping - 8WJDMMBYOBK2 found')
    #     print(timestep_0_potential_mapping["8WJDMMBYOBK2"])
    # if '8WJDMMBYOBK2' in visited_inter_list:
    #     print('visited_inter_list - 8WJDMMBYOBK2 found')
    #     print(visited_inter_list["8WJDMMBYOBK2"])
    return timestep_0_potential_mapping, timestep_1_potential_mapping

def tracking_phase_2_part_2(timestep_0_potential_mapping, timestep_1_potential_mapping,inter_potential_mapping,visited_inter_list, intra_potential_mapping, ENABLE_PARTIAL_COVERAGE: bool):
    t0_ids = set(list(timestep_0_potential_mapping))
    t1_ids = set(list(timestep_1_potential_mapping))
    
    # print(t0_ids, t1_ids)
    
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
        
    ''' Adding these ids to interpotential mapping directly '''
    # if not inter_potential_mapping:
    for id in different_ids_0:
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        for j in timestep_0_potential_mapping[id]:
            if j not in visited_inter_list[id]:
                inter_potential_mapping[id].add(j)
            
    for id in different_ids_1:
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        for j in timestep_1_potential_mapping[id]:
            if j not in visited_inter_list[id]:
                inter_potential_mapping[id].add(j)
    
    if ENABLE_PARTIAL_COVERAGE:
        for id in common_ids:
            inter_potential_mapping[id] = set(inter_potential_mapping[id])
            for j in timestep_0_potential_mapping[id]:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id].add(j)
            for j in timestep_1_potential_mapping[id]:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id].add(j)
        return inter_potential_mapping, visited_inter_list
    # print("Inter potential Mapping: ", inter_potential_mapping)
    
    for id in common_ids:
        ''' Sanity check if id exists but is inter t0 mapping is null'''
        if not timestep_0_potential_mapping[id]:
            for j in timestep_1_potential_mapping[id]:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id].add(j)
            continue
        if not timestep_1_potential_mapping[id]:
            # inter_potential_mapping[id].update(timestep_0_potential_mapping[id])
            for j in timestep_0_potential_mapping[id]:
                if j not in visited_inter_list[id]:
                    inter_potential_mapping[id].add(j)
            continue
            
        ''' Find common mappings inside common ids'''
        common_mappings = timestep_0_potential_mapping[id].intersection(timestep_1_potential_mapping[id])
        
        # print("Common_mappings for ", id, ": ", common_mappings, "\n")
        
        ''' Adding the common mappings directly to the interpotential mappings'''
        inter_potential_mapping[id] = set(inter_potential_mapping[id])
        inter_potential_mapping[id].update(common_mappings)
        
        inter_potential_mapping[id] = inter_potential_mapping[id] - visited_inter_list[id]
        
        # print("Updated common mappings to inter potential mapping")
        # print(inter_potential_mapping, "\n")
        
        ''' Calculating non common mappings (T0_1) AND (T1_0) in the common ids (having T0 and T1)'''

        t0_1 = timestep_0_potential_mapping[id] - timestep_1_potential_mapping[id]
        t1_0 = timestep_1_potential_mapping[id] - timestep_0_potential_mapping[id]
        
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
                        inter_potential_mapping[id].add(i)
                else:
                    if i in inter_potential_mapping[id]:
                        inter_potential_mapping[id].remove(i)
                    visited_inter_list[id].add(i)
                    
        elif t0_1 and not t1_0:
            for i in t0_1:
                if not intra_potential_mapping[i].intersection(common_mappings):
                    if i in inter_potential_mapping[id]:
                        inter_potential_mapping[id].remove(i)
                    visited_inter_list[id].add(i)
                else:
                    if i not in visited_inter_list[id]:
                        inter_potential_mapping[id].add(i)
                    
        elif t0_1 and t1_0:
            # if '8WJDMMBYOBK2' in inter_potential_mapping:
            #     print("t0_1")
            #     print(t0_1)
            #     print("t1_0")
            #     print(t1_0)
            #     print("common_mappings")
            #     print(common_mappings)
            #     print('inter_potential_mapping - 8WJDMMBYOBK2 found - 2-2')
            #     print(inter_potential_mapping["8WJDMMBYOBK2"])
            total_ids = t0_1.union(t1_0)
            added_ids = set()
            for i in t0_1:
                for j in common_mappings:
                    if j in intra_potential_mapping[i]:
                        if i not in visited_inter_list[id]:
                            inter_potential_mapping[id].add(i)
                            added_ids.add(i)

                if intra_potential_mapping[i].intersection(t1_0):
                    if i not in visited_inter_list[id]:
                        inter_potential_mapping[id].add(i)
                        inter_potential_mapping[id].update(intra_potential_mapping[i].intersection(t1_0))
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
                            inter_potential_mapping[id].add(i)
                            added_ids.add(i)
                # if i not in inter_potential_mapping[id]:
                #     visited_inter_list[id].add(i)
                #     if i in inter_potential_mapping[id]:
                #         inter_potential_mapping[id].remove(i)
            
            s = total_ids - added_ids
            
            for i in s:
                if i in inter_potential_mapping[id]:
                    inter_potential_mapping[id].remove(i)
                if i not in visited_inter_list[id]:
                    visited_inter_list[id].add(i)
                    
            for i in t1_0:
                for j in common_mappings:
                    if i in intra_potential_mapping[j]:
                        if i not in visited_inter_list[id]:
                            inter_potential_mapping[id].update({i})
                        break
                      
            common_set_for_t1_0 = set()
            not_common_set = set()
            ''' Select id from t0_1 '''
            for i in t0_1:
                intra_potential_mapping[i] = set(intra_potential_mapping[i])
                ''' check if intrapotential mapping of that id exists in the intersection '''
                id_in_t1_0_common = intra_potential_mapping[i].intersection(t1_0)
                
                ''' check if intra potential mapping of that id exists in the common mappings and add it if true '''
                if intra_potential_mapping[i].intersection(common_mappings):
                    if i not in visited_inter_list[id]:
                        inter_potential_mapping[id].update({i})
                    
                common_set_for_t1_0.update(id_in_t1_0_common)
                ''' Find not common mappings of that id'''
                not_common_set.update(t1_0 - id_in_t1_0_common)
                ''' Add i as well as common mappings to inter potential mappings '''
                if id_in_t1_0_common:
                    ''' Update both id in t0_1 and id in t1_0'''
                    inter_potential_mapping[id].update(id_in_t1_0_common)
                    if i not in visited_inter_list[id]:
                        inter_potential_mapping[id].update({i})
                else:
                    if i not in inter_potential_mapping[id]:
                        visited_inter_list[id].update({i})
                    # print(visited_inter_list[id])
            if not_common_set:
                uncommon_set = not_common_set - common_set_for_t1_0
                for i in uncommon_set:
                    if i not in inter_potential_mapping[id]:
                        visited_inter_list[id].update({i})
    # if '8WJDMMBYOBK2' in inter_potential_mapping:
    #     print('inter_potential_mapping - 8WJDMMBYOBK2 found - 2-1')
    #     print(inter_potential_mapping["8WJDMMBYOBK2"])
        
    return inter_potential_mapping, visited_inter_list
    
def tracking_phase_2_part_3(inter_potential_mapping, visited_inter_list):
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
            for element in value_set:
                inter_potential_mapping_elem = inter_potential_mapping[element]
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
                inter_potential_mapping[key] = value_set
        # Only re-sort the dictionary if changes were made
        if removal:
            inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
            inter_potential_mapping = defaultdict(set, inter_potential_mapping)

    inter_potential_mapping = dict(sorted(inter_potential_mapping.items(), key=lambda item: len(item[1]), reverse=True))
    inter_potential_mapping = defaultdict(set, inter_potential_mapping)
    
    return inter_potential_mapping, visited_inter_list
    
    
def tracking_phase_3(inter_potential_mapping, intra_potential_mapping, visited_intra_list):
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

def tracking_algorithm(two_timestep_data, intra_potential_mapping: defaultdict[set], inter_potential_mapping: defaultdict[set], visited_inter_list:defaultdict[set], visited_intra_list:defaultdict[set]):
    intra_potential_mapping: defaultdict[set]  = defaultdict(set,intra_potential_mapping)
    inter_potential_mapping: defaultdict[set] = defaultdict(set, inter_potential_mapping)
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
                        
    # print("Intra potential mapping - Initial")
    # pprint(intra_potential_mapping)
    # print("Visited intra mapping - Initial")
    # pprint(visited_intra_list)
    
    ''' Performing Inter Mapping '''
    
    ''' Step 1: Calculate mapping for timestep 0 and timestep 1'''
    timestep_0_potential_mapping, timestep_1_potential_mapping = tracking_phase_2_part_1(mapping0, mapping1, visited_inter_list, inter_potential_mapping)
    # print("Inter potential mapping - timestep")
    # pprint(timestep_0_potential_mapping)
    # pprint(timestep_1_potential_mapping)

    inter_potential_mapping, visited_inter_list = tracking_phase_2_part_2(timestep_0_potential_mapping, timestep_1_potential_mapping, inter_potential_mapping, visited_inter_list, intra_potential_mapping, ENABLE_PARTIAL_COVERAGE)
    # print("Intra potential mapping - After Inter")
    # pprint(intra_potential_mapping)
    # print("Inter potential mapping without filtering")
    # pprint(inter_potential_mapping)
    
    # print("Visited Inter List without filtering")
    # pprint(visited_inter_list)

    ''' Update the inter potential mappings and intra potential mappings 
    Here, if L1 -> W3,W1, but W3 does not contain L1 then remove W3 from L1's mapping; check iteratively in while loop'''
    if not ENABLE_PARTIAL_COVERAGE:
        inter_potential_mapping, visited_inter_list = tracking_phase_2_part_3(inter_potential_mapping, visited_inter_list)
    # print("intra_potential_mapping - before updation")
    # pprint(intra_potential_mapping)
    # print("inter_potential_mapping - before updation")
    # pprint(inter_potential_mapping)
        
    # print("Visited intra list prior phase 3")
    # pprint(visited_intra_list)
    # print("Visited Inter mapping prior phase 3")
    # pprint(visited_inter_list)
    ''' Update the intra potential mappings based on inter potential mappings '''
    intra_potential_mapping, visited_intra_list = tracking_phase_3(inter_potential_mapping, intra_potential_mapping, visited_intra_list)
    
    return intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list

