from collections import defaultdict
import itertools
from pprint import pprint
from env import ENABLE_BLUETOOTH
from services.general import combine_and_exclude_all

''' Tracking Algorithm: 
Input: Data of Two timesteps along with existing potential mapping and visited list 
Output: Visited List, Potential Mapping'''
def tracking_algorithm_smart(two_timestep_data, intra_potential_mapping: defaultdict[set], visited_intra_list:defaultdict[set]):
    intra_potential_mapping: defaultdict[set]  = defaultdict(set,intra_potential_mapping)
    visited_intra_list = defaultdict(set, visited_intra_list)
    
    timestep0 = two_timestep_data[0][0]
    mapping0 = two_timestep_data[0][1]
    
    timestep1 = two_timestep_data[1][0]
    mapping1 = two_timestep_data[1][1]
    
    # print("Timestep", timestep0, timestep1)
    
    ''' Performing Intra Mapping '''
    
    ''' Step 1: Loop through all groups of Mapping 1 and Mapping 2 - Get all the visited list and inter potential mappings'''
    
    ''' Loop through mapping 0 and then loop through mapping 1'''
    ''' Picking id from one group and adding other groups to visited list of id'''
    if ENABLE_BLUETOOTH:
        keys = ["LTE", "WiFi", "Bluetooth"]
    else:
        keys = ["LTE", "WiFi"]

    visited_intra_list = combine_and_exclude_all(mapping0, keys, visited_intra_list)
    # print(mapping0)
    ''' Then loop through mapping 1'''
    for m1 in mapping0:
        ''' Loop through mapping 0 and mapping 1 '''
        for m2 in mapping1:
            ''' Fetching protocols and the identifiers in mapping 1 '''
            for p1, ids1 in m1.items():
                ''' Comparing with only same protocol types during intra mapping'''
                if p1 not in m2:
                    continue
                ids1:set = set(ids1)
                ids2:set = set(m2[p1])
                for id1 in ids1:
                    if id1 not in intra_potential_mapping: intra_potential_mapping[id1] = set()
                    ''' Add same group elements of mapping 0 to potential mapping '''
                    visited_intra_list[id1] = visited_intra_list[id1] - ids1
                    intra_potential_mapping[id1].update(ids1 - {id1})
                    ''' Add same group elements of mapping 1 to potential mapping if id from mapping 0 exists in mapping 1 '''
                    if id1 in ids2:
                        visited_intra_list[id1] = visited_intra_list[id1] - ids2
                        intra_potential_mapping[id1].update(ids2 - {id1})
                    intra_potential_mapping[id1] = intra_potential_mapping[id1] - visited_intra_list[id1]

    ''' Note: Do not combine both the phases '''
    
    ''' Step 2: take intersection and consider common elements'''

    ''' Then loop through mapping 1'''
    for m1 in mapping0:
        ''' Loop through mapping 0 and mapping 1 '''
        for m2 in mapping1:
            ''' Fetching protocols and the identifiers in mapping 1 '''
            for p1, ids1 in m1.items():
                ''' Comparing with only same protocol types during intra mapping'''
                if p1 not in m2:
                    continue
                
                ids1:set = set(ids1)
                ids2:set = set(m2[p1])
                
                ''' If intersection exists, add to intrapotential mapping 
                Else add to visited list '''
                common_ids = ids1.intersection(ids2)
                if common_ids:
                    t0_1 = ids1 - ids2
                    t1_0 = ids2 - ids1
                    not_common_set = set()   
                    common_set_for_i = set()         
                    if t0_1 and t1_0:
                        ''' Add the ids which are assymmetrically different as intra potential mapping T0->T1'''
                        for i in t0_1:
                            common_set_for_i = visited_intra_list[i].intersection(t1_0)
                            not_common_set.update(t1_0 - common_set_for_i)
                            intra_potential_mapping[i] = set(intra_potential_mapping[i])
                            intra_potential_mapping[i].update(not_common_set)  
                            intra_potential_mapping[i] = intra_potential_mapping[i] - visited_intra_list[i]   
                else:
                    for id1 in ids1:
                        visited_intra_list[id1].update(ids2)
                        
                if len(common_ids) > 1:
                    for id in common_ids:
                        to_remove = set()
                        for i in intra_potential_mapping[id]:
                            if i in intra_potential_mapping and id in intra_potential_mapping[i]:
                                intra_potential_mapping[i].remove(id)
                                visited_intra_list[i].add(id)
                                to_remove.add(i)
                                # print(to_remove, "hello", id)
                        intra_potential_mapping[id] = intra_potential_mapping[id] - to_remove
                        visited_intra_list[id].update(to_remove)  
    
    ''' Remove any redundant mappings from visited intra list '''       
    for id1 in visited_intra_list:
        visited_intra_list[id1] = visited_intra_list[id1] - intra_potential_mapping[id1] 
                
    # ''' Step 2: If id not in visited list, check localization and then add it to the potential mapping '''
    # for m1 in mapping0:
    #     ''' Loop through mapping 0 and mapping 1 '''
    #     for m2 in mapping1:
    #         ''' Compare protocols and identifiers '''
            
    #         for p1, ids1 in m1.items():
    #             ''' Comparing with only same protocol types during intra mapping'''
    #             if p1 not in m2:
    #                 continue
                
    #             ids2:set = set(m2[p1])
                
    #             if ids1.intersection(ids2):
    #                 print(ids1, ids2)
    #                 t0_1 = ids1 - ids2
    #                 t1_0 = ids2 - ids1
    #                 not_common_set = set()   
    #                 common_set_for_i = set()         
    #                 if t0_1 and t1_0:
    #                     for i in t0_1:
    #                         common_set_for_i = visited_intra_list[i].intersection(t1_0)
    #                         print(i, common_set_for_i, visited_intra_list[i])
    #                         not_common_set.update(t1_0 - common_set_for_i)
    #                         intra_potential_mapping[i] = set(intra_potential_mapping[i])
    #                         intra_potential_mapping[i].update(not_common_set)    

    return intra_potential_mapping, visited_intra_list

