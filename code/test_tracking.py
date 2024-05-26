from funct.fn import tracking_algorithm
from collections import defaultdict

test_tuple = [
    (
        0,
        [
            {"LTE": ["L1", "L2", "L3", "L4"], "WiFi": ["W1", "W2"]},
            {"LTE": ["L2", "L7"], "WiFi": ["W3"]},
        ],
    ),
    (
        1,
        [
            {"LTE": ["L1", "L4", "L6", "L7"], "WiFi": ["W1", "W3"]},
            {"LTE": ["L2", "L4", "L6"], "WiFi": ["W2"]},
        ],
    ),
]

tracking_algorithm(test_tuple, intra_potential_mapping=defaultdict(set), inter_potential_mapping=defaultdict(set), visited_list=defaultdict(set))