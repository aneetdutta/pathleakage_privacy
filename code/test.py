from funct.fn import group_distances



'''Test Case 1:
Groups Formed: {W1,W2,L1,L2,L3,L4}, {W3,W4,L1,L2,L3,L4}
'''
'''
# Sample list of dictionaries representing distances and types
sniffer_group = [
    {'protocol': 'LTE', 'lte_id': 'L1', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 90},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W1', 'bluetooth_id': None, 'dist_S_U': 90},
    {'protocol': 'LTE', 'lte_id': 'L2', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 80},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W2', 'bluetooth_id': None, 'dist_S_U': 80},
    {'protocol': 'LTE', 'lte_id': 'L3', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 10},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W3', 'bluetooth_id': None, 'dist_S_U': 10},
    {'protocol': 'LTE', 'lte_id': 'L4', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 20},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W4', 'bluetooth_id': None, 'dist_S_U': 20},
]

groups = group_distances(sniffer_group)
'''


'''Test Case 2:
Groups Formed: {W1,W2,L1,L2,L3,L4}, {W3,W4,L1,L2,L3,L4}, {W5,L1,L2,L3,L4}
'''

# Sample list of dictionaries representing distances and types
sniffer_group = [
    {'protocol': 'LTE', 'lte_id': 'L1', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 90},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W1', 'bluetooth_id': None, 'dist_S_U': 90},
    {'protocol': 'LTE', 'lte_id': 'L2', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 80},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W2', 'bluetooth_id': None, 'dist_S_U': 80},
    {'protocol': 'LTE', 'lte_id': 'L3', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 10},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W3', 'bluetooth_id': None, 'dist_S_U': 10},
    {'protocol': 'LTE', 'lte_id': 'L4', 'WiFi_id': None, 'bluetooth_id': None, 'dist_S_U': 5},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W4', 'bluetooth_id': None, 'dist_S_U': 5},
    {'protocol': 'WiFi', 'lte_id': None, 'WiFi_id': 'W5', 'bluetooth_id': None, 'dist_S_U': 45},
]

groups = group_distances(sniffer_group)
print(groups)

