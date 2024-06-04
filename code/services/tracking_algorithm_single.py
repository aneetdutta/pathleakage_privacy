from collections import defaultdict
import itertools
from pprint import pprint
from services.general import combine_and_exclude_all, optimized_mapping_comparison

""" Tracking Algorithm: 
Input: Data of Two timesteps along with existing potential mapping and visited list 
Output: Visited List, Potential Mapping"""


def tracking_algorithm_single(
    two_timestep_data,
    intra_potential_mapping: defaultdict[set],
    visited_intra_list: defaultdict[set],
):
    intra_potential_mapping: defaultdict[set] = defaultdict(
        set, intra_potential_mapping
    )
    visited_intra_list = defaultdict(set, visited_intra_list)

    timestep0 = two_timestep_data[0][0]
    mapping0 = two_timestep_data[0][1]

    timestep1 = two_timestep_data[1][0]
    mapping1 = two_timestep_data[1][1]

    # print(mapping0)
    # print("Timestep", timestep0, timestep1)

    """ Performing Intra Mapping """

    """ Step 1: Loop through all groups of Mapping 1 and Mapping 2 - Get all the visited list mappings"""

    """ Loop through mapping 0 and then loop through mapping 1"""
    """ Picking id from one group and adding other groups to visited list of id"""

    keys = ["LTE", "WiFi"]

    visited_intra_list = combine_and_exclude_all(mapping0, keys)

    # m1: dict
    # for m1 in mapping0:
    #     # print(m1)
    #     for m2 in mapping0:
    #         for p1, ids1 in m1.items():
    #             for id1 in ids1:
    #                 visited_intra_list[id1].update((set(ids1) - set(id1)))
    #                 if id1 not in intra_potential_mapping: intra_potential_mapping[id1] = set()
    #                 for p2, ids2 in m2.items():
    #                     if p1 != p2 and ids1 == ids2:
    #                         continue

    #                     if not set(ids2).issubset(set(visited_intra_list[id1])):
    #                         visited_intra_list[id1].update(set(ids2))

    """ Step 2: If id not in visited list, check localization and then add it to the potential mapping """
    visited_intra_list, intra_potential_mapping = optimized_mapping_comparison(
        mapping0=mapping0,
        mapping1=mapping1,
        visited_intra_list=visited_intra_list,
        intra_potential_mapping=intra_potential_mapping,
    )
    # for m1 in mapping0:
    #     ''' Loop through mapping 0 and mapping 1 '''
    #     for m2 in mapping1:
    #         ''' Compare protocols and identifiers '''

    # for p1, ids1 in m1.items():
    #     ''' Comparing with only same protocol types during intra mapping'''
    #     if p1 not in m2:
    #         continue
    #     ids1:set = set(ids1)
    #     ids2:set = set(m2[p1])

    #     if ids1.intersection(ids2):
    #         t0_1 = ids1 - ids2
    #         t1_0 = ids2 - ids1
    #         not_common_set = set()
    #         common_set_for_i = set()
    #         if t0_1 and t1_0:
    #             for i in t0_1:
    #                 common_set_for_i = visited_intra_list[i].intersection(t1_0)
    #                 not_common_set.update(t1_0 - common_set_for_i)
    #                 intra_potential_mapping[i] = set(intra_potential_mapping[i])
    #                 intra_potential_mapping[i].update(not_common_set)

    return intra_potential_mapping, visited_intra_list
