import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracking.tracking_algorithm import tracking_algorithm, tracking_phase1, tracking_phase_2_part_1, tracking_phase_2_part_2, tracking_phase_2_part_3, tracking_phase_3
from collections import defaultdict
from pprint import pprint


# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W1"]},
#             {"LTE": ["L1"], "WiFi": ["W2"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L2"], "WiFi": ["W3"]},
#             {"LTE": ["L3"], "WiFi": ["W3"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1"], "WiFi": ["W1`"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L3"], "WiFi": ["W2"]},
#             {"LTE": ["L3"], "WiFi": ["W3"]},
#             {"LTE": ["L1"], "WiFi": ["W3"]},
#         ],
#     ),
#     (
#         2,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1`"]},
#             {"LTE": ["L1"], "WiFi": ["W1``"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L3"], "WiFi": ["W2"]},
#             {"LTE": ["L3"], "WiFi": ["W3"]},
#             {"LTE": ["L1"], "WiFi": ["W3"]},
#         ],
#     )

# ]


# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#         ],
#     )
# ]

# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#         ],
#     )
# ]

# test_tuple = [
#     (
#         0,
#         [
#             # {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L3"], "WiFi": ["W3"]},
#             {"LTE": ["L3"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L2"], "WiFi": ["W2`"]},
#             {"LTE": ["L4"], "WiFi": ["W4"]}
#         ],
#     )
# ]
# test_tuple = [
#     (
#         0,
#         [
#             # {"LTE": ["L1"], "WiFi": ["W1"]},
#             # {"LTE": ["L1`"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         2,
#         [
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#         ],
#     )
# ]

# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L2"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1`"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#             {"LTE": ["L2"], "WiFi": ["W1"]},
#         ],
#     )
# ]


test_tuple = [
    # (
    #     0,
    #     [
    #         {"LTE": ["L1"], "WiFi": ["W1"]},
    #         {"LTE": ["L1"], "WiFi": ["W1`"]},
    #         {"LTE": ["L2"], "WiFi": ["W1`"]},
    #         {"LTE": ["L2"], "WiFi": ["W2"]},
    #         {"LTE": ["L3"], "WiFi": ["W3"]},
    #     ],
    # ),
    (
        1,
        [
            {"LTE": ["L1"], "WiFi": ["W1`"]},
            {"LTE": ["L2"], "WiFi": ["W2`"]},
            {"LTE": ["L1"], "WiFi": ["W1``"]},
            # {"LTE": ["L1"], "WiFi": ["W1```"]},
        ],
    ),
    (
        2,
        [
            # {"LTE": ["L1"], "WiFi": ["W1`"]},
            {"LTE": ["L2"], "WiFi": ["W2`"]},
            {"LTE": ["L1"], "WiFi": ["W1``"]},
            {"LTE": ["L1`"], "WiFi": ["W1``"]},
            {"LTE": ["L1`"], "WiFi": ["W1```"]},
            {"LTE": ["L2"], "WiFi": ["W1```"]},
        ],
    ),
    (
        3,
        [
            # {"LTE": ["L1"], "WiFi": ["W1`"]},
            {"LTE": ["L1`"], "WiFi": ["W1```"]},
        ],
    )
]

timestep_pairs = [
    (test_tuple[i], test_tuple[i + 1]) for i in range(len(test_tuple) - 1)
]
# print(timestep_pairs)
(
    intra_potential_mapping,
    inter_potential_mapping,
    visited_inter_list,
    visited_intra_list,
) = (defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))

i = 0
for timestep_pair in timestep_pairs:

    # print(timestep_pair)
    # potential_mapping = tracking_algorithm(two_timestep_data)
    (
        intra_potential_mapping,
        inter_potential_mapping,
        visited_inter_list,
        visited_intra_list,
    ) = tracking_algorithm(
        timestep_pair,
        intra_potential_mapping=intra_potential_mapping,
        inter_potential_mapping=inter_potential_mapping,
        visited_inter_list=visited_inter_list,
        visited_intra_list=visited_intra_list,
    )

    print(f"for timestep - {i} - {i+1} \n")

    print("\nInter potential mapping\n")
    pprint(inter_potential_mapping)

    print("\nIntra_potential_mapping\n")
    pprint(intra_potential_mapping)

    print("\nVisited Inter List\n")
    pprint(visited_inter_list)

    print("\nVisited Intra List\n")
    pprint(visited_intra_list)
    print("\n")
    i += 1
