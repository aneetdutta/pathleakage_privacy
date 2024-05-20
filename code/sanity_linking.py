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

# with open('rule1.json') as f2:
#     linked_ids=json.load(f2)

# print(len(linked_ids))

with open('20240506150753_sniffed_data.json') as f1:
    data_user = json.load(f1)
 
# #  GVL512J4OPBN P322TQGO1ABY
# count=0
# userid1=12312321
# userid2=104343243240
# flag1 = False
# flag2 = False
# for key,value in linked_ids.items():
#     print(key,value)
#     # print(np.shape(data_user), type(data_user))
#     for line in data_user:
#         if key in line.values():
#             userid1=line['user_id']
#             flag1 = True
#             # print("value found", userid1)
#         if value in line.values():
#             #print(line['user_id'])
#             userid2=line['user_id']
#             flag2 = True
#             # print("value found2", userid2)
#         if userid1==userid2:
#             print(userid2)
#             flag1, flag2 = False, False
#             userid1=12312321
#             userid2=104343243240
#             count=count+1
#             break
        
#         if flag1 and flag2:
#             flag2, flag1 = False, False
#             print("Not mapped", userid1, userid2)
            
            
# print(count/len(linked_ids))

# import sys
# sys.exit()

 
        
