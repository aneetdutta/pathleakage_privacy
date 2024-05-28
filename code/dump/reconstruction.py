import csv
import json
import numpy as np
import multiprocessing
import pickle
from services.general import generate_traces
from modules.devicemanager import DeviceManager
from modules.device import Device
# Opening JSON file

pickle_file='manager.pkl'
with open(pickle_file, 'rb') as file:
    manager = pickle.load(file)


with open('linked_ids.json') as f2:
    linked_ids=json.load(f2)

with open('user_data.json') as f1:
    data_user = json.load(f1)
    
with open('sniffed_user.json') as f:
    data = json.load(f)

ground_truth=[]
reconstructed=[]




tracking=[]
user_traces=dict()

manager: DeviceManager
device: Device
for device in manager.device_list:
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    print(a)
    print(b)
    print(c)
    user_id=0
    for line in data_user:
        if a is not None and line['bluetooth_id']==a:
            user_id=line['user_id']
            break
        if b is not None and line['wifi_id']==b:
            user_id=line['user_id']
            break
        if c is not None and line['lte_id']==c:
            user_id=line['user_id']
            break
        
    generate_traces(a,b,c)
    if user_id in user_traces.keys():
        l=user_traces[user_id]
        l.append(list(set(tracking)))
    else:
        l=[]
        l.append(list(set(tracking)))
        user_traces[user_id]=l
    tracking=[]
    #if len(user_traces[user_id])==1:
    print(user_id)
    print(user_traces[user_id])
   # else:
    #    print(user_id)
     #   for item in user_traces[user_id]:
      #      print(item)
       #     print("****")
    print("----------------------------------------")
    
    #print("----")
    


