import csv
import json
import numpy as np
import multiprocessing
import pickle
# Opening JSON file
from modules.device import Device
from modules.devicemanager import DeviceManager


pickle_file='manager.pkl'
with open(pickle_file, 'rb') as file:
    manager = pickle.load(file)

with open('linked_ids.json') as f2:
    linked_ids=json.load(f2)

print(len(linked_ids))


with open('user_data.json') as f1:
    data_user = json.load(f1)
 
 
count=0
userid1=1
userid2=100
for key,value in linked_ids.items():
    print(key,value)
    for line in data_user:
        if key in line.values():
            userid1=line['user_id']
            print(userid1)
        if value in line.values():
            #print(line['user_id'])
            userid2=line['user_id']
            print(userid2)
        if userid1==userid2:
            count=count+1
            break
            
            
print(count/len(linked_ids))

count=0


linked_ids_reconstruct = dict()

for key,value in linked_ids.items():
    if value not in linked_ids_reconstruct.keys():
        linked_ids_reconstruct[value]=key

file_path = "linked_ids.json"

# Open the file in write mode
with open(file_path, 'w') as json_file:
    # Serialize the dictionary to JSON and write it to the file
    json.dump(linked_ids_reconstruct, json_file)

user_devices=[]
devices_mapped=[]

device: Device
for device in manager.device_list:
    #generate_traces(str(device.bluetooth_id),str(device.wifi_id),str(device.lte_id))
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    print(a)
    print(b)
    print(c)
    user_id1=1001
    user_id2=1908
    user_id3=4678
    user_id=9829

    
    for line in data_user:
        
        if a in line.values():
            user_id1=line['user_id']
        if b in line.values():
            user_id2=line['user_id']
        if c in line.values():
            user_id3=line['user_id']
        if a is None and user_id2==user_id3:
            #print(line['user_id'])
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif user_id1==user_id2 and user_id1==user_id3:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif b is None and user_id1==user_id3:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif c is None and user_id1==user_id2:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
    print("-----------")    
    print(user_id1)
    print(user_id2)
    print(user_id3)
    print("-----------")


print(count/len(manager.device_list))     



    

 
        
