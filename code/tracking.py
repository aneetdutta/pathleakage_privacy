import pickle
import json
import numpy as np
from modules.devicemanager import DeviceManager
from functions.fn import group_lines_by_distance, extract_lines_with_same_time
from collections import defaultdict
from functions.rules import rule_1, rule_2, rule_3, rule_4, rule_5, rule_6

# Opening JSON file
with open("20240506150753_sniffed_data.json") as f:
    data = json.load(f)

print("data loaded")

mapped_devices = dict()
linked_ids = dict()

protocol_to_id = {
    "Bluetooth": "bluetooth_id",
    "WiFi": "WiFi_id",
    "LTE": "lte_id",
}

target_time = 0
T = []

D = defaultdict(list)

for target_time in range(0, 7200):
    print(target_time)
    # print("----")
    lines_with_same_time = extract_lines_with_same_time(data, target_time)
    groups = group_lines_by_distance(lines_with_same_time, 0.1)

    for item in groups:
        # List comprehension with conditional tuples
        l = list({
            (element["protocol"], element[protocol_to_id[element["protocol"]]])
            for element in item
            if element["protocol"] in {"Bluetooth", "WiFi", "LTE"}
        })
        D[target_time].append(l)

print("done1")
manager = DeviceManager()
devices = []
for target_time in range(0, 7199):
    l = D.get(target_time, [])
    new_target = target_time + 1
    for j in range(new_target, new_target + 1):
        if j in D:
            l1 = D[j]
        else:
            j = new_target + 1
            continue

        for item in l:
            device = rule_2(manager, item, devices)
            for item1 in l1:
                mapping = rule_3(manager, item, item1)
                if mapping is not None:
                    linked_ids[mapping[0].pop()] = mapping[1].pop()
                mapping, devices = rule_1(item, item1, devices)
                
                if mapping is not None:
                    linked_ids[mapping[0].pop()] = mapping[1].pop()
                rule_4(manager, item, item1)
                rule_5(manager, item, item1)
                rule_6(manager, item, item1)

for device in manager.device_list:
    print(device.bluetooth_id, device.wifi_id, device.lte_id)

tracking = []
# Define file path
pickle_file = "manager.pkl"
with open(pickle_file, "wb") as file:
    pickle.dump(manager, file)

file_path = "linked_ids.json"
# Open the file in write mode
with open(file_path, "w") as json_file:
    # Serialize the dictionary to JSON and write it to the file
    json.dump(linked_ids, json_file)
