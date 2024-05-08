import pickle
import ijson, json
import time
# import pyximport; pyximport.install()
import numpy as np
from modules.device import Device
from modules.devicemanager import DeviceManager
from funct.fn import group_lines_by_distance, extract_lines_with_same_time, D_getter, extract_json

from funct.rules import rule_1, rule_2, rule_3, rule_4, rule_5, rule_6

# Opening JSON file

# with open("20240506150753_sniffed_data.json") as f:
#     data = json.load(f)

# with open("20240506150753_sniffed_data.json", "rb") as f:
#     data = ijson.items(f, "item")
#     data_array = pd.DataFrame(data) 
    
now = time.time()
data = extract_json("20240506150753_sniffed_data.json")
    
print(data)
print("data loaded", time.time() - now)

mapped_devices = dict()
linked_ids = dict()

now = time.time()

D = D_getter(data)

print("Processing data completed")

manager = DeviceManager()
manager.linked_ids = linked_ids
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
                mapping, devices = rule_3(manager, item, item1, devices)
                if mapping is not None:
                    linked_ids[mapping[0].pop()] = mapping[1].pop()
                    manager.linked_ids = linked_ids
                mapping, devices = rule_1(item, item1, devices)
                
                if mapping is not None:
                    linked_ids[mapping[0].pop()] = mapping[1].pop()
                    manager.linked_ids = linked_ids
                devices = rule_4(manager, item, item1, devices)
                devices = rule_5(manager, item, item1, devices)
                devices = rule_6(manager, item, item1, devices)

print("done", time.time() - now)
device: Device
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
