import pickle
import ijson, json
import time, sys
# import pyximport; pyximport.install()
import numpy as np
from modules.device import Device
from modules.devicemanager import DeviceManager
from funct.fn import *

from funct.rules import *

# Opening JSON file

# now = time.time()
# data = extract_json("20240506150753_sniffed_data.json")
    
# print(data)
# print("data loaded", time.time() - now)
# sys.exit()

mapped_devices = dict()
linked_ids = dict()




# now = time.time()
# D, L = D_getter(data)
# # # Open the file in write mode
# with open("processed_dict.json", "w") as json_file:
#     # Serialize the dictionary to JSON and write it to the file
#     json.dump(D, json_file)
    
# with open("location_dict.json", "w") as json_file:
#     # Serialize the dictionary to JSON and write it to the file
#     json.dump(L, json_file)


# sys.exit()
data = extract_orjson("processed_dict.json")
location_data = extract_orjson("location_dict.json")

# D = json_read_process("processed_dict.json")

# print(data)
# sys.exit()
print("Processing data completed")

# sys.exit()
manager = DeviceManager()
manager.linked_ids = linked_ids
devices = []


'''Contains array of tn, tn+1 of timestep queue'''
consecutive_tq = deque(maxlen=2)
'''Contains list of tn-1 to 0  (past values for elimination)'''
past_timestep_arr = []
'''Contains deque from tn to tn+k'''
# future_tq = deque(len(data))

'''Fetches timestep and data for that timestep in this loop'''
for timestep, data_ in data.items():
    consecutive_tq.append(data_)
    # break
    if len(consecutive_tq) == 2:
        for item_tn_num, item_tn in enumerate(consecutive_tq[0]):
            '''Create intermapping based on rule 2'''
            device = rule_2(manager, item_tn, devices)
            '''Add elimination step'''
            for item_tn1_num, item_tn1 in enumerate(consecutive_tq[1]):
                mapping, devices = rule_3(manager, item_tn, item_tn1, consecutive_tq[1], devices, timestep, location_data)
                
                # if mapping is not None:
                #     linked_ids[mapping[0].pop()] = mapping[1].pop()
                #     manager.linked_ids = linked_ids
                    
                '''Create intra mapping based on rule 1'''
                mapping, devices = rule_1(item_tn, item_tn1, consecutive_tq[1], devices, timestep, location_data)
                if mapping is not None and len(mapping) == 2:
                    mapping_key, mapping_value = tuple(mapping)
                    linked_ids[mapping_key] = mapping_value
                    manager.linked_ids = linked_ids
        # break
    # break
    #     print(timestep)
    # # TO DO
    # break
    

# for target_time in range(0, 7199):
#     l = D.get(target_time, [])
#     new_target = target_time + 1
#     for j in range(new_target, new_target + 1):
#         if j in D:
#             l1 = D[j]
#         else:
#             j = new_target + 1
#             continue

#         for item in l:
#             device = rule_2(manager, item, devices)
#             for item1 in l1:
#                 mapping, devices = rule_3(manager, item, item1, devices)
#                 if mapping is not None:
#                     linked_ids[mapping[0].pop()] = mapping[1].pop()
#                     manager.linked_ids = linked_ids
#                 mapping, devices = rule_1(item, item1, devices)
                
#                 if mapping is not None:
#                     linked_ids[mapping[0].pop()] = mapping[1].pop()
#                     manager.linked_ids = linked_ids
#                 devices = rule_4(manager, item, item1, devices)
#                 devices = rule_5(manager, item, item1, devices)
#                 devices = rule_6(manager, item, item1, devices)
    
'''

Rule 1 needs to be modified in such a way that it checks if the old identifier is still existing?
Needs to compare within t and t+1
In rule 3 the same check needs to be performed when the changed identifier belongs to a protocol having higher communication range than the protocol having a fixed set of identifiers.
Needs to compare within t and t+1
Rule 4 is the same , just check from time t to (t+n).
Elimination rules must be implemented.
Found mapping at time t_m
Check elimination rules by removing the mapped identities from the remaining set.
Run it from time t_0 to the time till which this pair exists.
Note: Don’t save the mapping found in rule 3 or rule 1 when applying elimination.

'''
    

'''
Mapping algorithm

Create mapping table

while loop (
    Check if mapping table already exists:
    Delete mappings from all the timesteps - (Elimination procedure)
    Run the while loop again
    )
    
    For loop: Check through all timesteps from t0 to tn

        *apply rule 1 mapping*
        check timestep tx and tx+1,
            Here check if old modifier of tx exists in tx+1             

        *apply rule 3 mapping*
        check if other protocols sets are same: 
            if larger range:
                apply rule 1 checks
                
                
        
        *Apply rule 4 mapping*


'''


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
