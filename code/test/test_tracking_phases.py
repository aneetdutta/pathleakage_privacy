import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracking.tracking_algorithm import tracking_algorithm, tracking_phase1, tracking_phase_2_part_1, tracking_phase_2_part_2, tracking_phase_2_part_3, tracking_phase_3
from collections import defaultdict
from pprint import pprint


test_tuple = [
    (
        0,
        [
            {"LTE": ["L1"], "WiFi": ["W1"]},
            {"LTE": ["L2"], "WiFi": ["W2"]},
            {"LTE": ["L2"], "WiFi": ["W1"]},
        ],
    ),
    (
        1,
        [
            {"LTE": ["L1`"], "WiFi": ["W1"]},
            {"LTE": ["L2"], "WiFi": ["W2"]},
            {"LTE": ["L2"], "WiFi": ["W1"]},
        ],
    )
]

(
    intra_potential_mapping,
    inter_potential_mapping,
    visited_inter_list,
    visited_intra_list,
) = (defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))

intra_potential_mapping, visited_intra_list = tracking_phase1(test_tuple[0][1], test_tuple[1][1], intra_potential_mapping, visited_intra_list)

print("INTRA POTENTIAL")
pprint(intra_potential_mapping)
print("VISITED INTRA")
pprint(visited_intra_list)

timestep_0_potential_mapping, timestep_1_potential_mapping = tracking_phase_2_part_1(test_tuple[0][1], test_tuple[1][1], visited_inter_list, inter_potential_mapping)
print("timestep_0_potential_mapping")
pprint(timestep_0_potential_mapping)
print("timestep_1_potential_mapping")
pprint(timestep_1_potential_mapping)

inter_potential_mapping, visited_inter_list = tracking_phase_2_part_2(timestep_0_potential_mapping, timestep_1_potential_mapping, inter_potential_mapping, visited_inter_list, intra_potential_mapping)

print("INTER POTENTIAL 2")
pprint(inter_potential_mapping)
print("VISITED INTER 2")
pprint(visited_inter_list)