import csv
import json
import numpy as np
import multiprocessing
import pickle
# Opening JSON file
from funct.fn import extract_orjson
from modules.device import Device
from modules.devicemanager import DeviceManager

linked_ids = extract_orjson('rule1.json')
print(len(linked_ids))
data_user = extract_orjson('20240506150753_sniffed_data.json')

count=0
userid1=12312321
userid2=104343243240
flag1, flag2 = False, False
for key,value in linked_ids.items():
    print(key,value)
    for line in data_user:
        if key in line.values():
            userid1=line['user_id']
            flag1 = True
        if value in line.values():
            userid2=line['user_id']
            flag2 = True
        if userid1==userid2:
            print(userid2)
            flag1, flag2 = False, False
            userid1=12312321
            userid2=104343243240
            count=count+1
            break
        
        if flag1 and flag2:
            flag2, flag1 = False, False
            print("Not mapped", userid1, userid2)
            
print(count/len(linked_ids))
