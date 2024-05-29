from services.tracking_algorithm import tracking_algorithm
from collections import defaultdict
from pprint import pprint


# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1", "L2", "L3"], "WiFi": ["W1", "W2"]},
#             {"LTE": ["L2", "L3", "L4"], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L1", "L4"], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1", "L2", "L3", "L4"], "WiFi": ["W1`", "W2"]},
#             {"LTE": ["L2", "L3"], "WiFi": ["W3"]},
#             {"LTE": ["L1", "L4"], "WiFi": ["W4"]},
#         ],
#     ),
   
# ]



# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1", "L2"], "WiFi": ["W1", "W2"]},
#             {"LTE": ["L2", "L3"], "WiFi": ["W2", "W3"]},
#             {"LTE": ["L1", "L3"], "WiFi": ["W1", "W3"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L2", "L3"], "WiFi": ["W2", "W3"]},
#             {"LTE": ["L1", "L3"], "WiFi": ["W1", "W3"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W1", "W2"]},
#         ],
#     ),
   
# ]

# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1", "L2"], "WiFi": ["W1", "W2"]},
#             {"LTE": ["L2", "L3"], "WiFi": ["W2", "W3"]},
#             {"LTE": ["L1", "L3"], "WiFi": ["W1", "W3"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L2", "L3"], "WiFi": ["W2", "W3"]},
#             {"LTE": ["L1", "L3"], "WiFi": ["W1'", "W3"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W1'", "W2"]},
#         ],
#     ),
   
# ]

# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W1"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W2"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L2", "L1"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#         ],
#     ),
# ]


# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1"], "WiFi": ["W1"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W1"]},
#             {"LTE": ["L1", "L2"], "WiFi": ["W2"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L2", "L1"], "WiFi": ["W1"]},
#             {"LTE": ["L2"], "WiFi": ["W2"]},
#         ],
#     ),
# ]



# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": [], "WiFi": ["W1", "W2"]},
#             {"LTE": ["L2", "L3", "L4"], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L1", "L4"], "WiFi": ["W1"]},
#             {"LTE": ["L1", "L2"], "WiFi": []},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1", "L2", "L3", "L4"], "WiFi": ["W1`", "W2"]},
#             {"LTE": ["L1", "L2", "L3"], "WiFi": ["W3"]},
#             {"LTE": ["L1", "L4"], "WiFi": ["W4"]},
#         ],
#     )
# ]

# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": [], "WiFi": ["W1", "W2"]},
#             {"LTE": ["L2", "L3", "L4"], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L1", "L4"], "WiFi": []},
#             {"LTE": ["L1", "L2"], "WiFi": []},
#             {"LTE": [], "WiFi": ["W1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1", "L2", "L3", "L4"], "WiFi": []},
#             {"LTE": [], "WiFi": ["W1", "W2"]},
#             {"LTE": [], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L3", "L4"], "WiFi": ["W3"]},
#             {"LTE": [], "WiFi": ["W3"]},
#             {"LTE": [], "WiFi": ["W3"]},
#             {"LTE": ["L3", "L4"], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L1", "L2", "L3"], "WiFi": ["W3"]},
#             {"LTE": ["L1", "L4"], "WiFi": ["W4"]},
#         ],
#     ),
#     (
#         2,
#         [
#             {"LTE": ["L1", "L2"], "WiFi": []},
#             {"LTE": ["L2"], "WiFi": ["W1", "W2"]},
#             {"LTE": [], "WiFi": ["W3", "W4"]},
#             {"LTE": ["L3", "L4"], "WiFi": ["W3"]},
#             {"LTE": ["L2", "L3"], "WiFi": ["W3"]},
#             {"LTE": [], "WiFi": ["W3"]},
#             {"LTE": ["L3", "L4"], "WiFi": ["W4"]},
#             {"LTE": ["L1", "L2", "L3"], "WiFi": ["W3"]},
#             {"LTE": [], "WiFi": ["W4"]},
#         ],
#     )
# ]
# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1", "L2"], "WiFi": []},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1", "L2", "L3"], "WiFi": ["W1", "W2"]},
#         ],
#     ),
#     (
#         2,
#         [
#             {"LTE": ["L1", "L3", "L4"], "WiFi": ["W3"]},
#         ],
#     ),
   
# ]


# test_tuple = [
#     (
#         0,
#         [
#             {"LTE": ["L1", "L2"], "WiFi": ["W1", "W2"], "Bluetooth": ["B1"]},
#         ],
#     ),
#     (
#         1,
#         [
#             {"LTE": ["L1`", "L2"], "WiFi": ["W1`", "W2"], "Bluetooth": ["B2"]},
#         ],
#     ),
   
# ]


test_tuple = [
    (
        0,
        [
            {"LTE": ["L1", "L2"], "WiFi": ["W1"]},
            {"LTE": ["L1", "L2", "L3"], "WiFi": ["W2", "W3"]},
            {"LTE": ["L1", "L3"], "WiFi": ["W3"]},
        ],
    ),
    (
        1,
        [
            {"LTE": ["L2", "L3"], "WiFi": ["W2"]},
            {"LTE": ["L1", "L3"], "WiFi": ["W1"]},
            {"LTE": ["L3", "L2"], "WiFi": ["W3"]},
        ],
    ),
   
]


timestep_pairs = [(test_tuple[i], test_tuple[i + 1]) for i in range(len(test_tuple) - 1)]
# print(timestep_pairs)
intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list = defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set)

i = 0
for timestep_pair in timestep_pairs:
    
    # print(timestep_pair)  
    # potential_mapping = tracking_algorithm(two_timestep_data)
    intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list =  tracking_algorithm(timestep_pair, intra_potential_mapping=intra_potential_mapping, inter_potential_mapping=inter_potential_mapping, visited_inter_list=visited_inter_list, visited_intra_list=visited_intra_list)

    print(f"for timestep - {i} - {i+1} \n")
    
    print("\nInter potential mapping\n")
    pprint(inter_potential_mapping)
                                    
    print("\nIntra_potential_mapping\n")
    pprint(intra_potential_mapping)
    print("\n")

    print("\Visited Inter List\n")
    pprint(visited_inter_list)
    print("\n")
        
    print("\Visited Intra List\n")
    pprint(visited_intra_list)
    print("\n")
    i+=1
