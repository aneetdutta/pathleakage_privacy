import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from group.grouping_algorithm_seq import grouper
from collections import defaultdict
from pprint import pprint

# """Test Case 1:
# Same protocol, same distance, different IDs
# """

# sniffer_group = {"1234":[
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "99", "timestep": 18001.25},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "99", "timestep": 18001.5},
#     {"protocol": "LTE", "id": "LTEID3", "dist_S_U": "99", "timestep": 18002.75},
#     {"protocol": "LTE", "id": "LTEID4", "dist_S_U": "99", "timestep": 18003.75},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "99", "timestep": 18004.0},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "98", "timestep": 18004.75},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "98", "timestep": 18005.75},
# ]}

# """Test Case 2:
# Different protocols, same distance, different IDs
# """

# sniffer_group = {"1234":[
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "10", "timestep": 18001.25},
#     {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "10", "timestep": 18001.5},
#     {"protocol": "LTE", "id": "LTEID3", "dist_S_U": "99", "timestep": 18002.75},
#     {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "10", "timestep": 18003.5},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "99", "timestep": 18004.0},
#     {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "10", "timestep": 18004.5},
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "98", "timestep": 18005.75},
# ]}

# """Test Case 3:
# Different protocols, different distance, different IDs, large timesteps
# """

# sniffer_group = {"1234":[
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "10", "timestep": 18001.25},
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "10", "timestep": 18001.5},
#     {"protocol": "WiFi", "id": "WIFIID2", "dist_S_U": "10", "timestep": 18001.5},
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "50", "timestep": 18011.5},
# ]}


"""Test Case 4:
Different protocols, different distance, different IDs, large timesteps
"""

# sniffer_group = {"1234":[
#     {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "10", "timestep": 18001.25},
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "18", "timestep": 18001.5},
#     {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "18", "timestep": 18001.5},
#     {"protocol": "WiFi", "id": "WIFIID2", "dist_S_U": "10", "timestep": 18001.5},
#     {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "49", "timestep": 18011.5},
#     {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "50", "timestep": 18011.5},
# ]}

# sniffer_group = {
#     "1234": [
#         {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "10", "timestep": 18001.25},
#         {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "18", "timestep": 18001.5},
#         {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "18", "timestep": 18001.5},
#         {"protocol": "WiFi", "id": "WIFIID2", "dist_S_U": "10", "timestep": 18001.5},
#         {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "49", "timestep": 18011.5},
#         {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "10", "timestep": 18012.5},
#         # {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "50", "timestep": 18011.5},
#     ]
# }

sniffer_group = {
    "1234": [
            {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "10", "timestep": 18001.25},
            {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "30", "timestep": 18001.5},
            {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "30", "timestep": 18001.5},
            {"protocol": "WiFi", "id": "WIFIID2", "dist_S_U": "10", "timestep": 18001.5},
            {"protocol": "Bluetooth", "id": "BLE1", "dist_S_U": "30", "timestep": 18001.5},
            {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "40", "timestep": 18011.5},
            {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "20", "timestep": 18011.5},
        ]
}
incompatible_intra_ids, incompatible_inter_ids = defaultdict(set), defaultdict(set)
incompatible_intra_ids, incompatible_inter_ids, groups = grouper(sniffer_group, incompatible_intra_ids, incompatible_inter_ids,)
pprint(groups)
pprint(incompatible_intra_ids)
pprint(incompatible_inter_ids)
