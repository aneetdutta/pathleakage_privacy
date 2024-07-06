import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict
from group.grouping_smart_algorithm_seq import grouper
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

sniffer_group = {"1234":[
    {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "10", "timestep": 18001.25},
    {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "20", "timestep": 18010.25},
    # {"protocol": "WiFi", "id": "WIFIID1", "dist_S_U": "40", "timestep": 18001.25},
    # {"protocol": "WiFi", "id": "WIFIID2", "dist_S_U": "10", "timestep": 18006.25},
    # {"protocol": "LTE", "id": "LTEID1", "dist_S_U": "20", "timestep": 18011.5},
    # {"protocol": "LTE", "id": "LTEID2", "dist_S_U": "50", "timestep": 18011.5},
]}

incompatible_ids = defaultdict(set)
incompatible_ids, groups = grouper(sniffer_group, incompatible_ids)
pprint(groups)
pprint(incompatible_ids)
# print(groups)
# for item in groups:
#     for i in item:
#         print(i[1])

#     print('\n')

# '''Test Case 2:
# Groups Formed: {W1,W2,L1,L2,L3,L4}, {W3,W4,L1,L2,L3,L4}, {W5,L1,L2,L3,L4}
# '''

# # Sample list of dictionaries representing distances and types
# sniffer_group = [
#     {'protocol': 'LTE', 'lte_id': 'L1', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 90},
#     {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W1', 'bluetooth_id': None, 'dist_S_U': 90},
#     {'protocol': 'LTE', 'lte_id': 'L2', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 80},
#     {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W2', 'bluetooth_id': None, 'dist_S_U': 80},
#     {'protocol': 'LTE', 'lte_id': 'L3', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 10},
#     {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W3', 'bluetooth_id': None, 'dist_S_U': 10},
#     {'protocol': 'LTE', 'lte_id': 'L4', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 5},
#     {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W4', 'bluetooth_id': None, 'dist_S_U': 5},
#     {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W5', 'bluetooth_id': None, 'dist_S_U': 45},
# ]

# groups = group_distances(sniffer_group)
# print(groups)
